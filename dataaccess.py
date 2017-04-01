import json
import redis


def write(key, value):
    # return None
    redis_instance = redis.Redis(host='localhost', port='6379', db=1)

    redis_key = json.dumps(key, sort_keys=True)
    redis_instance.set(redis_key, json.dumps(value))


def get(key):
    # return None
    redis_instance = redis.Redis(host='localhost', port='6379', db=1, decode_responses=True)
    redis_key = json.dumps(key, sort_keys=True)

    cached_value = redis_instance.get(redis_key)
    if cached_value is not None:
        return json.loads(cached_value)
    else:
        return None


def get_keys():
    redis_instance = redis.StrictRedis(host='localhost', port='6379', db=1)
    return redis_instance.keys()


def clean_db():
    redis_instance = redis.Redis(host='localhost', port='6379', db=1)
    for key in get_keys():
        redis_instance.delete(key)