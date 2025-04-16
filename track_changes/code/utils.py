from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


def time_ago(target_datetime: datetime, current_datetime: datetime) -> str:
    if target_datetime > current_datetime:
        return "Future time"

    delta = current_datetime - target_datetime
    if delta.total_seconds() < 60:
        return f"{int(delta.total_seconds())} second{'s' if delta.total_seconds() != 1 else ''} ago"
    elif delta.total_seconds() < 3600:
        minutes = int(delta.total_seconds() // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif delta.total_seconds() < 86400:
        hours = int(delta.total_seconds() // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif delta.total_seconds() < 604800:
        days = delta.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif delta.total_seconds() < 2592000:
        weeks = delta.days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        rdelta = relativedelta(current_datetime, target_datetime)
        if rdelta.years > 0:
            return f"{rdelta.years} year{'s' if rdelta.years != 1 else ''} ago"
        elif rdelta.months > 0:
            return f"{rdelta.months} month{'s' if rdelta.months != 1 else ''} ago"
        else:
            return f"{rdelta.days} day{'s' if rdelta.days != 1 else ''} ago"


def ensure_datetime(ts):
    if isinstance(ts, datetime):
        dt = ts
    elif isinstance(ts, str):
        ts = ts.strip()
        try:
            # Try standard ISO first (with optional Z for UTC)
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            try:
                # Try with comma milliseconds (your format)
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S,%f")
            except ValueError as e:
                raise ValueError(f"Unrecognized datetime format: {ts}") from e
    else:
        raise TypeError(f"Unsupported timestamp type: {type(ts)}")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt
