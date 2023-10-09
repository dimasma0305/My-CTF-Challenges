import os
import redis

class Config(object):
    SESSION_TYPE = "redis"
    SESSION_PERMANENT= bool(os.environ['SESSION_PERMANENT'])
    SESSION_USE_SIGNER = bool(os.environ['SESSION_USE_SIGNER'])
    SESSION_REDIS = redis.from_url(os.environ['SESSION_REDIS'])

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']

    SECRET_KEY = os.environ['SECRET_KEY']