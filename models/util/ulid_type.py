import ulid
from sqlalchemy.types import TypeDecorator, BINARY
from sqlmodel import Field
from typing import Any


class ULIDBinary(TypeDecorator):
    """
    Handles the transparent conversion:
    Python (String) <---> MySQL (BINARY 16)
    """
    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> bytes | None:
        if value is None:
            return None
        # Ensure it's a valid ULID and convert to bytes
        return ulid.from_str(str(value)).bytes

    def process_result_value(self, value: Any, dialect: Any) -> str | None:
        if value is None:
            return None
        # Convert binary back to string for Python/API use
        return str(ulid.from_bytes(value))


def ulid_field(primary_key: bool = False, **kwargs):
    """
    Reusable ULID field for SQLModel.
    - If primary_key=True: automatically adds a default generator.
    - If primary_key=False: works as a standard or foreign key field.
    """
    default_factory = lambda: str(ulid.new()) if primary_key else None

    return Field(
        default_factory=default_factory,
        sa_type=ULIDBinary,
        primary_key=primary_key,
        **kwargs
    )
