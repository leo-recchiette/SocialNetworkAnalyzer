#  coding: utf-8
#! /usr/bin/env python

import json
import sys

sys.path.append('~/anaconda2/envs/sna_temp/lib/python2.7/site-packages')

sys.path.append('~/sna/server/')
import dbConnector as dbc
graph = dbc.neo4jHelper()

##########  SELECTED CONTACTS ##########

def getSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, id ):
    if sn=='facebook':
        return getFacebookSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id)
    elif sn=='twitter':
        return getTwitterSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id)
    elif sn == 'mbox':
        return getMboxSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id)


def getFacebookSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id):
    if graphType == 'relNet':
        return getFacebookSelectedContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'trafficNet':
        return getFacebookSelectedContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)


def getFacebookSelectedContactsForRelationshipNetwork (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):

    if (id !='All' and id !='Friend' and id!='remFriend'):
        return graph.run(
            'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
            'MATCH (n)--(u:fbUser) '
            'WHERE '
            ' ID(n) = ' + id + ' '
            'OPTIONAL MATCH (n)-[s:TAGGED_TOGETHER]-(d) '
            'WHERE '
            's.tagged_together >= ' + minEdgeValue + ' AND '
            ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
            '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
            ' d.nodeDegree>=' + minNodevalue + ' '
            'OPTIONAL MATCH (n)-[r:FRIEND]-(f) '
            'WHERE '
            ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
            '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
            ' f.nodeDegree>=' + minNodevalue + ' '
            'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as taggedTogetherValue, count(r) AS fbUserNodeDegree, u.name AS propertyDump'
        ).data()
    else:
        if (id=='All'):
            if keyword != '' and person != '':
                return graph.run(
                    'MATCH (p)-[r]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                     '(type(r)=\'TAG\' or type(r)=\'PUBLISHED\') AND '                                                                      
                    ' f.name=~ \'(?i).*' + person + '.*\' AND '
                    ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' 
                    ' (f:Friend or f:RemovedFriend or f:DM_Participant) AND '
                    ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                    '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter').data()
            elif keyword != '' and person == '':
                return graph.run(
                    'MATCH (p)-[r]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    '(type(r)=\'TAG\' or type(r)=\'PUBLISHED\') AND '
                    ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND '
                    ' (f:Friend or f:RemovedFriend) AND '
                    ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                    '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter').data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' f.name=~ \'(?i).*' + person + '.*\' AND '
                    ' (f:Friend or f:RemovedFriend) AND '
                    ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                    '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter').data()
            elif keyword == '' and person == '':
                return graph.run(
                    'MATCH (f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' (f:Friend or f:RemovedFriend) AND '
                    ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                    '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter'
                ).data()
        elif (id=='Friend'):
            if keyword != '' and person != '':
                return graph.run(
                    'MATCH (f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' f.name=~ \'(?i).*' + person + '.*\' AND '
                    ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND '
                    ' (f.timestamp>=\'' + start_date + '\' AND f.timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter').data()
            elif keyword != '' and person == '':
                return graph.run(
                    'MATCH (f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND '
                    ' (f.timestamp>=\'' + start_date + '\' AND f.timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter').data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' f.name=~ \'(?i).*' + person + '.*\' AND '
                    ' (f.timestamp>=\'' + start_date + '\' AND f.timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter').data()
            elif keyword == '' and person == '':
                return graph.run(
                    'MATCH (f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' (f.timestamp>=\'' + start_date + '\' AND f.timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter'
                ).data()
        else:
            if keyword != '' and person != '':
                return graph.run(
                    'MATCH (f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' f.name=~ \'(?i).*' + person + '.*\' AND '
                    ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND '
                    ' (f.removed_timestamp>=\'' + start_date + '\' AND f.removed_timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter'
                ).data()
            elif keyword != '' and person == '':
                return graph.run(
                    'MATCH (f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND '                                                                            
                    ' (f.removed_timestamp>=\'' + start_date + '\' AND f.removed_timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter'
                ).data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' f.name=~ \'(?i).*' + person + '.*\' AND '                                                                            
                    ' (f.removed_timestamp>=\'' + start_date + '\' AND f.removed_timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter'
                ).data()
            elif keyword == '' and person == '':
                return graph.run(
                    'MATCH (f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' (f.removed_timestamp>=\'' + start_date + '\' AND f.removed_timestamp<=\'' + end_date + '\') AND '
                    ' f.nodeDegree>=' + minNodevalue + ' '
                    'RETURN count(f) As Counter'
                ).data()


def getFacebookSelectedContactsForTrafficNetwork (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    if (id != 'all' and id != 'post' and id != 'friendPost' and id != 'comment' and id != 'dm' ):
        nodeType = graph.run(
            'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
            'WHERE '
            ' ID(n) = ' + id + ' '
            'RETURN labels(n) AS nodeType'
        ).data()[0]['nodeType'][0]

        if nodeType != 'Direct_Message':
            return graph.run(
                'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (n)--(u:fbUser) '                                                          
                'WHERE '
                ' ID(n) = ' + id + ' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'OPTIONAL MATCH (n)-[r:PUBLISHED]-(f) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, count(r) AS fbUserNodeDegree, u.name AS propertyDump '
            ).data()
        else:
            return graph.run(
                'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (n)--(u:fbUser) '                                                         
                'WHERE '
                ' ID(n) = ' + id + ' '
                'OPTIONAL MATCH x=(n)<-[:REPLAY*]-(r) '
                'WHERE '
                'r.timestamp>\'' + start_date + '\' AND r.timestamp<\'' + end_date + '\' '                   
                'RETURN n AS StartOfConversation, u.name AS propertyDump, r AS Replay ORDER by r.timestamp ASC'
            ).data()
    else:
        if (id =='all'):
            if keyword != '' and person !=  '':
                return graph.run(
                    'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' 
                    ' n.content CONTAINS \''+keyword+'\' ) AND ' 
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' 
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' 
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' 
                    ' (n:FriendPost or n:Post or n:Comment or n:Direct_Message) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND ' 
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter').data()
            elif keyword != '' and person ==  '':
                return graph.run(
                    'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' 
                    ' n.content CONTAINS \''+keyword+'\' ) AND ' 
                    ' (n:FriendPost or n:Post or n:Comment or n:Direct_Message) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND ' 
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter').data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR '
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  '
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND '
                    ' (n:FriendPost or n:Post or n:Comment or n:Direct_Message) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter').data()
            elif keyword == '' and person ==  '':
                return graph.run(
                    'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (n:FriendPost or n:Post or n:Comment or n:Direct_Message) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND ' 
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
        elif (id =='post'):
            if keyword != '' and person !=  '':
                return graph.run(
                    'MATCH (n:Post {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' 
                    ' n.content CONTAINS \''+keyword+'\' ) AND ' 
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' 
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' 
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' 
                    ' n.nodeDegree>=' + minNodevalue + ' AND '                                                                    
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword != '' and person ==  '':
                return graph.run(
                    'MATCH (n:Post {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' 
                    ' n.content CONTAINS \''+keyword+'\' ) AND '                                                                    
                    ' n.nodeDegree>=' + minNodevalue + ' AND ' 
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                    ).data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (n:Post {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' 
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' 
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND '                                                                    
                    ' n.nodeDegree>=' + minNodevalue + ' AND ' 
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                    ).data()
            elif keyword == '' and person ==  '':
                return graph.run(
                    'MATCH (n:Post {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '                                                                    
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
        elif (id =='friendPost'):
            if keyword != '' and person != '':
                return graph.run(
                    'MATCH (n:FriendPost {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                    ' n.content CONTAINS \'' + keyword + '\' ) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR '
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  '
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                    ).data()
            elif keyword != '' and person == '':
                return graph.run(
                    'MATCH (n:FriendPost {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                    ' n.content CONTAINS \'' + keyword + '\' ) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (n:FriendPost {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR '
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  '
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword == '' and person == '':
                return graph.run(
                    'MATCH (n:FriendPost {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
        elif (id =='comment'):
            if keyword != '' and person != '':
                return graph.run(
                    'MATCH (n:FriendPost {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                    ' n.content CONTAINS \'' + keyword + '\' ) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR '
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  '
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword != '' and person == '':
                return graph.run(
                    'MATCH (n:Comment {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                    ' n.content CONTAINS \'' + keyword + '\' ) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (n:Comment {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?i).*' + person + '.*\') OR '
                    ' ANY(title IN n.title WHERE title =~ \'(?i).*' + person + '.*\') OR  '
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword == '' and person == '':
                return graph.run(
                    'MATCH (n:Comment {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' n.nodeDegree>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
        else:
            if keyword != '' and person != '':
                return graph.run(
                    'MATCH (n:Direct_Message {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                    ' n.content CONTAINS \'' + keyword + '\' ) AND '
                    ' ANY(participant IN n.participants WHERE participant =~ \'(?ism).*' + person + '.*\') AND '                                     
                    ' length(n.participants)>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword != '' and person == '':
                return graph.run(
                    'MATCH (n:Direct_Message {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                    ' n.content CONTAINS \'' + keyword + '\' ) AND '                                                                                                 
                    ' length(n.participants)>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword == '' and person != '':
                return graph.run(
                    'MATCH (n:Direct_Message {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' ANY(participant IN n.participants WHERE participant =~ \'(?ism).*' + person + '.*\') AND '                                                                             
                    ' length(n.participants)>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()
            elif keyword == '' and person == '':
                return graph.run(
                    'MATCH (n:Direct_Message {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' exists (n.timestamp) AND '
                    ' length(n.participants)>=' + minNodevalue + ' AND '
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'RETURN count(n) AS Counter'
                ).data()


def getFacebookPlace(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, lat, lng):
    if ((lat != 'all' and lng != 'all')  and (lat != 'post' and lng != 'post') and (lat != 'geoTag' and lng != 'geoTag')):
        return graph.run(
            'MATCH (p {graph_information:[\'' + usr + '\', \''+ sn +'\']})--(u:fbUser) ' +
            'WHERE ' 
            ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
            ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
            ' p.place_latitude CONTAINS \''+ lat +'\' AND p.place_longitude CONTAINS \''+ lng +'\' AND' 
            ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
            ' RETURN p AS place, u.name AS propertyDump'
        ).data()
    else:
        if (lat == 'all' and lng == 'all'):
            return graph.run(
                'MATCH (p {graph_information:[\'' + usr + '\', \'' + sn + '\']})--(u:fbUser) ' +
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN count(p) AS Counter'
            ).data()
        elif(lat == 'post' and lng == 'post'):
            return graph.run(
                'MATCH (p:Post {graph_information:[\'' + usr + '\', \'' + sn + '\']})--(u:fbUser) ' +
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN count(p) AS Counter'
            ).data()
        else:
            return graph.run(
                'MATCH (p:Place {graph_information:[\'' + usr + '\', \'' + sn + '\']})--(u:fbUser) ' +
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN count(p) AS Counter'
            ).data()


def getTwitterSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id):
    if graphType == 'relNet':
        return getTwitterSelectedContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'trafficNet':
        return getTwitterSelectedContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)


def getTwitterSelectedContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):

    if (id!='All' and id!='follower' and id!='following'):
        return graph.run(
            'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})--(f) ' +
            'WHERE ' +
            'ID(f) = ' + id + ' AND '
            ' exists(f.firstInteration) AND ' +
            ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
            ' f.nodeDegree>=' + minNodevalue + ' ' +
            'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
            'WHERE '
            ' s.tagged_together>=' + minEdgeValue + ' AND ' +
            ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
            ' d.nodeDegree>=' + minNodevalue + ' '
            'RETURN u.username AS propertyDump, collect(distinct d.screen_name) AS taggedWith, count(s) AS taggedTogetherValue, f AS node '
        ).data()
    else:
        if (id=='All'):
            return graph.run(
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})--(f) ' +
                'WHERE ' +
                ' (f:BothFollowType or f:Following or f:Follower) AND '
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN count(f) as Counter '
             ).data()
        elif(id=='follower'):
            return graph.run(
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})--(f:Follower) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN count(f) as Counter '
            ).data()
        elif (id == 'following'):
            return graph.run(
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})--(f:Following) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN count(f) as Counter '
            ).data()


def getTwitterSelectedContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    if (id != 'all' and id != 'tweet' and id != 'retweet'):
        return graph.run(
            'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t) '
            'WHERE '
            'ID(t)='+ id +' AND '
            ' t.nodeDegree>= ' + minNodevalue + ' AND '
            ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
            'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(d) '
            'RETURN t AS node, collect(d.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
        ).data()
    else:
        if (id != 'all'):
            return graph.run(
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t) '
                'WHERE '
                ' (t:Tweet or t:Retweet) AND '
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(d) '
                'RETURN count(t) AS Counter'
            ).data()
        elif(id != 'tweet'):
            return graph.run(
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Tweet) '
                'WHERE '
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(d) '
                'RETURN count(t) AS Counter'
            ).data()
        elif( id != 'retweet'):
            return graph.run(
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Retweet) '
                'WHERE '
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(d) '
                'RETURN count(t) AS Counter'
            ).data()


def getTwitterPlace( keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, lat, lng ):
    if (lat !=0 and lng !=0):
        return graph.run(
            'MATCH (u:twUser)--(n:Tweet {graph_information:[\'' + usr + '\', \'twitter\']}) '
            'WHERE n.latitude CONTAINS \''+ lat +'\' AND n.longitude CONTAINS \''+lng+'\' '
            'RETURN n as place, u.username AS propertyDump '
        ).data()
    else:
        return graph.run(
            'MATCH (u:twUser)--(n:Tweet {graph_information:[\'' + usr + '\', \'twitter\']}) '
            'WHERE exists(n.latitude) AND exists(n.longitude) AND '
            ' not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' '
            'RETURN count(n) AS Counter '
        ).data()



def getMboxSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id):
    if graphType == 'relNet':
        return getMboxSelectedContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'trafficNet':
        return getMboxSelectedContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)


def getMboxSelectedContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    if (id != 'All'):
        return graph.run(
            'MATCH (n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
            'WHERE '
            ' ID(n) = ' + id +' AND '
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND '
            ' r.edge_weight>' + minEdgeValue + ' '
            'RETURN n AS node, count(r) AS taggedTogetherValue, collect(distinct p.label) AS taggedWith'
        ).data()
    else:
        return graph.run(
            'MATCH (n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
            'WHERE '
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND '
            ' r.edge_weight>' + minEdgeValue + ' '
            'RETURN count(n) AS Counter'
        ).data()


def getMboxSelectedContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):

    if (id == 'All'):
        return graph.run(
            'MATCH (n:Mail)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
            'WHERE '
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND '
            ' r.edge_weight>' + minEdgeValue + ' '
            'RETURN count(n) AS Counter'
        ).data()
    else:
        return graph.run(
            'MATCH (n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
            'WHERE '
            ' ID(n) = ' + id + ' AND '
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND '
            ' r.edge_weight>' + minEdgeValue + ' '
            'RETURN n AS node, count(r) AS taggedTogetherValue, collect(distinct p.label) AS taggedWith'
        ).data()


def getMboxPlace ():
    print (2)


#################   FILTERED CONTACTS #########################


def getFilteredContacts (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, sortValue, ntd):
    if sn=='facebook':
        return getFacebookFilteredContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue, ntd)
    elif sn=='twitter':
        return getTwitterFilteredContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue, ntd)
    elif sn == 'mbox':
        return getMboxFilteredContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue)


def getFacebookFilteredContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue, ntd):
    if graphType == 'relNet':
        return getFacebookFilteredContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd)
    elif graphType == 'trafficNet':
        return getFacebookFilteredContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd)
    elif graphType == 'map':
        return getFacebookFilteredContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd)
    elif graphType == 'wordFrec':
        return getFacebookFilteredContactsForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd)


def getFacebookFilteredContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd):
    query = ''
    if ntd =='All':
        if keyword != '' and person != '':
            query = ('MATCH (u:fbUser)--(p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' 
                ' p.content CONTAINS \''+keyword+'\' ) AND ' 
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + person + '.*\') OR ' 
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' 
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' 
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' 
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' 
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword != '' and person == '':
            query = ('MATCH (u:fbUser)--(p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' AND '                                                                                      
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' 
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' 
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword == '' and person != '':
            query = ('MATCH (n)-[r:FRIEND]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (f)--(u:fbUser) '
                'WHERE '
                ' f.name=~ \'(?ism).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword=='' and person=='':
            query = ('MATCH (n)-[r:FRIEND]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (f)--(u:fbUser) '                                                                 
                'WHERE '
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '                                   
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
    if ntd =='Friend':
        if keyword != '' and person != '':
            query = ('MATCH (u:fbUser)--(p)-[:TAG]-(f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' AND '                                                                                             
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' f.name=~ \'(?ism).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword != '' and person == '':
            query = ('MATCH (u:fbUser)--(p)-[:TAG]-(f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' AND '                                                                                             
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword == '' and person != '':
            query = ('MATCH (n)-[r:FRIEND]-(f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (f)--(u:fbUser) '
                'WHERE '
                ' f.name=~ \'(?ism).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword=='' and person=='':
            query = ('MATCH (n)-[r:FRIEND]-(f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (f)--(u:fbUser) '                                                                 
                'WHERE '
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '                                   
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
    if ntd =='remFriend':
        if keyword != '' and person != '':
            query = ('MATCH (u:fbUser)--(p)-[:TAG]-(f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' AND '                                                                                                    
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' f.name=~ \'(?ism).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword != '' and person == '':
            query = ('MATCH (u:fbUser)--(p)-[:TAG]-(f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' AND '                                                                                                    
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword == '' and person != '':
            query = ('MATCH (n)-[r:FRIEND]-(f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (f)--(u:fbUser) '
                'WHERE '
                ' f.name=~ \'(?ism).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')
        elif keyword=='' and person=='':
            query = ('MATCH (n)-[r:FRIEND]-(f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (f)--(u:fbUser) '                                                                 
                'WHERE '
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR '
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND '
                ' f.nodeDegree>=' + minNodevalue + ' '
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR '
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND '
                ' d.nodeDegree>=' + minNodevalue + ' '                                   
                'RETURN u.name AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by ')

    if sortValue == 'timedesc':
        query = query + 'f.timestamp DESC'
    elif sortValue == 'timeasc':
        query = query + 'f.timestamp ASC'
    elif sortValue == 'name':
        query = query + 'f.name ASC'
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC'
    elif sortValue == 'degree':
        query = query + 'f.nodeDegree DESC'

    return graph.run( query ).data()


def getFacebookFilteredContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd):
    query = ''

    if ntd == 'all':
        if keyword != '' and person != '':
            query = (
                'MATCH (n)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (n)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (n)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (n)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '                                                          
                'WHERE '
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
    elif ntd == 'post':
        if keyword != '' and person != '':
            query = (
                    'MATCH (n:Post)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                    'WHERE '
                    ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                    ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                    ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                    ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                    ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                    ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                    'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                    'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (n:Post)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (n:Post)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (n:Post)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
    elif ntd == 'friendPost':
        if keyword != '' and person != '':
            query = (
                'MATCH (n:FriendPost)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (n:FriendPost)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (n:FriendPost)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (n:FriendPost)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
    elif ntd =='comment':
        if keyword != '' and person != '':
            query = (
                'MATCH (n:Comment)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (n:Comment)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (n:Comment)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (n:Comment)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
    elif ntd =='dm':
        if keyword != '' and person != '':
            query = (
                'MATCH (n:Direct_Message)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (n:Direct_Message)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' ANY(content IN n.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND  ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (n:Direct_Message)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' (ANY(content IN n.content WHERE content =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(title IN n.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  ' +
                ' ANY(tags IN n.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND ' +
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (n:Direct_Message)-[:PUBLISHED]-(u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' n.nodeDegree>=' + minNodevalue + ' AND ' +
                ' n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\' '
                'OPTIONAL MATCH (n)-[s:TAG]-(d) '
                'RETURN n AS node, collect(d.name) AS taggedWith, count(s) as nodeDegree, u.name AS propertyDump '
            )

    if sortValue == 'timedesc':
        query = query + ' ORDER BY n.timestamp DESC'
    elif sortValue == 'timeasc':
        query = query + ' ORDER BY n.timestamp ASC'
    elif sortValue == 'degree':
        query = query + ' ORDER BY n.nodeDegree DESC'

    return graph.run(query).data()


def getFacebookFilteredContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd):
    query = ''
    if ntd == 'all':
        if  keyword != '' and person != '':
            query = (
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
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword=='' and person == '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY  '
            )
    if ntd == 'geoTag':
        if  keyword != '' and person != '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
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
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword=='' and person == '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Place) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY  '
            )
    if ntd == 'post':
        if  keyword != '' and person != '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
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
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword != '' and person == '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR '
                ' p.name =~ \'(?ism).*' + keyword + '.*\' OR p.place_address=~ \'(?ism).*' + keyword + '.*\' OR '
                ' p.place_name=~ \'(?ism).*' + keyword + '.*\') AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' (ANY(post IN p.post WHERE post =~ \'(?ism).*' + person + '.*\') OR '
                ' ANY(title IN p.title WHERE title =~ \'(?ism).*' + person + '.*\') OR  '
                ' ANY(tags IN p.tags WHERE tags =~ \'(?ism).*' + person + '.*\')) AND '
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY '
            )
        elif keyword=='' and person == '':
            query = (
                'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p:Post) '
                'WHERE '
                ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
                ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' AND'
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' '
                'RETURN u.name AS propertyDump, p AS place ORDER BY  '
            )

    if sortValue == 'timedesc':
        query = query + 'p.timestamp DESC'
    elif sortValue == 'timeasc':
        query = query + 'p.timestamp ASC'
    elif sortValue == 'name':
        query = query + 'p.name ASC'
    elif sortValue == 'degree':
        query = query + 'p.nodeDegree DESC'

    return graph.run(query).data()


def getFacebookFilteredContactsForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd):
    return graph.run(
                'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']})<-[:WORD]-(w:Word {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'WHERE '
                ' exists(n.content) AND '
                ' (n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\') ' +
                'RETURN  w.word as word, toFloat(w.value) as value ORDER BY value DESC LIMIT 100 '
            ).data()

def getTwitterFilteredContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue, ntd):
    if graphType == 'relNet':
        return getTwitterFilteredContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd)
    elif graphType == 'trafficNet':
        return getTwitterFilteredContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd)
    elif graphType == 'map':
        return getTwitterFilteredContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd)
    else:
        return getTwitterFilteredContactsForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)


def getTwitterFilteredContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd):
    query = ''
    if ntd =='All':
        if keyword != '' and person != '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})--(f)-[:TAGGED_IN]-(t) ' +
                'WHERE ' +
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        if keyword != '' and person == '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})--(f)-[:TAGGED_IN]-(t) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})--(f) ' +
                'WHERE ' +
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})--(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
    if ntd =='follower':
        if keyword != '' and person != '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f)-[:TAGGED_IN]-(t) ' +
                'WHERE ' +
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        if keyword != '' and person == '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f)-[:TAGGED_IN]-(t) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:FOLLOW]-(f) ' +
                'WHERE ' +
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
    if ntd =='following':
        if keyword != '' and person != '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f)-[:TAGGED_IN]-(t) ' +
                'WHERE ' +
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        if keyword != '' and person == '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f)-[:TAGGED_IN]-(t) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        elif keyword == '' and person != '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:FOLLOWING]-(f) ' +
                'WHERE ' +
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
                'WHERE '
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND '
                ' d.nodeDegree>=' + minNodevalue + ' '          
                'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
            )

    if sortValue == 'timedesc':
        query = query + 'f.firstInteration DESC'
    elif sortValue == 'timeasc':
        query = query + 'f.firstInteration ASC'
    elif sortValue == 'name':
        query = query + 'f.name '
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC '
    elif sortValue == 'degree':
        query = query + 'f.nodeDegree DESC '

    return graph.run(query).data()


def getTwitterFilteredContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd):
    query = ''

    if ntd=='all':
        if keyword != '' and person != '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        if keyword != '' and person == '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        if keyword == '' and person != '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
    if ntd=='tweet':
        if keyword != '' and person != '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Tweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        if keyword != '' and person == '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Tweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        if keyword == '' and person != '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Tweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Tweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
    if ntd=='retweet':
        if keyword != '' and person != '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Retweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        if keyword != '' and person == '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Retweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        if keyword == '' and person != '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Retweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' (f.name=~ \'(?ism).*' + person + '.*\' OR f.screen_name=~ \'(?ism).*' + person + '.*\') AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )
        elif keyword == '' and person == '':
            query = (
                'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t:Retweet) '
                'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
                'WITH u,t,f,s '
                'WHERE '
                ' t.nodeDegree>= ' + minNodevalue + ' AND '
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' '
                'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
            )

    if sortValue == 'timedesc':
        query = query + ' ORDER BY t.created_at DESC'
    elif sortValue == 'timeasc':
        query = query + ' ORDER BY t.created_at ASC'
    elif sortValue == 'degree':
        query = query + ' ORDER BY t.nodeDegree DESC'

    return graph.run(query).data()


def getTwitterFilteredContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, ntd):
    query = ''

    if keyword != '' and person != '':
        query = (
            'MATCH (u:twUser)--(n:Tweet {graph_information:[\'' + usr + '\', \'twitter\']}) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' AND '
            ' ANY(u IN n.user_mentions WHERE u =~ \'(?ism).*' + person + '.*\') AND '
            ' (n.full_text =~ \'(?ism).*' + keyword + '.*\' OR '
            ' n.hashtags_text =~ \'(?ism).*' + keyword + '.*\' '                                        
            'RETURN n as place, u.username AS propertyDump ORDER BY '
        )
    if keyword != '' and person == '':
        query = (
            'MATCH (u:twUser)--(n:Tweet {graph_information:[\'' + usr + '\', \'twitter\']}) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' AND '
            ' n.full_text =~ \'(?ism).*' + keyword + '.*\' OR '
            ' n.hashtags_text =~ \'(?ism).*' + keyword + '.*\' '                                                                                       
            'RETURN n as place, u.username AS propertyDump ORDER BY '
        )
    elif keyword == '' and person != '':
        query = (
            'MATCH(u:twUser)--(n:Tweet {graph_information:[\'' + usr + '\', \'twitter\']}) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' AND '
            ' ANY(u IN n.user_mentions WHERE u =~ \'(?ism).*' + person + '.*\' '                                                                        
            'RETURN n as place, u.username AS propertyDump ORDER BY '
        )
    elif keyword == '' and person == '':
        query = (
            'MATCH (u:twUser)--(n:Tweet {graph_information:[\'' + usr + '\', \'twitter\']}) '
            'WHERE not n.latitude = \'\' AND not n.longitude = \'\' AND '
            ' n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\' '
            'RETURN n as place, u.username AS propertyDump ORDER BY '
        )

    if sortValue == 'timedesc':
        query = query + ' n.created_at DESC'
    elif sortValue == 'timeasc':
        query = query + ' n.created_at ASC '
    elif sortValue == 'degree':
        query = query + ' n.nodeDegree DESC '

    return graph.run(query).data()


def getTwitterFilteredContactsForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    return graph.run(
        'MATCH (n {graph_information:[\'' + usr + '\', \'twitter\']})<-[:WORD]-(w:Word {graph_information:[\'' + usr + '\', \'twitter\']}) '
        'WHERE '
        ' exists(n.full_text) AND '
        ' (n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\') ' +
        'RETURN  w.word as word, toFloat(w.value) as value ORDER BY value DESC LIMIT 100 '
    ).data()


def getMboxFilteredContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue):
    if graphType == 'relNet':
        return getMboxFilteredContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'trafficNet':
        return getMboxFilteredContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'map':
        return getMboxFilteredContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue, sortValue)
    else:
        return getMboxFilteredForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)


def getMboxFilteredContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    query = ''

    if keyword != '' and person != '':
        query = (
            'MATCH (m:Mail {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' (m.subject =~\'(?ism).*' + keyword + '.*\' OR m.content =~\'(?ism).*' + keyword + '.*\') AND ' +
            ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
            'MATCH (n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
            ' n.label  =~\'(?ism).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )
    if keyword != '' and person == '':
        query = (
                'MATCH (m:Mail {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
                'WHERE ' +
                ' (m.subject =~\'(?ism).*' + keyword + '.*\' OR m.content =~\'(?ism).*' + keyword + '.*\') AND ' +
                ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
                'MATCH x=(n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
                'WHERE ' +
                ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
                ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
                ' r.edge_weight>' + minEdgeValue + ' ' +
                'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )
    elif keyword == '' and person != '':
        query = (
            'MATCH x=(n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.label  =~\'(?ism).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )
    elif keyword == '' and person == '':
        query = (
            'MATCH (n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
            'WHERE '
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND '
            ' r.edge_weight>' + minEdgeValue + ' '
            'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )

    if sortValue == 'timedesc':
        query = query + 'n.firstInteration DESC'
    elif sortValue == 'timeasc':
        query = query + 'n.firstInteration ASC'
    elif sortValue == 'name':
        query = query + 'n.label ASC'
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC'
    elif sortValue == 'degree':
        query = query + 'n.nodeDegree DESC'

    return graph.run( query ).data()


def getMboxFilteredContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    query = ''

    if keyword != '' and person != '':
        query = (
            'MATCH (m:Mail {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' (m.subject =~\'(?ism).*' + keyword + '.*\' OR m.content =~\'(?ism).*' + keyword + '.*\') AND ' +
            ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
            'MATCH (n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
            ' n.label  =~\'(?ism).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )
    if keyword != '' and person == '':
        query = (
                'MATCH (m:Mail {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
                'WHERE ' +
                ' (m.subject =~\'(?ism).*' + keyword + '.*\' OR m.content =~\'(?ism).*' + keyword + '.*\') AND ' +
                ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
                'MATCH x=(n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
                'WHERE ' +
                ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
                ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
                ' r.edge_weight>' + minEdgeValue + ' ' +
                'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )
    elif keyword == '' and person != '':
        query = (
            'MATCH x=(n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.label  =~\'(?ism).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )
    elif keyword == '' and person == '':
        query = (
            'MATCH (n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
            'WHERE '
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND '
            ' r.edge_weight>' + minEdgeValue + ' '
            'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
        )

    if sortValue == 'timedesc':
        query = query + 'n.firstInteration DESC'
    elif sortValue == 'timeasc':
        query = query + 'n.firstInteration ASC'
    elif sortValue == 'name':
        query = query + 'n.label ASC'
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC'
    elif sortValue == 'degree':
        query = query + 'n.nodeDegree DESC'

    return graph.run(query).data()


def getMboxFilteredForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    return graph.run(
        'MATCH (n:Mail {graph_information:[\'' + usr + '\', \'mbox\']})<-[:WORD]-(w:Word {graph_information:[\'' + usr + '\', \'mbox\']} ) '
        'WHERE '
        ' n.time > \'' + start_date + '\' AND n.time < \'' + end_date + '\' '
        'RETURN DISTINCT w.word as word, toFloat(w.value) as value ORDER BY value DESC LIMIT 100 '
    ).data()


##################  ALL CONTACTS #########################

def getAllContacts (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, sortValue):
    if sn=='facebook':
        return getFacebookAllContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue)
    elif sn=='twitter':
        return getTwitterAllContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue)
    elif sn == 'mbox':
        return getMboxAllContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue)


def getFacebookAllContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue):
    if graphType == 'relNet':
        return getFacebookAllContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'trafficNet':
        return getFacebookAllContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'map':
        return getFacebookAllContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'wordFrec':
        return getfacebookAllForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)


def getFacebookAllContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    query = (
        'MATCH (n:fbUser)-[r:FRIEND]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) '
        'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
        'WITH n, count(s) as taggedTogetherValue, f '                                                                        
        'RETURN DISTINCT n.name AS propertyDump, taggedTogetherValue, f AS node ORDER BY '
    )

    if sortValue == 'timedesc':
        query = query + 'f.timestamp DESC '
    elif sortValue == 'timeasc':
        query = query + 'f.timestamp ASC '
    elif sortValue == 'name':
        query = query + 'f.name ASC '
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC '
    elif sortValue == 'degree':
        query = query + 'f.nodeDegree DESC '

    return graph.run(query).data()


def getFacebookAllContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    query = (
        'MATCH (u:fbUser {graph_information:[\'' + usr + '\', \'facebook\']})-->(p) '
        'WHERE '
        ' exists(p.place_latitude) AND exists(p.place_longitude) AND '
        ' not p.place_latitude = \'\' AND not p.place_longitude = \'\' '
        'RETURN u.name AS propertyDump, p AS place ORDER BY '
    )

    if sortValue == 'timedesc':
        query = query + 'p.timestamp DESC'
    elif sortValue == 'timeasc':
        query = query + 'p.timestamp ASC'
    elif sortValue == 'name':
        query = query + 'u.name ASC'
    elif sortValue == 'degree':
        query = query + 'p.nodeDegree DESC'

    return graph.run(query).data()


def getfacebookAllForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    return graph.run(
                'MATCH (w:Word {graph_information:[\'' + usr + '\', \'facebook\']}) '
                'RETURN  w.word as word, toFloat(w.value) as value ORDER BY value DESC limit 100 '
            ).data()


def getTwitterAllContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue):
    if graphType == 'relNet':
        return getTwitterAllContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'trafficNet':
        return getTwitterAllContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'map':
        return getTwitterAllContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    else :
        return getTwitterAllWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)


def getTwitterAllContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    query = (
            'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})--(f) ' +
            'WHERE ' +
            ' exists(f.firstInteration) ' +
            'OPTIONAL MATCH (f)-[s:TAGGED_TOGETHER]-(d) '
            'WHERE '
            ' s.tagged_together>=' + minEdgeValue + ' ' +
            'RETURN u.username AS propertyDump, count(s) AS taggedTogetherValue, f AS node Order by '
        )

    if sortValue == 'timedesc':
        query = query + 'f.firstInteration DESC'
    elif sortValue == 'timeasc':
        query = query + 'f.firstInteration ASC'
    elif sortValue == 'name':
        query = query + 'f.name '
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC '
    elif sortValue == 'degree':
        query = query + 'f.nodeDegree DESC '

    return graph.run(query).data()


def getTwitterAllContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    return graph.run(
        'MATCH x=(u:twUser {graph_information:[\'' + usr + '\', \'twitter\']})-[:TWEETED]->(t) '
        'OPTIONAL MATCH (t)-[s:TAGGED_IN]-(f) '
        'WITH u,t,f,s '        
        'RETURN t AS node, collect(f.screen_name) AS taggedWith, count(s) as nodeDegree, u.username AS propertyDump'
    ).data()


def getTwitterAllContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    return graph.run(
        'MATCH (u:twUser)--(n:Tweet {graph_information:[\'' + usr + '\', \'twitter\']}) '
        'WHERE not n.latitude = \'\' AND not n.longitude = \'\' '
        'RETURN n as place, u.username AS propertyDump '
    ).data()


def getTwitterAllWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    return graph.run(
            'MATCH (w:Word {graph_information:[\'' + usr + '\', \'twitter\']})'
            'RETURN  w.word as word, toFloat(w.value) as value ORDER BY value DESC limit 100 '
        ).data()


def getMboxAllContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, sortValue):
    if graphType == 'relNet':
        return getMboxAllContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'trafficNet':
        return getMboxAllContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    elif graphType == 'map':
        return getMboxAllContactsForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)
    else:
        return getMboxAllForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue)


def getMboxAllContactsForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    query = (
        'MATCH (n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
        'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
    )

    if sortValue == 'timedesc':
        query = query + 'n.firstInteration DESC'
    elif sortValue == 'timeasc':
        query = query + 'n.firstInteration ASC'
    elif sortValue == 'name':
        query = query + 'n.label ASC'
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC'
    elif sortValue == 'degree':
        query = query + 'n.nodeDegree DESC'

    return graph.run(query).data()


def getMboxAllContactsForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    query = (
        'MATCH (n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr + '\', \'mbox\']}) '
        'RETURN n AS node, count(r) AS taggedTogetherValue ORDER BY '
    )

    if sortValue == 'timedesc':
        query = query + 'n.firstInteration DESC'
    elif sortValue == 'timeasc':
        query = query + 'n.firstInteration ASC'
    elif sortValue == 'name':
        query = query + 'n.label ASC'
    elif sortValue == 'tagcount':
        query = query + 'taggedTogetherValue DESC'
    elif sortValue == 'degree':
        query = query + 'n.nodeDegree DESC'

    return graph.run(query).data()


def getMboxAllForWordFrec(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, sortValue):
    return graph.run(
        ' MATCH(w:Word {graph_information:[\'' + usr + '\', \'mbox\']}) '
        'RETURN  w.word as word, toFloat(w.value) as value ORDER BY value DESC limit 100 '
    ).data()

