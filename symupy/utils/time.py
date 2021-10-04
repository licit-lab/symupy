import math


class Date(object):
    """Short summary.

    Parameters
    ----------
    date : type
        Description of parameter `date`.

    Attributes
    ----------
    hours : type
        Description of attribute `hours`.
    minutes : type
        Description of attribute `minutes`.
    seconds : type
        Description of attribute `seconds`.
    _total_sec : type
        Description of attribute `_total_sec`.
    _significant_digit : type
        Description of attribute `_significant_digit`.
    _date : type
        Description of attribute `_date`.
    _hhmmss_to_second : type
        Description of attribute `_hhmmss_to_second`.
    _second_to_hhmmss : type
        Description of attribute `_second_to_hhmmss`.

    """

    def __init__(self, date):
        self.hours = None
        self.minutes = None
        self.seconds = None
        self._total_sec = None
        self._significant_digit = None
        if isinstance(date, str):
            self._date = date
            self._hhmmss_to_second()
        elif isinstance(date, (int, float)):
            assert date < 86400
            self._significant_digit = len(str(date).split(".")[-1])
            self._total_sec = float(date)
            self._second_to_hhmmss()

    def _second_to_hhmmss(self):
        frac = self._total_sec - int(self._total_sec)
        frac = float(
            "." + str(self._total_sec).split(".")[-1][: self._significant_digit]
        )
        mm, ss = divmod(int(self._total_sec), 60)
        hh, mm = divmod(mm, 60)
        self.hours = int(hh)
        self.minutes = int(mm)
        self.seconds = float(
            str(ss + frac).split(".")[0]
            + "."
            + str(ss + frac).split(".")[1][: self._significant_digit]
        )
        str_hh = "0" + str(self.hours) if len(str(self.hours)) == 1 else str(self.hours)
        str_mm = (
            "0" + str(self.minutes)
            if len(str(self.minutes)) == 1
            else str(self.minutes)
        )
        str_ss = (
            "0" + str(self.seconds)
            if len(str(self.seconds).split(".")[0]) == 1
            else str(self.seconds)
        )
        self._date = f"{str_hh}:{str_mm}:{str_ss}"

    def _hhmmss_to_second(self):
        hh, mm, ss = self._date.split(":")
        self.hours = int(hh)
        self.minutes = int(mm)
        self.seconds = float(ss)
        self._total_sec = (int(hh) * 60 + int(mm)) * 60 + float(ss)

    def to_seconds(self):
        return self._total_sec

    def to_hhmmss(self):
        return self._date

    def __repr__(self):
        return f"Date({self._date})"

    def __add__(self, other):
        secs = self._total_sec + other._total_sec
        return Date(secs)

    def __sub__(self, other):
        secs = self._total_sec - other._total_sec
        assert secs > 0
        return Date(secs)

    def __hash__(self):
        return hash(self._date)

    def __eq__(self, other):
        return self._total_sec == other._total_sec

    def __lt__(self, other):
        return self._total_sec < other._total_sec

    def __le__(self, other):
        return self._total_sec <= other._total_sec

    def __gt__(self, other):
        return self._total_sec > other._total_sec

    def __ge__(self, other):
        return self._total_sec >= other._total_sec


if __name__ == "__main__":
    d1 = Date("01:01:02")
    d2 = Date("01:01:01")
    d3 = d1 - d2
    d4 = Date(2365.67)
