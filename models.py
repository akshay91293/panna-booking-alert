from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Snapshot:
    park_name: Optional[str] = None
    to_dt: Optional[str] = None
    rule_image: Optional[str] = None
    single_seat_banner: Optional[str] = None
    tatkal_banner: Optional[str] = None
    important_notes: Optional[str] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Change:
    field: str
    previous: Optional[str]
    current: Optional[str]
