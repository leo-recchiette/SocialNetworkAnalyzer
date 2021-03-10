#  coding: utf-8

import json
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

paths = sys.path

for p in paths:
    if p == '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python':
        sys.path.remove(p)

sys.path.append('~/sna/server/')
import dbConnector as dbc
graph = dbc.neo4jHelper()

def getFbContent(word, start_date, end_date):
    return graph.run(
            'MATCH (w:Word)--(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
            'WHERE ' +
            ' exists (f.content) AND ' +
            ' w.word =\'' + word + '\' AND '
            ' (ANY(word IN split(f.content, \' \') WHERE word = w.word)) AND '                                   
            ' (f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') ' +
            'RETURN f as node, w.userProfileProperty as propertyDump'
        ).data()


def getTwContent(word, start_date, end_date):
    return graph.run(
        'MATCH (w:Word)--(f {graph_information:[\'' + usr + '\', \'twitter\']}) ' +
        'WHERE ' +
        ' exists (f.full_text) AND ' +
        ' w.word =\'' + word + '\' AND '
        ' ANY(word IN split(f.full_text, \' \') WHERE word = w.word ) AND '                               
        ' (f.created_at>\'' + start_date + '\' AND f.created_at<\'' + end_date + '\') ' +
        'RETURN f as node, w.userProfileProperty as propertyDump'
    ).data()


def getMboxContent(word, start_date, end_date):
    return graph.run(
        'MATCH (w:Word)--(m:Mail {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
        'WHERE ' +
        ' exists (m.content) AND ' +
        ' w.word =\'' + word + '\' AND '
        ' ANY(word IN split(m.content, \' \') WHERE word = w.word ) AND '                               
        ' (m.time>\'' + start_date + '\' AND m.time<\'' + end_date + '\') ' +
        'RETURN m as node, w.userProfileProperty as propertyDump'
    ).data()


data = str(sys.argv[1])
word = str(sys.argv[2])

if __name__ == '__main__':
    data = (json.loads(data))

    keyword = json.dumps(data['keyword']).replace('\"', '')
    person = json.dumps(data['person']).replace('\"', '')
    start_date = json.dumps(data['start_date']).replace('\"', '')
    end_date = json.dumps(data['end_date']).replace('\"', '')
    minNodevalue = json.dumps(data['minNodevalue']).replace('\"', '')
    minEdgeValue = json.dumps(data['minEdgeValue']).replace('\"', '')
    sn = json.dumps(data['sn']).replace('\"', '')
    graphType = json.dumps(data['graphType']).replace('\"', '')
    usr = json.dumps(data['usr']).replace('\"', '')
    dataViz1 = json.dumps(data['dataViz1']).replace('\"', '')
    dataViz2 = json.dumps(data['dataViz2']).replace('\"', '')
    sortValue = json.dumps(data['sortValue']).replace('\"', '')

    if sn == 'facebook':
        print json.dumps(getFbContent(word, start_date, end_date))
    elif sn == 'twitter':
        print json.dumps(getTwContent(word, start_date, end_date))
    elif sn == 'mbox':
        print json.dumps(getMboxContent(word, start_date, end_date))

