import logging
import os
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

logger = logging.getLogger(__name__)

tz = os.environ.get("TZ") or "Europe/Berlin"

try:
    TZ = ZoneInfo(tz)
except ZoneInfoNotFoundError:
    logger.warning("Timezone %r not found, falling back to 'Europe/Berlin'", tz)
    TZ = ZoneInfo("Europe/Berlin")
