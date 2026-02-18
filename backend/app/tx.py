from __future__ import annotations

from contextlib import contextmanager
from sqlalchemy.orm import Session


@contextmanager
def smart_begin(db: Session):
    """Abre transacción sólo si no hay una activa; compatible con uso anidado."""
    if db.in_transaction():
        yield
        return

    with db.begin():
        yield