##################  SELECTED LINKS #########################


def getSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, id):
    if sn=='facebook':
        return getFacebookSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id)
    elif sn=='twitter':
        return getTwitterSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id)
    elif sn == 'mbox':
        return getMboxSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id)


def getFacebookSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id):
    if graphType == 'relNet':
        return getFacebookSelectedLinkForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'trafficNet':
        return getFacebookSelectedLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'map':
        return getFacebookSelectedLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)


def getFacebookSelectedLinkForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    return graph.run(
        'MATCH (f)-[s:TAGGED_TOGETHER]->(d {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
        'WHERE ' +
        ' ID(s)=' + id + ' AND ' +
        ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
        '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
        ' f.nodeDegree>=' + minNodevalue + ' AND ' +
        ' s.tagged_together>=' + minEdgeValue + ' AND ' +
        ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
        '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
        ' d.nodeDegree>=' + minNodevalue + ' ' +
        'RETURN f.name as name_1, d.name as name_2, s.tagged_together AS link '
    ).data()


def getFacebookSelectedLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    return graph.run(
        'RETURN \'No links to visualize here\' AS place'
    ).data()


def getTwitterSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id):
    if graphType == 'relNet':
        return getTwitterSelectedLinkForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'trafficNet':
        return getTwitterSelectedLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'map':
        return getTwitterSelectedLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)


def getTwitterSelectedLinkForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    return graph.run(
        'MATCH (f)-[s:TAGGED_TOGETHER]->(e {graph_information:[\'' + usr + '\', \'twitter\']}) ' +
        'WHERE ' +
        ' ID(s) = ' + id + ' ' +
        'RETURN f.screen_name as name_1, e.screen_name as name_2, s.tagged_together AS link order by s.tagged_together DESC'
    ).data()


def getMboxSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr, id):
    if graphType == 'relNet':
        return getMboxSelectedLinkForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'trafficNet':
        return getMboxSelectedLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)
    elif graphType == 'map':
        return getMboxSelectedLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id)


def getMboxSelectedLinkForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    return graph.run(
        'MATCH (n)-[r:UNDIRECTED_EDGE]->(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
        'WHERE ' +
        ' ID(r) = ' + id + ' ' +
        'RETURN DISTINCT r, n.label AS name_1, p.label AS name_2, r.edge_weight AS link order by r.edge_weight DESC'
    ).data()


def getMboxSelectedLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr, id):
    return graph.run(
        'MATCH (n)-[r:DIRECTED_EDGE]->(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
        'WHERE ' +
        ' ID(r) = ' + id + ' ' +
        'RETURN DISTINCT r, n.label AS name_1, p.label AS name_2, r.edge_weight AS link order by r.edge_weight DESC'
    ).data()


