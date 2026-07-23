#!/usr/bin/env python3
"""Validate Pixira's static legal-page localization contract."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent.parent
PAGE_PATHS = {
    "privacy": ROOT / "privacy.html",
    "support": ROOT / "support.html",
    "terms": ROOT / "terms.html",
}
EXPECTED_LOCALE_COUNT = 29
RTL_LOCALES = {"ar", "he"}
LANGUAGE_LIST_ID = "language-list"
STANDARD_EULA_URL = (
    "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
)
CONTACT_EMAIL = "hipman8@gmail.com"
EMAIL_RE = re.compile(r"^[^@\s/?#]+@[^@\s/?#]+\.[^@\s/?#]+$")
STALE_CLAIMS = {
    "3-day": re.compile(r"\b3[\s-]*day\b", re.IGNORECASE),
    "3일": re.compile(r"3\s*일"),
    "6 default": re.compile(r"\b(?:6\s+default|default\s+6)\b", re.IGNORECASE),
    "기본 6개": re.compile(r"기본\s*6\s*개"),
    "individual bodies": re.compile(r"\bindividual\s+bodies\b", re.IGNORECASE),
    "개별 바디": re.compile(r"개별\s*바디"),
    "Classic pack": re.compile(r"\bclassic\s+pack\b", re.IGNORECASE),
    "클래식 팩": re.compile(r"클래식\s*팩"),
    "premium content": re.compile(r"\bpremium\s+content\b", re.IGNORECASE),
    "프리미엄 콘텐츠": re.compile(r"프리미엄\s*콘텐츠"),
    "same-price renewal": re.compile(
        r"(?:\b(?:auto(?:matically)?[\s-]*)?renew\w*\b.{0,60}\bsame\s+price\b"
        r"|\bsame\s+price\b.{0,60}\b(?:auto(?:matically)?[\s-]*)?renew\w*\b)",
        re.IGNORECASE,
    ),
    "동일 가격 자동갱신": re.compile(
        r"(?:동일\s*가격.{0,40}(?:자동\s*)?갱신|(?:자동\s*)?갱신.{0,40}동일\s*가격)"
    ),
}
FORBIDDEN_CUSTOM_EULA_PHRASES = {
    "English custom EULA phrase": re.compile(r"\bcustom\s+EULA\b", re.IGNORECASE),
    "Korean custom EULA phrase": re.compile(
        r"(?:커스텀|사용자\s*지정)\s*EULA", re.IGNORECASE
    ),
}
CONTRADICTORY_NO_CARD_ASSERTIONS = {
    "English positive card/payment handling claim": re.compile(
        r"\b(?:Pixira|the\s+app|we)\s+"
        r"(?:receives?|stores?|collects?|retains?|keeps?)\b"
        r".{0,60}\b(?:card|payment)\b",
        re.IGNORECASE,
    ),
    "Korean positive card/payment handling claim": re.compile(
        r"(?:Pixira|앱|당사|운영자)(?:는|은|가)?"
        r"[^.!?。！？]{0,60}(?:카드|결제)"
        r"[^.!?。！？]{0,60}"
        r"(?:받습니다|받아요|받는다|수신합니다|수신한다|저장합니다|저장한다|"
        r"보관합니다|보관한다|수집합니다|수집한다|유지합니다|유지한다)"
    ),
}
CSS_URL_FUNCTION_RE = re.compile(
    r"url\s*\(\s*(?:([\"'])(.*?)\1|([^)]*?))\s*\)",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMPORT_RE = re.compile(r"@import\s+([^;]+)", re.IGNORECASE | re.DOTALL)
NO_CARD_CONTRACT_KEY = (
    "pixira-does-not-receive-or-store-payment-card-details"
)
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
RUNTIME_URL_ATTRIBUTES = {
    "audio": ("src",),
    "embed": ("src",),
    "form": ("action",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "input": ("src",),
    "object": ("data",),
    "source": ("src", "srcset"),
    "track": ("src",),
    "video": ("poster", "src"),
}
RUNTIME_LINK_RELS = {
    "apple-touch-icon",
    "dns-prefetch",
    "icon",
    "manifest",
    "mask-icon",
    "modulepreload",
    "preconnect",
    "prefetch",
    "preload",
    "stylesheet",
}


def normalized(value: str) -> str:
    return " ".join(value.split())


def class_tokens(value: str | None) -> set[str]:
    return set((value or "").split())


class Node:
    def __init__(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]] | None = None,
        parent: Node | None = None,
    ) -> None:
        self.tag = tag
        self.attrs = {key: value or "" for key, value in (attrs or [])}
        self.parent = parent
        self.children: list[Node | str] = []

    def descendants(self, tag: str | None = None) -> Iterable[Node]:
        for child in self.children:
            if not isinstance(child, Node):
                continue
            if tag is None or child.tag == tag:
                yield child
            yield from child.descendants(tag)

    def has_class(self, name: str) -> bool:
        return name in class_tokens(self.attrs.get("class"))

    def text_content(self) -> str:
        parts: list[str] = []
        for child in self.children:
            parts.append(child.text_content() if isinstance(child, Node) else child)
        return normalized(" ".join(parts))


class DocumentParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.root = Node("document")
        self.stack = [self.root]
        self.parse_errors: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        node = Node(tag.lower(), attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag.lower() not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        node = Node(tag.lower(), attrs, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        wanted = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == wanted:
                if index != len(self.stack) - 1:
                    self.parse_errors.append(
                        f"misnested closing tag </{wanted}>; "
                        f"expected </{self.stack[-1].tag}>"
                    )
                del self.stack[index:]
                return
        self.parse_errors.append(f"unexpected closing tag </{wanted}>")

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)

    def close(self) -> None:
        super().close()
        if len(self.stack) > 1:
            unclosed = ", ".join(f"<{node.tag}>" for node in self.stack[1:])
            self.parse_errors.append(f"unclosed tags at end of document: {unclosed}")
            self.stack = [self.root]


class Page:
    def __init__(self, name: str, path: Path) -> None:
        self.name = name
        self.path = path
        self.source = path.read_text(encoding="utf-8")
        parser = DocumentParser(path)
        parser.feed(self.source)
        parser.close()
        self.root = parser.root
        self.parse_errors = parser.parse_errors

    @property
    def nodes(self) -> list[Node]:
        return list(self.root.descendants())

    @property
    def sections(self) -> list[Node]:
        return [node for node in self.nodes if node.has_class("policy-language")]

    @property
    def id_nodes(self) -> dict[str, list[Node]]:
        result: dict[str, list[Node]] = {}
        for node in self.nodes:
            node_id = node.attrs.get("id")
            if node_id:
                result.setdefault(node_id, []).append(node)
        return result

    def section_for_locale(self, locale: str) -> Node | None:
        wanted = f"lang-{locale}"
        return next(
            (section for section in self.sections if section.attrs.get("id") == wanted),
            None,
        )

    def language_nav_links(self) -> list[Node]:
        navs = [node for node in self.nodes if node.has_class("language-nav")]
        if len(navs) != 1:
            return []
        return list(navs[0].descendants("a"))

    def locale_order(self) -> list[str]:
        result: list[str] = []
        for link in self.language_nav_links():
            href = link.attrs.get("href", "")
            if href.startswith("#lang-"):
                result.append(href.removeprefix("#lang-"))
        return result


def add_error(errors: list[str], page: Page, message: str) -> None:
    errors.append(f"{page.path.name}: {message}")


def resolve_local_path(current: Path, raw_path: str) -> Path | None:
    path = unquote(raw_path)
    if path.startswith("/"):
        return None
    if path in {"", "."}:
        return current.resolve()
    candidate = current.parent / path
    candidates = [candidate]
    if candidate.suffix == "":
        candidates.extend([candidate.with_suffix(".html"), candidate / "index.html"])
    root = ROOT.resolve()
    for possible in candidates:
        resolved = possible.resolve()
        if resolved.is_relative_to(root) and resolved.exists():
            return resolved
    return None


def is_prohibited_runtime_url(tag: str, attr: str, value: str) -> bool:
    if value.startswith("/"):
        return True
    parsed = urlparse(value)
    scheme = parsed.scheme.casefold()
    if not scheme:
        return False
    if scheme == "data" and (tag, attr) in {
        ("img", "src"),
        ("source", "src"),
        ("video", "poster"),
    }:
        return False
    return True


def css_url_value(raw_value: str) -> str:
    value = raw_value.strip()
    if (
        len(value) >= 2
        and value[0] in {'"', "'"}
        and value[-1] == value[0]
    ):
        return value[1:-1].strip()
    return value


def is_prohibited_css_url(value: str, *, allow_data_image: bool) -> bool:
    if value.startswith("/"):
        return True
    scheme = urlparse(value).scheme.casefold()
    if not scheme:
        return False
    if (
        scheme == "data"
        and allow_data_image
        and value.casefold().startswith("data:image/")
    ):
        return False
    return True


def css_import_urls(css: str) -> list[str]:
    imports: list[str] = []
    for match in CSS_IMPORT_RE.finditer(css):
        import_target = match.group(1).strip()
        url_match = CSS_URL_FUNCTION_RE.search(import_target)
        if url_match:
            value = css_url_value(url_match.group(2) or url_match.group(3) or "")
        else:
            quoted = re.match(r"""(["'])(.*?)\1""", import_target, re.DOTALL)
            value = (
                quoted.group(2).strip()
                if quoted
                else css_url_value(import_target.split()[0])
            )
        if value:
            imports.append(value)
    return list(dict.fromkeys(imports))


def css_function_urls(css: str) -> list[str]:
    urls: list[str] = []
    for match in CSS_URL_FUNCTION_RE.finditer(css):
        value = css_url_value(match.group(2) or match.group(3) or "")
        if value:
            urls.append(value)
    return list(dict.fromkeys(urls))


def resolve_css_path(current: Path, raw_url: str) -> Path | None:
    parsed = urlparse(raw_url)
    path = unquote(parsed.path)
    if not path or path.startswith("/"):
        return None
    resolved = (current.parent / path).resolve()
    if not resolved.is_relative_to(ROOT.resolve()) or not resolved.is_file():
        return None
    return resolved


def validate_css_source(
    css: str,
    current: Path,
    source: str,
    page: Page,
    errors: list[str],
    visited_stylesheets: set[Path],
) -> None:
    imports = css_import_urls(css)
    for import_url in imports:
        if is_prohibited_css_url(import_url, allow_data_image=False):
            add_error(
                errors,
                page,
                f'non-local CSS import is prohibited in {source}: "{import_url}"',
            )
            continue
        imported_path = resolve_css_path(current, import_url)
        if imported_path is None:
            add_error(
                errors,
                page,
                f'CSS import does not resolve in {source}: "{import_url}"',
            )
            continue
        validate_local_stylesheet(
            imported_path, page, errors, visited_stylesheets
        )

    imported_urls = set(imports)
    for asset_url in css_function_urls(css):
        if asset_url in imported_urls:
            continue
        if is_prohibited_css_url(asset_url, allow_data_image=True):
            add_error(
                errors,
                page,
                f'non-local CSS runtime resource is prohibited in {source}: "{asset_url}"',
            )
            continue
        if asset_url.casefold().startswith("data:image/"):
            continue
        parsed = urlparse(asset_url)
        if not parsed.path and parsed.fragment:
            continue
        if resolve_css_path(current, asset_url) is None:
            add_error(
                errors,
                page,
                f'CSS asset does not resolve in {source}: "{asset_url}"',
            )


def validate_local_stylesheet(
    stylesheet_path: Path,
    page: Page,
    errors: list[str],
    visited_stylesheets: set[Path],
) -> None:
    resolved = stylesheet_path.resolve()
    if resolved in visited_stylesheets:
        return
    visited_stylesheets.add(resolved)
    try:
        stylesheet = resolved.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        add_error(
            errors,
            page,
            f'local stylesheet cannot be read as UTF-8: "{resolved}"',
        )
        return
    validate_css_source(
        stylesheet,
        resolved,
        f'linked stylesheet "{resolved.relative_to(ROOT.resolve())}"',
        page,
        errors,
        visited_stylesheets,
    )


def validate_document_basics(
    page: Page, pages_by_path: dict[Path, Page], errors: list[str]
) -> None:
    visited_stylesheets: set[Path] = set()
    for parse_error in page.parse_errors:
        add_error(errors, page, parse_error)

    for node_id, nodes in page.id_nodes.items():
        if len(nodes) != 1:
            add_error(errors, page, f'duplicate id "{node_id}"')

    ids = set(page.id_nodes)
    for node in page.nodes:
        labelledby = node.attrs.get("aria-labelledby")
        if labelledby:
            for target in labelledby.split():
                if target not in ids:
                    add_error(
                        errors,
                        page,
                        f'aria-labelledby target "#{target}" does not exist',
                    )

    if any(node.tag == "script" for node in page.nodes):
        add_error(errors, page, "<script> is prohibited")

    for node in page.nodes:
        css_sources: list[tuple[str, str]] = []
        if node.tag == "style":
            css_sources.append(("<style>", node.text_content()))
        if "style" in node.attrs:
            css_sources.append((f"<{node.tag} style>", node.attrs["style"]))
        for source, css in css_sources:
            validate_css_source(
                css,
                page.path,
                source,
                page,
                errors,
                visited_stylesheets,
            )

        if node.tag == "meta":
            http_equiv = node.attrs.get("http-equiv", "").casefold()
            if http_equiv in {"refresh", "set-cookie"}:
                add_error(errors, page, f'meta http-equiv="{http_equiv}" is prohibited')

        runtime_attrs = list(RUNTIME_URL_ATTRIBUTES.get(node.tag, ()))
        if node.tag == "link":
            rel = class_tokens(node.attrs.get("rel", "").casefold())
            if rel.intersection(RUNTIME_LINK_RELS):
                runtime_attrs.append("href")
        for attr in runtime_attrs:
            value = node.attrs.get(attr, "")
            candidates = value.split(",") if attr == "srcset" else [value]
            if any(
                is_prohibited_runtime_url(
                    node.tag, attr, candidate.strip().split()[0]
                )
                for candidate in candidates
                if candidate.strip()
            ):
                add_error(
                    errors,
                    page,
                    f'non-local runtime resource is prohibited: <{node.tag} {attr}="{value}">',
                )

        if node.tag == "link":
            rel = class_tokens(node.attrs.get("rel", "").casefold())
            href = node.attrs.get("href", "")
            parsed_href = urlparse(href)
            if (
                "stylesheet" in rel
                and href
                and not parsed_href.scheme
                and not href.startswith("//")
            ):
                stylesheet_path = resolve_local_path(page.path, parsed_href.path)
                if stylesheet_path is not None:
                    validate_local_stylesheet(
                        stylesheet_path,
                        page,
                        errors,
                        visited_stylesheets,
                    )

    for node in page.nodes:
        href = node.attrs.get("href")
        if not href:
            continue
        parsed = urlparse(href)
        if parsed.scheme == "mailto":
            address = parsed.path
            if not EMAIL_RE.fullmatch(address):
                add_error(errors, page, f'invalid mailto link "{href}"')
            continue
        if parsed.scheme or href.startswith("//"):
            continue

        if parsed.path.startswith("/"):
            add_error(
                errors,
                page,
                f'root-relative link is invalid; use a repository-relative link: "{href}"',
            )
            continue
        target_path = resolve_local_path(page.path, parsed.path)
        if target_path is None:
            add_error(errors, page, f'local link does not resolve: "{href}"')
            continue
        if parsed.fragment:
            target_page = pages_by_path.get(target_path)
            if target_page is None:
                try:
                    target_page = Page(target_path.stem, target_path)
                except (OSError, UnicodeDecodeError):
                    target_page = None
            if target_page is None or parsed.fragment not in target_page.id_nodes:
                add_error(errors, page, f'fragment target does not resolve: "{href}"')


def localized_back_labels(
    privacy: Page, expected_locales: list[str], errors: list[str]
) -> dict[str, str]:
    labels: dict[str, str] = {}
    for locale in expected_locales:
        section = privacy.section_for_locale(locale)
        if section is None:
            continue
        links = [
            anchor
            for block in section.descendants()
            if block.has_class("back-to-languages")
            for anchor in block.descendants("a")
            if anchor.attrs.get("href") == f"#{LANGUAGE_LIST_ID}"
            and anchor.text_content()
        ]
        if len(links) == 1:
            labels[locale] = links[0].text_content()
        else:
            add_error(
                errors,
                privacy,
                f"{locale} Privacy section cannot define one localized back-link label",
            )
    return labels


def validate_locale_shell(
    page: Page,
    expected_locales: list[str],
    expected_back_labels: dict[str, str],
    errors: list[str],
) -> None:
    links = page.language_nav_links()
    nav_count = len([node for node in page.nodes if node.has_class("language-nav")])
    if nav_count != 1:
        add_error(errors, page, f"expected one .language-nav, found {nav_count}")

    actual_order = page.locale_order()
    if actual_order != expected_locales:
        add_error(
            errors,
            page,
            f"locale navigation mismatch: expected {expected_locales}, got {actual_order}",
        )

    section_locales = [
        section.attrs.get("id", "").removeprefix("lang-")
        for section in page.sections
        if section.attrs.get("id", "").startswith("lang-")
    ]
    if section_locales != expected_locales:
        add_error(
            errors,
            page,
            f"locale section mismatch: expected {expected_locales}, got {section_locales}",
        )

    for link in links:
        href = link.attrs.get("href", "")
        if not href.startswith("#lang-"):
            add_error(errors, page, f'language-nav link is not a #lang-* fragment: "{href}"')
        if not link.attrs.get("lang"):
            add_error(errors, page, f'language-nav link "{href}" is missing lang')

    for locale in expected_locales:
        link = next(
            (
                candidate
                for candidate in links
                if candidate.attrs.get("href") == f"#lang-{locale}"
            ),
            None,
        )
        section = page.section_for_locale(locale)
        if link is not None and locale in RTL_LOCALES:
            if link.attrs.get("dir", "").casefold() != "rtl":
                add_error(errors, page, f"{locale} navigation link must use dir=rtl")
        if section is None:
            continue
        if not section.attrs.get("lang"):
            add_error(errors, page, f"{locale} section is missing lang")
        if locale in RTL_LOCALES and section.attrs.get("dir", "").casefold() != "rtl":
            add_error(errors, page, f"{locale} section must use dir=rtl")

        labelledby = section.attrs.get("aria-labelledby", "")
        headings = [
            node
            for node in section.descendants("h2")
            if node.attrs.get("id") == labelledby
        ]
        if len(headings) != 1:
            add_error(
                errors,
                page,
                f"{locale} section must have one h2 matching aria-labelledby",
            )

        back_blocks = [
            node for node in section.descendants() if node.has_class("back-to-languages")
        ]
        valid_back_links = [
            anchor
            for block in back_blocks
            for anchor in block.descendants("a")
            if anchor.attrs.get("href") == f"#{LANGUAGE_LIST_ID}"
            and anchor.text_content()
        ]
        if len(back_blocks) != 1 or len(valid_back_links) != 1:
            add_error(
                errors,
                page,
                f"{locale} section needs one localized back-to-language-list link",
            )
        elif valid_back_links[0].text_content() != expected_back_labels.get(locale):
            add_error(
                errors,
                page,
                f"{locale} back-to-language-list label must match localized contract copy",
            )


def direct_list_items(node: Node) -> list[Node]:
    return [
        child for child in node.children if isinstance(child, Node) and child.tag == "li"
    ]


def metadata_value_after_strong(meta: Node, strong_index: int) -> str | None:
    strong_positions = [
        index
        for index, child in enumerate(meta.children)
        if isinstance(child, Node) and child.tag == "strong"
    ]
    if strong_index >= len(strong_positions):
        return None
    start = strong_positions[strong_index] + 1
    end = (
        strong_positions[strong_index + 1]
        if strong_index + 1 < len(strong_positions)
        else len(meta.children)
    )
    parts: list[str] = []
    for child in meta.children[start:end]:
        if isinstance(child, Node):
            if child.tag == "a":
                continue
            parts.append(child.text_content())
        else:
            parts.append(child)
    return normalized(" ".join(parts)).strip(" ·")


def validate_support(
    page: Page, expected_locales: list[str], errors: list[str]
) -> None:
    for locale in expected_locales:
        section = page.section_for_locale(locale)
        if section is None:
            continue
        headings = list(section.descendants("h3"))
        if len(headings) != 7:
            add_error(
                errors,
                page,
                f"{locale} Support section must have exactly 7 h3 topics; found {len(headings)}",
            )

        privacy_links = [
            node
            for node in section.descendants("a")
            if node.attrs.get("href") == f"privacy#lang-{locale}"
        ]
        if len(privacy_links) != 1:
            add_error(
                errors,
                page,
                f"{locale} Support section must link once to privacy#lang-{locale}",
            )

        disclosures = [
            node
            for node in section.descendants()
            if node.attrs.get("data-contract") == "no-card-storage"
        ]
        if (
            len(disclosures) != 1
            or disclosures[0].attrs.get("data-contract-key")
            != NO_CARD_CONTRACT_KEY
        ):
            add_error(
                errors,
                page,
                f'{locale} Support section needs one data-contract="no-card-storage" disclosure with data-contract-key="{NO_CARD_CONTRACT_KEY}"',
            )
        elif any(
            pattern.search(disclosures[0].text_content())
            for pattern in CONTRADICTORY_NO_CARD_ASSERTIONS.values()
        ):
            add_error(
                errors,
                page,
                f"{locale} no-card-storage disclosure contains a contradictory positive card/payment handling claim",
            )


def validate_terms_metadata(
    terms_section: Node,
    privacy_section: Node,
    locale: str,
    page: Page,
    errors: list[str],
) -> None:
    terms_meta = [
        node for node in terms_section.descendants() if node.has_class("localized-meta")
    ]
    privacy_meta = [
        node for node in privacy_section.descendants() if node.has_class("localized-meta")
    ]
    if len(terms_meta) != 1 or len(privacy_meta) != 1:
        add_error(
            errors,
            page,
            f"{locale} Terms section must have one localized-meta matching Privacy",
        )
        return

    for index, label in ((0, "effective date"), (1, "operator")):
        terms_value = metadata_value_after_strong(terms_meta[0], index)
        privacy_value = metadata_value_after_strong(privacy_meta[0], index)
        if not terms_value or terms_value != privacy_value:
            add_error(
                errors,
                page,
                f"{locale} Terms {label} does not match Privacy: "
                f"{terms_value!r} != {privacy_value!r}",
            )

    mailtos = [
        node.attrs.get("href", "")
        for node in terms_meta[0].descendants("a")
        if node.attrs.get("href", "").startswith("mailto:")
    ]
    if mailtos != [f"mailto:{CONTACT_EMAIL}"]:
        add_error(
            errors,
            page,
            f"{locale} Terms metadata must contain contact {CONTACT_EMAIL}",
        )


def validate_terms(
    page: Page,
    privacy: Page,
    expected_locales: list[str],
    errors: list[str],
) -> None:
    for locale in expected_locales:
        section = page.section_for_locale(locale)
        privacy_section = privacy.section_for_locale(locale)
        if section is None or privacy_section is None:
            continue

        headings = list(section.descendants("h3"))
        if len(headings) != 8:
            add_error(
                errors,
                page,
                f"{locale} Terms section must have exactly 8 h3 headings; found {len(headings)}",
            )

        purchase_lists = [
            item
            for item in section.descendants("ul")
            if item.attrs.get("data-contract") == "purchase-terms"
        ]
        if (
            len(purchase_lists) != 1
            or len(direct_list_items(purchase_lists[0])) != 7
        ):
            counts = [len(direct_list_items(item)) for item in purchase_lists]
            add_error(
                errors,
                page,
                f'{locale} Terms section needs exactly one data-contract="purchase-terms" list with 7 direct items; found {counts}',
            )

        eula_links = [
            node
            for node in section.descendants("a")
            if node.attrs.get("href") == STANDARD_EULA_URL
        ]
        if len(eula_links) != 1:
            add_error(
                errors,
                page,
                f"{locale} Terms section must link once to the Apple Standard EULA",
            )

        validate_terms_metadata(section, privacy_section, locale, page, errors)

    localized_sections = {
        locale: page.section_for_locale(locale) for locale in ("ko", "en-US")
    }
    assertion_scopes = (
        localized_sections
        if all(localized_sections.values())
        else {"unstructured Korean/English copy": page.root}
    )
    for locale, scope in assertion_scopes.items():
        assert scope is not None
        text = scope.text_content()
        for label, pattern in FORBIDDEN_CUSTOM_EULA_PHRASES.items():
            if pattern.search(text):
                add_error(errors, page, f"{locale} contains {label}")


def validate_stale_claims(page: Page, errors: list[str]) -> None:
    text = page.root.text_content()
    for label, pattern in STALE_CLAIMS.items():
        if pattern.search(text):
            add_error(errors, page, f'contains stale claim "{label}"')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--page",
        choices=("support", "terms"),
        help="validate Privacy plus only the selected production page",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected_names = ["privacy", args.page] if args.page else list(PAGE_PATHS)
    pages = {name: Page(name, PAGE_PATHS[name]) for name in selected_names}
    privacy = pages["privacy"]
    pages_by_path = {page.path.resolve(): page for page in pages.values()}
    errors: list[str] = []

    expected_locales = privacy.locale_order()
    if len(expected_locales) != EXPECTED_LOCALE_COUNT:
        add_error(
            errors,
            privacy,
            f"Privacy locale contract must contain {EXPECTED_LOCALE_COUNT} entries; "
            f"found {len(expected_locales)}",
        )
    if len(expected_locales) != len(set(expected_locales)):
        add_error(errors, privacy, "Privacy locale navigation contains duplicates")

    expected_back_labels = localized_back_labels(
        privacy, expected_locales, errors
    )
    for page in pages.values():
        validate_document_basics(page, pages_by_path, errors)
        validate_locale_shell(
            page, expected_locales, expected_back_labels, errors
        )

    if "support" in pages:
        validate_support(pages["support"], expected_locales, errors)
        validate_stale_claims(pages["support"], errors)
    if "terms" in pages:
        validate_terms(pages["terms"], privacy, expected_locales, errors)
        validate_stale_claims(pages["terms"], errors)

    if errors:
        print(f"LOCALIZATION CONTRACT FAILED ({len(errors)} errors)")
        for error in errors:
            print(f"- {error}")
        return 1

    scope = args.page or "all"
    print(
        f"LOCALIZATION CONTRACT PASSED: scope={scope}, "
        f"locales={len(expected_locales)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
