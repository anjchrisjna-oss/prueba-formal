from __future__ import annotations

from pathlib import Path
from unittest import TestCase

from app.main import app


class HistoryIntegrationTests(TestCase):
    def test_history_routes_are_registered(self) -> None:
        paths = {route.path for route in app.router.routes}
        self.assertIn("/ui/history", paths)
        self.assertIn("/ui/pallet/{pallet_id}/history", paths)

    def test_pallet_template_contains_history_shortcut(self) -> None:
        tpl = Path(__file__).resolve().parents[1] / "app" / "templates" / "pallet.html"
        html = tpl.read_text(encoding="utf-8")
        self.assertIn('/ui/pallet/{{ pallet.id }}/history', html)
        self.assertIn('Ver historial del pallet', html)
