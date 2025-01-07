from enum import StrEnum


class SessionType(StrEnum):
    RACE = "race"
    SPRINT = "sprint"

    @property
    def url_value(self) -> str:
        """Return a filename-friendly version."""
        mapping = {
            SessionType.RACE: "rac",
            SessionType.SPRINT: "spr",
        }
        return mapping[self]
