from datetime import datetime, timedelta


def get_period_date(period):

    now = datetime.now()

    if period == "день":
        return now - timedelta(days=1)

    elif period == "неделя":
        return now - timedelta(days=7)

    elif period == "месяц":
        return now - timedelta(days=30)

    elif period == "год":
        return now - timedelta(days=365)

    return now - timedelta(days=30)