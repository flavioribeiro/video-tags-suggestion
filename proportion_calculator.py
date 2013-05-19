#encoding: utf-8
import redis
import operator

from nltk.stem import RSLPStemmer

stemmer = RSLPStemmer()


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

    result = {}

    for term in terms:
        tags = api_get_tags(term)

        for tag in tags.keys():
            if tag in result:
                result[tag] += tags[tag]
            else:
                result[tag] = tags[tag]

    sorted_list = sorted(result.iteritems(), key=operator.itemgetter(1))
    sorted_list.reverse()
    return sorted_list


def tokenize_text(text):
    s = ' '.join([stemmer.stem(word) for word in text.split(' ')])

    return s.replace('\n', '')
