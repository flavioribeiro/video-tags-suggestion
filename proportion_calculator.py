import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

def redis_handler():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_tags(term):
    r = redis_handler()
    keys = r.hkeys(term)
    result = {}

    for key in keys:
        result[key] = int(r.hget(term, key))

    return result

def get_proportion(tag, term):
    r = redis_handler()
    total = int(r.get(term + ":count"))
    tag_count = r.hget(term, tag)

    return float(tag_count) / total

def api_get_tags(term):
    tags = get_tags(term)
    result = {}
    for tag in tags:
        result[tag] = get_proportion(tag, term)

    return result
