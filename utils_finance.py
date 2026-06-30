def calculate_shift(hours: float, rate: float, revenue: float, percent: float) -> float:
    hourly_pay = hours * rate
    revenue_share = revenue * percent / 100
    return round(hourly_pay + revenue_share, 2)
