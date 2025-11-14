thonpython
from datetime import datetime, timezone

def convert_timestamp(ts):
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except Exception:
        return None