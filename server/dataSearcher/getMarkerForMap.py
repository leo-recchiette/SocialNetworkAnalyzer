#  coding: utf-8
#! /usr/bin/env python

import json
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

sys.path.append('~/sna/server/')
import dbConnector as dbc
graph = dbc.neo4jHelper()

##########  FACEBOOK MAP ##########

def getMarkersForFacebook(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, markersToDisplay):
    if markersToDisplay == 'all':
        if keyword != '' and person != '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword != '' and person == '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword == '' and person != '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword == '' and person == '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
    elif markersToDisplay == 'geoTag':
        if keyword != '' and person != '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword != '' and person == '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword == '' and person != '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword == '' and person == '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
    elif markersToDisplay == 'post':
        if keyword != '' and person != '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + keyword + '.*\') OR  '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword != '' and person == '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword == '' and person != '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()
        elif keyword == '' and person == '':
            return graph.run(
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN p '
            ).data()

##########  TWITTER MAP ##########

def getMarkersForTwitter(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    if keyword != '' and person != '':
        return graph.run(
            'MATCH (n:Tweet) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' AND '
            ' ANY(u IN n.user_mentions WHERE u =~ \'(?ism).*' + person + '.*\') AND '
            ' (n.full_text =~ \'(?ism).*' + keyword + '.*\' OR '
            ' n.hashtags_text =~ \'(?ism).*' + keyword + '.*\' '                                        
            'RETURN n as place '
        ).data()

    elif keyword != '' and person == '':
        return graph.run(
            'MATCH (n:Tweet) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' AND '
            ' n.full_text =~ \'(?ism).*' + keyword + '.*\' OR '
            ' n.hashtags_text =~ \'(?ism).*' + keyword + '.*\' '                                                                                       
            'RETURN n as place '
        ).data()

    elif keyword == '' and person != '':
        return graph.run(
            'MATCH (n:Tweet) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' AND '
            ' ANY(u IN n.user_mentions WHERE u =~ \'(?ism).*' + person + '.*\' '                                                                        
            'RETURN n as place '
        ).data()

    elif keyword == '' and person == '':
        return graph.run(
            'MATCH (n:Tweet) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' '
            'RETURN n as place '
        ).data()


data = str(sys.argv[1])

if __name__ == '__main__':
    data = (json.loads(data))

    keyword = json.dumps(data['keyword']).replace('\"','')
    person = json.dumps(data['person']).replace('\"', '')
    start_date = json.dumps(data['start_date']).replace('\"', '')
    end_date = json.dumps(data['end_date']).replace('\"', '')
    minNodevalue = json.dumps(data['minNodevalue']).replace('\"', '')
    minEdgeValue = json.dumps(data['minEdgeValue']).replace('\"', '')
    sn = json.dumps(data['sn']).replace('\"','')
    graphType = json.dumps(data['graphType']).replace('\"','')
    usr = json.dumps(data['usr']).replace('\"', '')
    dataViz1 =  json.dumps(data['dataViz1']).replace('\"', '')
    dataViz2 = json.dumps(data['dataViz2']).replace('\"', '')

    if sn == 'facebook':
        markersToDisplay = str(sys.argv[2])

        print (json.dumps(getMarkersForFacebook(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, markersToDisplay)))
    elif sn == 'twitter':
        print (json.dumps(getMarkersForTwitter(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)))

