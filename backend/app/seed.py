from __future__ import annotations

from sqlalchemy.orm import Session


def seed_minimum(db: Session) -> None:
    """Carga base mínima si aplica.

    Implementación no-op para mantener arranque y tests estables.
    """
    _ = db


def seed_demo_if_empty(db: Session) -> None:
    """Carga demo opcional cuando la BD está vacía.

    Implementación no-op para mantener arranque y tests estables.
    """
    _ = db
