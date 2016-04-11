# -*- coding: utf-8 -*-

from __future__ import absolute_import

from math import sqrt

from utils import swap_data


def sim_distance(data, subject1, subject2):
    """Euclidean Distance"""
    shared_items = {item: 1
                    for item in data[subject1]
                    if item in data[subject2]}

    if len(shared_items) == 0:
        return 0

    sum_of_squares = sum([pow(data[subject1][item] - data[subject2][item], 2)
                          for item in shared_items])

    return 1/(1 + sqrt(sum_of_squares))


def sim_pearson(data, subject1, subject2):
    """Pearson Correlation Score"""
    shared_items = {item: 1
                    for item in data[subject1]
                    if item in data[subject2]}
    nitems = len(shared_items)
    if nitems == 0:
        return 0

    # sum data
    sum_subject1 = sum([data[subject1][item] for item in shared_items])
    sum_subject2 = sum([data[subject2][item] for item in shared_items])

    # sum squares
    sum_sq_subject1 = sum([pow(data[subject1][item], 2) for item in shared_items])
    sum_sq_subject2 = sum([pow(data[subject2][item], 2) for item in shared_items])

    # sum products
    sum_products = sum([data[subject1][item] * data[subject2][item]
                        for item in shared_items])

    num = sum_products - (sum_subject1 * sum_subject2 / nitems)
    den = sqrt((sum_sq_subject1 - pow(sum_subject1, 2) / nitems) *
               (sum_sq_subject2 - pow(sum_subject2, 2) / nitems))

    if den == 0:
        return 0

    return num / den


def sim_jaccard(data, subject1, subject2):
    """Tanimoto coefficient, useful when you want to know if two sets
    are similar

    http://mines.humanoriented.com/classes/2010/fall/csci568/portfolio_exports/sphilip/tani.html
    """
    shared_items = len({item: 1
                        for item in data[subject1]
                        if item in data[subject2]})
    total_items = len(data[subject1]) + len(data[subject2]) - shared_items
    return float(shared_items) / float(total_items)


def similar_items(data, n=10, similarity=sim_distance):
    result = {}
    c = 0
    items_data = swap_data(data)

    for item in items_data:
        c += 1
        if c % 100 == 0:
            print "{} / {}".format(c, len(items_data))
        result[item] = top_matches(items_data, item, n=n, similarity=similarity)

    return result


def top_matches(data, target, n=5, similarity=sim_pearson):
    scores = [(similarity(data, target, other), other) for other in data if other != target]
    scores.sort()
    scores.reverse()  # highest scores at the top
    return scores[0:n]


def recommendations(data, target, similarity=sim_pearson):
    print "Recommendations for {}:".format(target)
    totals = {}
    similarity_sums = {}

    for other in data:
        if other == target:
            continue

        score = similarity(data, target, other)
        if score <= 0:
            continue

        for item in data[other]:
            # only score items I haven't scored yet
            if item not in data[target] or data[target][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += data[other][item] * score
                similarity_sums.setdefault(item, 0)
                similarity_sums[item] += score

    rankings = [(total/similarity_sums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()

    return rankings


def recommended_items(data, items_data, target):
    print "Recommended Items for {}:".format(target)
    scores = {}
    similarity_sums = {}

    # Loop over items in the target
    for item, score in data[target].items():
        # Love over items similar to this one
        for similarity_score, other_item in items_data[item]:
            # Ignore if the other_item is in the target data
            if other_item in data[target]:
                continue
            scores.setdefault(other_item, 0)
            scores[other_item] += similarity_score * score

            similarity_sums.setdefault(other_item, 0)
            similarity_sums[other_item] += similarity_score

    rankings = [(score/similarity_sums[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()

    return rankings
