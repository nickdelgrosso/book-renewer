from datetime import datetime
from src.app.app import Clock

class DatetimeClock(Clock):

    def set_current(self, current: datetime):
        raise IOError("Not Possible")

    def get_current(self) -> datetime:
        return datetime.now()