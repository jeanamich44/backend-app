import calendar
from datetime import date

# ----------------------------------------------------------------------


def get_days_in_month(month: int, year: int) -> int:
    return calendar.monthrange(year, month)[1]


def get_month_sequence(start_month: int, start_year: int, count: int) -> list[tuple[int, int]]:
    seq = []
    curr_m = int(start_month)
    curr_y = int(start_year)
    for _ in range(max(1, count)):
        seq.append((curr_m, curr_y))
        curr_m += 1
        if curr_m > 12:
            curr_m = 1
            curr_y += 1
    return seq


def get_retroactive_sequence(count: int = 3, end_month: int | None = None, end_year: int | None = None) -> list[tuple[int, int]]:
    if end_month is None or end_year is None:
        today = date.today()
        first_of_this_month = date(today.year, today.month, 1)
        if first_of_this_month.month == 1:
            end_month = 12
            end_year = first_of_this_month.year - 1
        else:
            end_month = first_of_this_month.month - 1
            end_year = first_of_this_month.year

    curr_m = end_month
    curr_y = end_year
    rev = []
    for _ in range(max(1, count)):
        rev.append((curr_m, curr_y))
        curr_m -= 1
        if curr_m < 1:
            curr_m = 12
            curr_y -= 1
    rev.reverse()
    return rev


def get_last_business_day(month: int, year: int) -> int:
    last_day = get_days_in_month(month, year)
    d = date(year, month, last_day)
    while d.weekday() >= 5:
        d = date(year, month, d.day - 1)
    return d.day


def get_payment_date_str(month: int, year: int) -> str:
    day = get_last_business_day(month, year)
    return f"le {day:02d}/{month:02d}/{year}"


def get_period_strings(month: int, year: int) -> tuple[str, str]:
    last_day = get_days_in_month(month, year)
    return (f"01/{month:02d}/{year}", f"{last_day:02d}/{month:02d}/{year}")
