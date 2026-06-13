#  coding: utf-8
#! /usr/bin/env python

import json
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

import dbConnector as dbc
graph = dbc.neo4jHelper()


# The min-node-value / min-edge-value sliders should max out at what the CURRENT
# view actually shows. relNet draws people, trafficNet draws content; computing
# the max nodeDegree over *all* nodes let high-degree content nodes (Post,
# Tweet, ...) inflate the relNet slider far above the people's real max.
#
# Per (social network, graphType): the node labels drawn in that view (so the
# node-degree max is view-scoped), and the relationship type + weight property
# the min-edge-value slider bounds against.
NODE_LABELS = {
    ('facebook', 'relNet'):     ['Friend', 'RemovedFriend'],
    ('facebook', 'trafficNet'): ['Post', 'FriendPost', 'Comment', 'Direct_Message'],
    ('twitter', 'relNet'):      ['Follower', 'Following', 'BothFollowType'],
    ('twitter', 'trafficNet'):  ['Tweet', 'Retweet'],
    ('mbox', 'relNet'):         ['Undirected_Node'],
    ('mbox', 'trafficNet'):     ['Directed_Node'],
}

# (relationship type, weight property)
EDGE_WEIGHT = {
    ('facebook', 'relNet'):     ('TAGGED_TOGETHER', 'tagged_together'),
    ('facebook', 'trafficNet'): ('PUBLISHED', 'count'),
    ('twitter', 'relNet'):      ('TAGGED_TOGETHER', 'tagged_together'),
    ('twitter', 'trafficNet'):  ('TWEETED', 'count'),
    ('mbox', 'relNet'):         ('UNDIRECTED_EDGE', 'edge_weight'),
    ('mbox', 'trafficNet'):     ('DIRECTED_EDGE', 'edge_weight'),
}


def maxNodeDegree(usr, sn, graphType):
    labels = NODE_LABELS.get((sn, graphType))
    # Unknown graphType (e.g. map/wordFrec) -> no label scoping (global max).
    labelPred = ''
    if labels:
        labelPred = '(' + ' OR '.join('n:' + label for label in labels) + ') AND '
    return graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'' + sn + '\']}) '
        'WHERE ' + labelPred + ' exists(n.nodeDegree) '
        'RETURN n.nodeDegree AS nodeDegree ORDER BY n.nodeDegree DESC limit 1'
    ).data()


def maxEdgeWeight(usr, sn, graphType):
    edge = EDGE_WEIGHT.get((sn, graphType))
    if not edge:
        return []
    relType, prop = edge
    return graph.run(
        'MATCH ()-[r:' + relType + ']-(m {graph_information: [\'' + usr + '\', \'' + sn + '\']}) '
        'WHERE exists(r.' + prop + ') '
        'RETURN r.' + prop + ' AS edgeDegree ORDER BY r.' + prop + ' DESC limit 1'
    ).data()


def getFbValues(usr, graphType):
    range = []
    allTimestamps = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'facebook\']}) '
        'WHERE '
        ' exists (n.timestamp) '
        'RETURN n.timestamp AS timestamp ORDER BY n.timestamp ASC'
    ).data()

    nodeDegree = maxNodeDegree(usr, 'facebook', graphType)
    edgeDegree = maxEdgeWeight(usr, 'facebook', graphType)

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


def getTwValues(usr, graphType):
    range = []
    allTimestamps = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'twitter\']}) '
        'WHERE '
        ' exists (n.created_at) '
        'RETURN n.created_at AS timestamp ORDER BY n.created_at ASC'
    ).data()

    nodeDegree = maxNodeDegree(usr, 'twitter', graphType)
    edgeDegree = maxEdgeWeight(usr, 'twitter', graphType)

    try:
        startDate = allTimestamps[0]['timestamp'].split()
        endDate = allTimestamps[len(allTimestamps) - 1]['timestamp'].split()

        range.append(startDate[0])
        range.append(endDate[0])
        range.append(nodeDegree[0]['nodeDegree'] if nodeDegree else 0)
        range.append(edgeDegree[0]['edgeDegree'] if edgeDegree else 0)

        return json.dumps(range)
    except Exception as e:
        return "There aren't any dumps uploaded"


def getMboxValues(usr, graphType):
    range = []
    allTimestamps = graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\', \'mbox\']}) '
        'WHERE '
        ' exists (n.time) '
        'RETURN n.time AS timestamp ORDER BY n.time ASC'
    ).data()

    nodeDegree = maxNodeDegree(usr, 'mbox', graphType)
    edgeDegree = maxEdgeWeight(usr, 'mbox', graphType)

    try:
        startDate = allTimestamps[0]['timestamp'].split()
        endDate = allTimestamps[len(allTimestamps) - 1]['timestamp'].split()

        range.append(startDate[0])
        range.append(endDate[0])
        range.append(nodeDegree[0]['nodeDegree'] if nodeDegree else 0)
        range.append(edgeDegree[0]['edgeDegree'] if edgeDegree else 0)

        return json.dumps(range)
    except Exception as e:
        return "There aren't any dumps uploaded"


if __name__ == '__main__':

    usr = str(sys.argv[1])
    sn = str(sys.argv[2])
    # graphType scopes the node/edge maxima to the current view; default relNet
    # keeps older callers (that pass only usr + sn) working.
    graphType = str(sys.argv[3]) if len(sys.argv) > 3 else 'relNet'

    if sn == 'facebook':
        print (getFbValues(usr, graphType))

    elif sn == 'twitter':
        print (getTwValues(usr, graphType))

    elif sn == 'mbox':
        print (getMboxValues(usr, graphType))
