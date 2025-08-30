from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class StaticVideoSource:
    title: str
    file_type: str
    quality: str
    link: str
    link_expires: Optional[float]

    def is_expired(self) -> bool:
        if self.link_expires is None or datetime.fromtimestamp(self.link_expires, tz=timezone.utc) > datetime.now(tz=timezone.utc):
            return False

        return True

    def __repr__(self) -> str:
        return f"{self.title}\nquality: {self.quality}\nvideo_url: {self.link}\nexpired: {self.is_expired()}"

