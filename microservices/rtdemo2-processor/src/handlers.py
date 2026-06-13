"""Developer logic slot (RT-2). The platform owns transport (Kafka, /ws, HTTP);
this module owns what the bytes MEAN. Implement per REQUIREMENTS.md; the
post-deploy contract test is the acceptance gate.

- to_message(body)  : ingest    — map an HTTP POST body to the produced event.
- transform(message): processor — map a consumed event to the produced event
                                  (return None to drop).
Defaults are passthrough/identity so the service boots before logic lands.
"""
from collections import deque
from typing import Deque
from typing import Any, Dict, Optional


SENSOR_WINDOWS: Dict[Any, Deque[float]] = {}


def to_message(body: Dict[str, Any]) -> Dict[str, Any]:
    return body


def transform(message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    sensor_id = message.get("sensor_id")
    if sensor_id is None:
        return None

    value = message.get("value")
    if isinstance(value, bool):
        return None

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None

    window = SENSOR_WINDOWS.setdefault(sensor_id, deque(maxlen=10))
    window.append(numeric_value)

    return {
        "sensor_id": sensor_id,
        "value": numeric_value,
        "rolling_avg": sum(window) / len(window),
        "count": len(window),
        "ts": message.get("ts"),
    }
