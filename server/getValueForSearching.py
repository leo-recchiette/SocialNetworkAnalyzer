#  coding: utf-8
#! /usr/bin/env python

import json
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

import dbConnector as dbc
graph = dbc.neo4jHelper()


def getFbValues(usr):
    range = []
    allTimestamps = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'facebook\']}) '
        'WHERE '
        ' exists (n.timestamp) '
        'RETURN n.timestamp AS timestamp ORDER BY n.timestamp ASC'
    ).data()

    nodeDegree = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'facebook\']}) '
        'WHERE '
        ' exists (n.nodeDegree) '
        'RETURN n.nodeDegree AS nodeDegree ORDER BY n.nodeDegree DESC limit 1'
    ).data()

    edgeDegree = graph.run(
        'MATCH ()-[n]-(m {graph_information: [\'' + usr + '\', \'facebook\']}) '
        'WHERE '
        ' exists (n.tagged_together) '
        'RETURN n.tagged_together AS edgeDegree ORDER BY n.tagged_together DESC limit 1'
    ).data()

    startDate = allTimestamps[0]['timestamp'].split()
    endDate = allTimestamps[len(allTimestamps) - 1]['timestamp'].split()

    try:
        range.append(startDate[0])
    except Exception as e:
        range.append(0)

    try:
        range.append(endDate[0])
    except Exception as e:
        range.append(0)

    try:
        range.append(nodeDegree[0]['nodeDegree'])
    except Exception as e:
        range.append(0)

    try:
        range.append(edgeDegree[0]['edgeDegree'])
    except Exception as e:
        range.append(0)

    return json.dumps(range)


def getTwValues(usr):
    range = []
    allTimestamps = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'twitter\']}) '
        'WHERE '
        ' exists (n.created_at) '
        'RETURN n.created_at AS timestamp ORDER BY n.created_at ASC'
    ).data()

    nodeDegree = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'twitter\']}) '
        'WHERE '
        ' exists (n.nodeDegree) '
        'RETURN n.nodeDegree AS nodeDegree ORDER BY n.nodeDegree DESC limit 1'
    ).data()

    edgeDegree = graph.run(
        'MATCH ()-[n]-(m {graph_information: [\'' + usr + '\', \'twitter\']}) '
        'WHERE '
        ' exists (n.tagged_together) '
        'RETURN n.tagged_together AS edgeDegree ORDER BY n.tagged_together DESC limit 1'
    ).data()

    try:
        startDate = allTimestamps[0]['timestamp'].split()
        endDate = allTimestamps[len(allTimestamps) - 1]['timestamp'].split()

        range.append(startDate[0])
        range.append(endDate[0])
        range.append(nodeDegree[0]['nodeDegree'])
        range.append(edgeDegree[0]['edgeDegree'])

        return json.dumps(range)
    except Exception as e:
        return "There aren't any dumps uploaded"


def getMboxValues(usr):
    range = []
    allTimestamps = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'mbox\']}) '
        'WHERE '
        ' exists (n.time) '
        'RETURN n.time AS timestamp ORDER BY n.time ASC'
    ).data()

    nodeDegree = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'mbox\']}) '
        'WHERE '
        ' exists (n.nodeDegree) '
        'RETURN n.nodeDegree AS nodeDegree ORDER BY n.nodeDegree DESC limit 1'
    ).data()

    edgeDegree = graph.run(
        'MATCH ()-[n]-(m {graph_information: [\'' + usr + '\', \'mbox\']}) '
        'WHERE '
        ' exists (n.edge_weight) '
        'RETURN n.edge_weight AS edgeDegree ORDER BY n.edge_weight DESC limit 1'
    ).data()

    try:
        startDate = allTimestamps[0]['timestamp'].split()
        endDate = allTimestamps[len(allTimestamps) - 1]['timestamp'].split()

        range.append(startDate[0])
        range.append(endDate[0])
        range.append(nodeDegree[0]['nodeDegree'])
        range.append(edgeDegree[0]['edgeDegree'])

        return json.dumps(range)
    except Exception as e:
        return "There aren't any dumps uploaded"


if __name__ == '__main__':

    usr = str(sys.argv[1])
    sn = str(sys.argv[2])

    if sn == 'facebook':
        print (getFbValues(usr))

    elif sn == 'twitter':
        print (getTwValues(usr))

    elif sn == 'mbox':
        print (getMboxValues(usr))
