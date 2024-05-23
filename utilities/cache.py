
from flask_caching import Cache

client_cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
