import pytest
import requests
import json
from proportion_calculator import redis_handler, get_tags, get_proportion, api_get_tags


def insert(term, tags):
    redis = redis_handler()
    total = 0
    for tag in tags.iteritems():
        redis.hset(term, tag[0], tag[1])
        total += tag[1]

    redis.set(term + ":count", total)

def test_calculator_should_get_all_tags_from_term():
    term = "neymar"
    insert(term=term, tags={"santos": 100, "futebol": 80, "dancinha": 10})

    assert {"santos": 100, "futebol": 80, "dancinha": 10} == get_tags(term)

def test_calculator_should_return_the_proportion_of_a_tag_for_term():
    term = "neymar"
    insert(term=term, tags={"santos": 100, "futebol": 80, "dancinha": 10})

    assert 0.5263157894736842 == get_proportion("santos", "neymar")
    assert 0.42105263157894735 == get_proportion("futebol", "neymar")
    assert 0.05263157894736842 == get_proportion("dancinha", "neymar")

def test_api_should_return_json_with_proportions_of_term():
    term = "neymar"
    insert(term=term, tags={"santos": 100, "futebol": 80, "dancinha": 10})
    result = api_get_tags(term)

    assert result == {"santos": 0.5263157894736842,"futebol": 0.42105263157894735, \
                     "dancinha": 0.05263157894736842}
