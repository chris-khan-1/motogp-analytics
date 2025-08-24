from enum import StrEnum


class SessionType(StrEnum):
    RACE = "race"
    SPRINT = "sprint"
    QUALIFYING_1 = "q1"
    QUALIFYING_2 = "q2"

    @property
    def url_value(self) -> str:
        """Return a url version of session."""
        mapping = {
            self.RACE: "rac",
            self.SPRINT: "spr",
            self.QUALIFYING_1: "q1",
            self.QUALIFYING_2: "q2",
        }
        return mapping[self]
