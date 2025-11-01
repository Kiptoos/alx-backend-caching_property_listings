from django.core.cache import cache
from django.conf import settings
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    cache_key = "all_properties"
    properties = cache.get(cache_key)
    if properties is None:
        properties = list(Property.objects.all())
        cache.set(cache_key, properties, timeout=getattr(settings, "CACHE_TTL", 3600))
    return properties

def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total) if total else 0
    metrics = {"hits": hits, "misses": misses, "hit_ratio": hit_ratio}
    logger.info("Redis cache metrics: %s", metrics)
    return metrics