##################  FILTERED LINKS #########################


def getFilteredLinks (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr):
    if sn=='facebook':
        return getFacebookFilteredLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr)
    elif sn=='twitter':
        return getTwitterFilteredLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr)
    elif sn == 'mbox':
        return getMboxFilteredLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr)


def getFacebookFilteredLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr):
    if graphType == 'relNet':
        return getFacebookFilteredLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'trafficNet':
        return getFacebookFilteredLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'map':
        return getFacebookFilteredLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)


def getFacebookFilteredLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (f)-[s:TAGGED_TOGETHER]->(d {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
        'WHERE ' +
        ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
        '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
        ' f.nodeDegree>=' + minNodevalue + ' AND ' +
        ' s.tagged_together>=' + minEdgeValue + ' AND ' +
        ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
        '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
        ' d.nodeDegree>=' + minNodevalue + ' ' +
        'RETURN f.name as name_1, d.name as name_2, s.tagged_together AS link order by s.tagged_together DESC'
    ).data()


def getFacebookFilteredLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'RETURN \'No links to visualize here\' AS place'
    ).data()


def getTwitterFilteredLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr):
    if graphType == 'relNet':
        return getTwitterFilteredLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'trafficNet':
        return getTwitterFilteredLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'map':
        return getTwitterFilteredLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)


def getTwitterFilteredLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (f)-[s:TAGGED_TOGETHER]->(e) ' +
        'WHERE ' +
        ' f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\' AND '
        ' e.firstInteration>\'' + start_date + '\' AND e.firstInteration<\'' + end_date + '\' AND '
        ' f.nodeDegree>=' + minNodevalue + ' AND '
        's.tagged_together>=' + minEdgeValue + ' ' +
        'RETURN DISTINCT s, f.screen_name as name_1, e.screen_name as name_2, s.tagged_together AS link order by s.tagged_together DESC'
    ).data()


def getMboxFilteredLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr):
    if graphType == 'relNet':
        return getMboxFilteredLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'trafficNet':
        return getMboxFilteredLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'map':
        return getMboxFilteredLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)


def getMboxFilteredLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (n:Undirected_Node)--(m:Mail {graph_information:[\'' + usr + '\', \'mbox\']})--(p:Undirected_Node) ' +
        'MATCH (n)-[r:UNDIRECTED_EDGE]->(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
        'WHERE ' +
        ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' AND ' +
        ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
        ' r.edge_weight>' + minEdgeValue + ' ' +
        'RETURN DISTINCT r, n.label AS name_1, p.label AS name_2, r.edge_weight AS link order by r.edge_weight DESC'
    ).data()


def getMboxFilteredLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (n)-[r:DIRECTED_EDGE]->(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
        'WHERE ' +
        ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
        ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
        ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
        ' r.edge_weight>' + minEdgeValue + ' ' +
        'RETURN DISTINCT r, n.label AS name_1, p.label AS name_2, r.edge_weight AS link order by r.edge_weight DESC'
    ).data()


##################  ALL LINKS #########################

def getAllLinks (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr):
    if sn=='facebook':
        return getFacebookAllLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr)
    elif sn=='twitter':
        return getTwitterAllLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr)
    elif sn == 'mbox':
        return getMboxAllLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr)


def getFacebookAllLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr):
    if graphType == 'relNet':
        return getFacebookAllLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'trafficNet':
        return getFacebookAllLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'map':
        return getFacebookAllLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)


def getFacebookAllLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (f)-[s:TAGGED_TOGETHER]->(d {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
        'RETURN f.name as name_1, d.name as name_2, s.tagged_together AS link order by s.tagged_together DESC'
    ).data()


def getFacebookAllLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'RETURN \'No links to visualize here\' AS place'
    ).data()


def getTwitterAllLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr):
    if graphType == 'relNet':
        return getTwitterAllLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'trafficNet':
        return getTwitterAllLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'map':
        return getTwitterAllLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)


def getTwitterAllLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (f)-[s:TAGGED_TOGETHER]->(e {graph_information:[\'' + usr + '\', \'twitter\']}) ' +
        'RETURN DISTINCT s, f.screen_name as name_1, e.screen_name as name_2, s.tagged_together AS link order by s.tagged_together DESC'
    ).data()


def getMboxAllLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, graphType, usr):
    if graphType == 'relNet':
        return getMboxAllLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'trafficNet':
        return getMboxAllLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)
    elif graphType == 'map':
        return getMboxAllLinksForMap(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr)


def getMboxAllLinksForRelationshipNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (n)-[r:UNDIRECTED_EDGE]->(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
        'RETURN DISTINCT r, n.label AS name_1, p.label AS name_2, r.edge_weight AS link order by r.edge_weight DESC'
    ).data()


def getMboxAllLinksForTrafficNetwork(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, usr):
    return graph.run(
        'MATCH (n)-[r:DIRECTED_EDGE]->(p {graph_information:[\'' + usr + '\', \'mbox\']}) ' +
        'RETURN DISTINCT r, n.label AS name_1, p.label AS name_2, r.edge_weight AS link order by r.edge_weight DESC'
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
    sortValue = json.dumps(data['sortValue']).replace('\"', '')

    if dataViz1=='selected':
        if dataViz2 == 'contacts':
            # for search a specific node
            if (graphType == 'relNet' or graphType == 'trafficNet'):
                if len(sys.argv) <= 3:
                    try:
                        idNode = str(sys.argv[2])
                        id = idNode
                    except Exception as e:
                        id = 'All'

                    print (json.dumps(
                        getSelectedContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, id)
                    ))
            # for search a place
            if (graphType == 'map'):
                lat = ''
                lng = ''
                if len(sys.argv) <= 3:
                    if sn=='facebook':
                        lat = sys.argv[2]
                        lng = sys.argv[2]
                    else:
                        lng = 0
                        lat = 0
                elif len(sys.argv) == 4:

                    lng = str(sys.argv[2]).split('.')
                    lat = str(sys.argv[3]).split('.')

                    lng = lng[0] + '.' + lng[1][:4]
                    lat = lat[0] + '.' + lat[1][:4]

                if sn == 'facebook':
                    print (json.dumps(
                        getFacebookPlace(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, lat, lng)
                    ))
                elif sn == 'twitter':
                    print (json.dumps( getTwitterPlace(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, lat, lng) ))

                elif sn == 'mbox':
                    print (json.dumps( getMboxPlace() ))
        elif dataViz2 == 'links':
            if len(sys.argv) == 3:
                id = str(sys.argv[2])
                print (json.dumps(getSelectedLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, id)))
    elif dataViz1=='filtered':
        ntd = ''
        if len(sys.argv) == 3:
            ntd = str(sys.argv[2])
        if dataViz2 == 'contacts':
            print (json.dumps( getFilteredContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, sortValue, ntd )))
        if dataViz2 == 'links':
            print (json.dumps( getFilteredLinks (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr) ))
    elif dataViz1 == 'all':
        if dataViz2 == 'contacts':
            print (json.dumps( getAllContacts(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr, sortValue)))
        elif dataViz2 == 'links':
            print (json.dumps(getAllLinks(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, usr)))