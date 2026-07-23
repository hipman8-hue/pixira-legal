from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_localizations as checker


NO_CARD_KEY = "pixira-does-not-receive-or-store-payment-card-details"
RESTORE_ACTION_KEY = "in-app-restore-action"
RESTORE_LABEL_SOURCE = (
    "/Users/mac/Documents/secondcam/SecondCam/Resources/Localizable.xcstrings"
)


class LocalizationCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.original_root = checker.ROOT
        self.original_page_paths = checker.PAGE_PATHS
        self.original_locale_count = checker.EXPECTED_LOCALE_COUNT
        checker.ROOT = self.root
        checker.PAGE_PATHS = {
            name: self.root / f"{name}.html"
            for name in ("privacy", "support", "terms")
        }
        checker.EXPECTED_LOCALE_COUNT = 2
        self.locales = ("ko", "en-US")
        self.back_labels = {
            "ko": "privacy-canonical-back-ko",
            "en-US": "privacy-canonical-back-en",
        }
        self.restore_labels = {
            "ko": "구매 복원",
            "en-US": "Restore Purchases",
        }
        (self.root / "style.css").write_text("", encoding="utf-8")
        contracts = self.root / "contracts"
        contracts.mkdir()
        (contracts / "restore_action_labels.json").write_text(
            json.dumps(
                {
                    "_source": RESTORE_LABEL_SOURCE,
                    "labels": self.restore_labels,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        self.write_valid_pages()

    def tearDown(self) -> None:
        checker.ROOT = self.original_root
        checker.PAGE_PATHS = self.original_page_paths
        checker.EXPECTED_LOCALE_COUNT = self.original_locale_count
        self.temporary_directory.cleanup()

    def nav(self) -> str:
        return (
            '<nav class="language-nav" id="language-list">'
            + "".join(
                f'<a href="#lang-{locale}" lang="{locale}">{locale}</a>'
                for locale in self.locales
            )
            + "</nav>"
        )

    def section_start(self, locale: str) -> str:
        return (
            f'<section class="policy-language" id="lang-{locale}" '
            f'lang="{locale}" aria-labelledby="heading-{locale}">'
            f'<h2 id="heading-{locale}">{locale}</h2>'
        )

    def metadata(self) -> str:
        return (
            '<p class="localized-meta"><strong>Date:</strong> 23 July 2026 · '
            '<strong>Operator:</strong> DesignWorks (Rep. Jaeseung Han) · '
            '<strong>Contact:</strong> '
            '<a href="mailto:hipman8@gmail.com">hipman8@gmail.com</a></p>'
        )

    def shell(self, body: str) -> str:
        return (
            '<!doctype html><html><head>'
            '<link rel="stylesheet" href="style.css">'
            f"</head><body>{body}</body></html>"
        )

    def write_valid_pages(
        self,
        *,
        support_disclosure: str = "Localized disclosure copy.",
        support_marker: str = NO_CARD_KEY,
        support_restore_marker: str | None = RESTORE_ACTION_KEY,
        support_restore_labels: dict[str, str] | None = None,
        terms_extra: dict[str, str] | None = None,
    ) -> None:
        terms_extra = terms_extra or {}
        support_restore_labels = support_restore_labels or self.restore_labels
        privacy_sections: list[str] = []
        support_sections: list[str] = []
        terms_sections: list[str] = []
        for locale in self.locales:
            back = self.back_labels[locale]
            back_link = (
                '<p class="back-to-languages">'
                f'<a href="#language-list">{back}</a></p>'
            )
            privacy_sections.append(
                self.section_start(locale)
                + self.metadata()
                + back_link
                + "</section>"
            )
            topics = "".join(f"<h3>Topic {index}</h3>" for index in range(7))
            restore_attribute = (
                f' data-restore-contract="{support_restore_marker}"'
                if support_restore_marker is not None
                else ""
            )
            support_sections.append(
                self.section_start(locale)
                + topics
                + '<p data-contract="no-card-storage" '
                + f'data-contract-key="{support_marker}"'
                + restore_attribute
                + ">"
                + support_disclosure
                + '<span data-contract="restore-action-label">'
                + support_restore_labels[locale]
                + "</span>"
                + "</p>"
                + f'<a href="privacy#lang-{locale}">Privacy</a>'
                + back_link
                + "</section>"
            )
            headings = "".join(f"<h3>Heading {index}</h3>" for index in range(8))
            purchase_terms = (
                '<ul data-contract="purchase-terms">'
                + "".join(f"<li>Clause {index}</li>" for index in range(7))
                + "</ul>"
            )
            terms_sections.append(
                self.section_start(locale)
                + self.metadata()
                + headings
                + purchase_terms
                + terms_extra.get(locale, "")
                + f'<a href="{checker.STANDARD_EULA_URL}">Standard EULA</a>'
                + back_link
                + "</section>"
            )

        checker.PAGE_PATHS["privacy"].write_text(
            self.shell(self.nav() + "".join(privacy_sections)),
            encoding="utf-8",
        )
        checker.PAGE_PATHS["support"].write_text(
            self.shell(self.nav() + "".join(support_sections)),
            encoding="utf-8",
        )
        checker.PAGE_PATHS["terms"].write_text(
            self.shell(self.nav() + "".join(terms_sections)),
            encoding="utf-8",
        )

    def run_checker(self, page: str | None = None) -> tuple[int, str]:
        previous_argv = sys.argv
        sys.argv = ["check_localizations.py"] + (
            ["--page", page] if page else []
        )
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                status = checker.main()
        finally:
            sys.argv = previous_argv
        return status, output.getvalue()

    def validate_basic_source(self, source: str) -> list[str]:
        path = self.root / "case.html"
        path.write_text(source, encoding="utf-8")
        page = checker.Page("case", path)
        errors: list[str] = []
        checker.validate_document_basics(
            page, {path.resolve(): page}, errors
        )
        return errors

    def test_root_relative_links_are_rejected(self) -> None:
        errors = self.validate_basic_source('<a href="/privacy">Privacy</a>')
        self.assertTrue(
            any("repository-relative" in error for error in errors), errors
        )

    def test_recursive_stylesheets_validate_imports_assets_and_cycles(self) -> None:
        styles = self.root / "styles"
        images = self.root / "images"
        styles.mkdir()
        images.mkdir()
        (images / "hero.png").write_bytes(b"image")
        (images / "badge.svg").write_text("<svg/>", encoding="utf-8")
        (styles / "main.css").write_text(
            '@import "nested.css";'
            '.hero{background:url("../images/hero.png")}',
            encoding="utf-8",
        )
        (styles / "nested.css").write_text(
            '@import "main.css";'
            '.badge{background:url("../images/badge.svg")}',
            encoding="utf-8",
        )
        source = '<link rel="stylesheet" href="styles/main.css">'
        self.assertEqual(self.validate_basic_source(source), [])

        (styles / "nested.css").write_text(
            '@import "https://example.com/remote.css";',
            encoding="utf-8",
        )
        errors = self.validate_basic_source(source)
        self.assertTrue(any("https://example.com" in error for error in errors))

        (styles / "nested.css").write_text(
            '.remote{background:url("https://example.com/remote.png")}',
            encoding="utf-8",
        )
        errors = self.validate_basic_source(source)
        self.assertTrue(any("remote.png" in error for error in errors))

        (styles / "nested.css").write_text(
            '@import "missing.css";', encoding="utf-8"
        )
        errors = self.validate_basic_source(source)
        self.assertTrue(any("CSS import does not resolve" in error for error in errors))

        (styles / "nested.css").write_text(
            '.missing{background:url("../images/missing.png")}',
            encoding="utf-8",
        )
        errors = self.validate_basic_source(source)
        self.assertTrue(any("CSS asset does not resolve" in error for error in errors))

    def test_malformed_nesting_and_duplicate_ids_are_rejected(self) -> None:
        errors = self.validate_basic_source(
            '<div id="duplicate"><span id="duplicate"></div>'
        )
        self.assertTrue(any("duplicate id" in error for error in errors), errors)
        self.assertTrue(any("misnested" in error for error in errors), errors)

    def test_cli_scopes_validate_only_selected_production_page(self) -> None:
        support_status, support_output = self.run_checker("support")
        terms_status, terms_output = self.run_checker("terms")
        all_status, all_output = self.run_checker()
        self.assertEqual((support_status, terms_status, all_status), (0, 0, 0))
        self.assertIn("scope=support", support_output)
        self.assertIn("scope=terms", terms_output)
        self.assertIn("scope=all", all_output)

        self.write_valid_pages(
            terms_extra={"en-US": "<p>Classic pack</p>"}
        )
        self.assertEqual(self.run_checker("support")[0], 0)
        self.assertEqual(self.run_checker("terms")[0], 1)

    def test_stale_custom_eula_and_card_contract_rules(self) -> None:
        self.write_valid_pages(
            terms_extra={
                "ko": "<p>커스텀 EULA 여부</p>",
                "en-US": "<p>premium content</p>",
            }
        )
        status, output = self.run_checker("terms")
        self.assertEqual(status, 1)
        self.assertIn("Korean custom EULA phrase", output)
        self.assertIn('stale claim "premium content"', output)

        self.write_valid_pages(
            support_disclosure=(
                "Localized disclosure copy. "
                "The app keeps card and payment details."
            )
        )
        status, output = self.run_checker("support")
        self.assertEqual(status, 1)
        self.assertIn("contradictory positive", output)

        self.write_valid_pages(support_marker="wrong-contract-key")
        status, output = self.run_checker("support")
        self.assertEqual(status, 1)
        self.assertIn("data-contract-key", output)

    def test_korean_effective_date_does_not_match_three_day_trial(self) -> None:
        pattern = checker.STALE_CLAIMS["3일"]
        self.assertIsNone(pattern.search("시행일: 2026년 7월 23일"))
        self.assertIsNotNone(pattern.search("첫 3일 무료 체험"))

    def test_support_requires_in_app_restore_action_contract(self) -> None:
        self.write_valid_pages(support_restore_marker=None)
        status, output = self.run_checker("support")
        self.assertEqual(status, 1)
        self.assertIn("data-restore-contract", output)

    def test_support_rejects_wrong_english_or_mixed_restore_label(self) -> None:
        mutations = (
            "복원 구매",
            "Restore Purchases",
            "구매 복원 / Restore Purchases",
        )
        for mutated_label in mutations:
            with self.subTest(mutated_label=mutated_label):
                labels = dict(self.restore_labels)
                labels["ko"] = mutated_label
                self.write_valid_pages(support_restore_labels=labels)
                status, output = self.run_checker("support")
                self.assertEqual(status, 1)
                self.assertIn("restore-action-label", output)


if __name__ == "__main__":
    unittest.main()
