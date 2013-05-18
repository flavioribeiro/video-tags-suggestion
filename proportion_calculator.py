#encoding: utf-8
import redis
import os
import operator

REDIS_HOST = "localhost"
REDIS_PORT = 6379

def redis_handler():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_tags(term):
    r = redis_handler()
    keys = r.hkeys('term:' + term)
    result = {}

    for key in keys:
        result[key] = int(r.hget('term:' + term, key))

    return result

def get_proportion(tag, term):
    r = redis_handler()
    total = int(r.get(term + ":count"))
    tag_count = r.hget('term:' + term, tag)

    return float(tag_count) / total

def api_get_tags(term):
    term = term.lower()
    tags = get_tags(term)
    result = {}
    for tag in tags:
        result[tag] = get_proportion(tag, term)

    return result

def api_get_merged_tags(text):
    terms = tokenize_text(text)
    terms = terms.split()

    print "Terms: " + str(terms)
    result = {}

    for term in terms:
        tags = api_get_tags(term)

        for tag in tags.keys():
            if result.has_key(tag):
                result[tag] += tags[tag]
            else:
                result[tag] = tags[tag]

    sorted_list = sorted(result.iteritems(), key=operator.itemgetter(1))
    sorted_list.reverse()
    return sorted_list

def tokenize_text(text):
    s = os.popen('java -jar /tmp/video-dump-1.0.0-SNAPSHOT-standalone.jar "' + str(text) + '"').read()

    return s.replace('\n', '')
