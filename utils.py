# -*- coding: utf-8 -*-

import json
import os
import random


def fixtures(name):
    with open('fixtures/{}.json'.format(name)) as data_file:
        data = json.loads(data_file.read())
    return data


def movies():
    basepath = 'fixtures/movies'
    movies = {}
    for line in open(os.path.join(basepath, 'item')):
        id, title = line.split('|')[0:2]
        movies[id] = title
    data = {}
    for line in open(os.path.join(basepath, 'data')):
        user, movieid, rating, ts = line.split('\t')
        data.setdefault(user, {})
        data[user][movies[movieid]] = float(rating)
    return data


def swap_data(data):
    new_data = {}
    for person in data:
        for item in data[person]:
            new_data.setdefault(item, {})
            new_data[item][person] = data[person][item]
    return new_data


def random_key(data):
    return data.keys()[random.randint(0, len(data) - 1)]
