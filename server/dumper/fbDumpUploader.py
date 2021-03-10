#! /usr/bin/env python
# coding= UTF-8

import json
import os
from zipfile import ZipFile
import sys
import time
import os

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

from py2neo.data import Node

sys.path.append('~/sna/server/dataSearcher/nlp')
import wordsFrequency

sys.path.append('~/sna/server/')
import mailSender as ms

import dbConnector as dbc
graph = dbc.neo4jHelper()


def extract(entries):
    for entrie in entries:
        file = entrie
        data_zip = ZipFile(path + '/' + file, 'r')
        data_zip.extractall(path=path)
        # remove the zip file from the folder /uploads/usr/filename
        os.remove(path + '/' + file)


def createUserNode(path, usr):
    file = path + '/' + 'profile_information/profile_information.json'
    if os.path.exists(file):
        config = json.loads(open(file).read())
        node = Node(
            'fbUser',
            name=config['profile']['name']['full_name'].encode('latin1'),
            email=config['profile']['emails']['emails'],
            birthday=str(config['profile']['birthday']['year']) + '/' + str(config['profile']['birthday']['month']) + '/' + str(config['profile']['birthday']['day']),
            profile_uri=config['profile']['profile_uri'],
            graph_information=[usr, 'facebook'],
            userProfileProperty=config['profile']['emails']['emails'][0]
        )
        graph.create(node)

        return config['profile']['emails']['emails'][0]


def createFriendsNode(path, usr, userProfileProperty):
    file = path + '/' + 'friends/friends.json'

    if os.path.exists(file):
        friends = json.loads(open(file).read())
        for friend in friends['friends']:
            name = friend['name'].encode('latin1')
            timestamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(friend['timestamp']))

            node = Node(
                'Friend',
                name=name,
                timestamp=timestamp,
                graph_information=[usr, 'facebook'],
                userProfileProperty = userProfileProperty
            )
            graph.create(node)

        graph.run(
            'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (f:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '        
            'WHERE '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' '                                                  
            'MERGE (u)-[r:FRIEND {relationship_type:[\'friend\']}]->(f) '
        )


def createRemovedFriendNode(path, usr, userProfileProperty):
    file = path + '/' + 'friends/removed_friends.json'

    if os.path.exists(file):
        friends = json.loads(open(file).read())
        for friend in friends['deleted_friends']:
            name = friend['name'].encode('latin1')
            timestamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(friend['timestamp']))

            node = Node(
                'RemovedFriend',
                name=name,
                removed_timestamp=timestamp,
                timestamp=timestamp,
                graph_information=[usr, 'facebook'],
                userProfileProperty = userProfileProperty
            )
            graph.create(node)

        graph.run(
            'MATCH (f:RemovedFriend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE f.name = u.name AND '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' '
            'DELETE f'

        )

        graph.run(
            'MATCH (u:RemovedFriend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (f:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE u.name = f.name AND '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' '
            'SET f.previously_delete_at=u.removed_timestamp '
            'DELETE u '
        )

        graph.run(
            'MATCH (f:RemovedFriend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' '                                                  
            'MERGE (u)-[r:FRIEND {relationship_type:[\'removed_friend\']}]->(f) '
        )

        graph.run(
            'MATCH (n:RemovedFriend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' n.userProfileProperty=\'' + userProfileProperty + '\' '
            'SET n:Friend '
        )


def createPostNode(path, usr, userProfileProperty):
    file = path + '/' + 'posts/your_posts_1.json'

    if os.path.exists(file):
        posts = json.loads(open(file).read())
        for post in posts:
            timestamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(post['timestamp']))
            post_text = ''
            title = ''
            url = ''
            tags = ''
            place_name = ''
            place_latitude = ''
            place_longitude = ''
            place_address = ''
            place_url = ''
            media_description = ''
            media_title = ''

            if 'data' in post:
                for d in post['data']:
                    if 'post' in d:
                        post_text = d['post'].encode('latin1').decode('utf8')
                        if post_text.find('@[') != -1:
                            post_text = ''.join([i for i in post_text if not i.isdigit()])
                            post_text = post_text.replace('[', '').replace(']', '').replace('::', '')

            if 'attachments' in post:
                for a in post['attachments']:
                    if 'data' in a:
                        for d in a['data']:
                            if 'external_context' in d:
                                if 'url' in d['external_context']:
                                    url = d['external_context']['url']
                            if 'place' in d:
                                place_name = d['place']['name'].encode('latin1').decode('utf8')
                                place_address = d['place']['address'].encode('latin1').decode('utf8')
                                if 'coordinate' in d['place']:
                                    place_latitude = str(d['place']['coordinate']['latitude'])
                                    place_longitude = str(d['place']['coordinate']['longitude'])
                                if 'url' in d['place']:
                                    place_url = d['place']['url'].encode('latin1').decode('utf8')
                            if 'media' in d:
                                if 'title' in d['media']:
                                    media_title = d['media']['title'].encode('latin1').decode('utf8')
                                if 'description' in d['media']:
                                    media_description = d['media']['description'].encode('latin1').decode('utf8')

            if 'title' in post:
                title = post['title'].encode('latin1').decode('utf8')

            if 'tags' in post:
                for tag in post['tags']:
                    tags = tags + ' @' + tag.encode('latin1')
                tags = tags[1:]

            if post_text!='' and title!='':
                node = Node(
                    'Post',
                    timestamp=timestamp,
                    title=title,
                    url=url,
                    tags=tags,
                    content=post_text,
                    place_name=place_name,
                    place_latitude = place_latitude,
                    place_longitude = place_longitude,
                    place_address =  place_address,
                    place_url = place_url,
                    media_title = media_title,
                    media_description = media_description,
                    graph_information = [usr, 'facebook'],
                    userProfileProperty = userProfileProperty
                )
                graph.create(node)

        graph.run(
            'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (p:Post {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' p.userProfileProperty=\'' + userProfileProperty + '\' '                                                    
            'MERGE (u)-[r:PUBLISHED {relationship_type:[\'published\']}]->(p) '
        )

        graph.run(
            'MATCH (p:Post {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (f:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' p.userProfileProperty=\'' + userProfileProperty + '\' AND '                                                   
            'p.tags CONTAINS f.name '
            'OR p.content CONTAINS f.name '
            'OR p.title CONTAINS f.name AND not f:namesake '
            'MERGE (p)-[t:TAG {relationship_type:[\'tag\']}]->(f) RETURN null'
        )


def createFriendPostNode(path, usr, userProfileProperty):
    file = path + '/' + 'posts/other_people\'s_posts_to_your_timeline.json'

    if os.path.exists(file):
        posts = json.loads(open(file).read())
        posts = posts['wall_posts_sent_to_you']['activity_log_data']
        for post in posts:
            timestamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(post['timestamp']))
            title = post['title'].encode('latin1')
            post_text = ''
            external_context = ''
            tags = ''

            for d in post['data']:
                if 'post' in d:
                    post_text = d['post'].encode('latin1').decode('utf8')

            if 'attachments' in post:
                for a in post['attachments']:
                    if 'data' in a:
                        for d in a['data']:
                            if 'external_context' in d:
                                external_context = d['external_context']['url']

            if 'tags' in post:
                for t in post['tags']:
                    tags = t

            node = Node(
                'FriendPost',
                timestamp=timestamp,
                title=title,
                tags=tags,
                content=post_text,
                external_context = external_context,
                graph_information=[usr, 'facebook'],
                userProfileProperty = userProfileProperty
            )
            graph.create(node)

        graph.run(
            'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (p:FriendPost {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' p.userProfileProperty=\'' + userProfileProperty + '\' '
            'MERGE (p)-[r:PUBLISHED {relationship_type:[\'tag\']}]->(u)'
        )

        graph.run(
            'MATCH (f:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (p:FriendPost {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE p.title CONTAINS f.name AND not f:namesake AND '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' p.userProfileProperty=\'' + userProfileProperty + '\' '                                                      
            'MERGE (f)-[r:TAG {relationship_type:[\'published\']}]->(p) '
        )

        graph.run(
            'MATCH (p:FriendPost {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (f:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE p.tags CONTAINS f.name AND not f:namesake AND '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' p.userProfileProperty=\'' + userProfileProperty + '\' '
            'MERGE (p)-[r:TAG {relationship_type:[\'tag\']}]->(f)'
        )


def createCommentsNode(path, usr, userProfileProperty):
    file = path + '/' + 'comments/comments.json'

    if os.path.exists(file):
        comments = json.loads(open(file).read())

        for comment in comments['comments']:
            timestamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(comment['timestamp']))
            title = comment['title'].encode('latin1')

            if 'data' in comment:
                group = ''
                for d in comment['data']:
                    comment_text = d['comment']['comment'].encode('latin1')
                    if 'group' in d['comment']:
                        group = d['comment']['group'].encode('latin1')

                if comment != '' :
                    if group == '':
                        node = Node(
                            'Comment',
                            timestamp=timestamp,
                            title=title,
                            content=comment_text,
                            graph_information=[usr, 'facebook'],
                            userProfileProperty = userProfileProperty
                        )
                    else:
                        node = Node(
                            'Comment',
                            timestamp=timestamp,
                            title=title,
                            content=comment_text,
                            group=group,
                            graph_information=[usr, 'facebook'],
                            userProfileProperty = userProfileProperty
                        )
                    graph.create(node)

            if 'attachments' in comment:
                for attachments in comment['attachments']:
                    for d in attachments['data']:
                        if 'external_context' in d:
                            url = d['external_context']['url']
                            graph.run(
                                'MATCH (c:Comment {timestamp:\'' + timestamp + '\', graph_information: [\'' + usr + '\', \'facebook\']}) '
                                'WHERE '
                                ' c.userProfileProperty=\'' + userProfileProperty + '\' '
                                'SET c.url=\'' + url + '\' '
                            )

        graph.run(
            'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (c:Comment {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' c.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' '
            'MERGE (u)-[r:PUBLISHED {relationship_type:[\'published\']}]->(c) '
        )

        graph.run(
            'MATCH (c:Comment {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (u:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' c.userProfileProperty=\'' + userProfileProperty + '\' AND '                                                              
            ' c.content CONTAINS u.name OR '
            ' c.title CONTAINS u.name AND not u:namesake '
            'MERGE (u)<-[r:TAG {relationship_type:[\'tag\']}]-(c) '
        )


def setNodeDegree(usr, userProfileProperty):

    # set degree for each friend

    graph.run(
        'MATCH (n:Friend {graph_information: [\'' + usr + '\',\'facebook\']})<-[r:TAG]-(p) '
        'WHERE '
        ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' p.userProfileProperty=\'' + userProfileProperty + '\' '                                                    
        'WITH n, count((n)-[r]-()) as degree '
        'SET n.inNodeDegree = degree '
    )

    graph.run(
        'MATCH (n:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
        'WHERE '
        ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '                                                  
        ' not exists(n.inNodeDegree) '
        'SET n.inNodeDegree = 0 '
    )

    graph.run(
        'MATCH (n:Friend {graph_information: [\'' + usr + '\',\'facebook\']})-[r:TAG]->(p) '
        'WHERE '
        ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' p.userProfileProperty=\'' + userProfileProperty + '\' '
        'WITH n, count((n)-[r]-()) as degree '
        'SET n.outNodeDegree = degree '
    )

    graph.run(
        'MATCH (n:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
        'WHERE '
        ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '                                                  
        ' not exists(n.outNodeDegree) '
        'SET n.outNodeDegree = 0 '
    )

    graph.run(
        'MATCH (n:Friend {graph_information: [\'' + usr + '\',\'facebook\']}) '
        'WHERE '
        ' n.userProfileProperty=\'' + userProfileProperty + '\' '                                                 
        'SET n.nodeDegree = n.inNodeDegree + n.outNodeDegree '
    )

    #####

    graph.run(
        'MATCH (f:Friend {graph_information: [\'' + usr + '\',\'facebook\']})-[s:TAG]-(p)  '
        'WHERE '
        ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' p.userProfileProperty=\'' + userProfileProperty + '\' '
        'WITH count(s) as s,p '
        'SET p.nodeDegree=s'
    )

    graph.run(
        'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']})-[r:PUBLISHED]-(p) '
        'WHERE '
        ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' p.userProfileProperty=\'' + userProfileProperty + '\' AND '                                                  
        ' not exists(p.nodeDegree) '
        'SET p.nodeDegree = 0'
    )


def taggedTogether(usr, userProfileProperty):
    graph.run(
        'MATCH (n:Friend {graph_information: [\'' + usr + '\',\'facebook\']})<-[x:TAG]-(p)-[y:TAG]->(m:Friend) '
        'WHERE '
        ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' p.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' m.userProfileProperty=\'' + userProfileProperty + '\' '                                                    
        'MERGE (n)-[z:TAGGED_TOGETHER]->(m) '
        'ON CREATE SET z.tagged_together = 1 '
        'ON MATCH SET z.tagged_together = z.tagged_together + 1 RETURN null'
    )

    graph.run(
        'MATCH (a {graph_information: [\'' + usr + '\',\'facebook\']})-[r1:TAGGED_TOGETHER]->(b)-[r2:TAGGED_TOGETHER]->(a) '
        'WHERE ID(a)<ID(b) AND '
        ' a.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' b.userProfileProperty=\'' + userProfileProperty + '\' '                                           
        'DELETE r2'
    )


def createAddressBookNode(path, usr, userProfileProperty):
    file = path + '/' + 'about_you/your_address_books.json'

    if os.path.exists(file):
        addressBooks = json.loads(open(file).read())
        addressBooks = addressBooks['address_book']['address_book']
        for addressBook in addressBooks:
            contact_point = []
            name = addressBook['name'].encode('latin1')
            created_timestampe = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(addressBook['created_timestamp']))

            if 'updated_timestamp' in addressBook:
                updated_timestamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(addressBook['updated_timestamp']))

            for detail in addressBook['details']:
                if 'contact_point' in detail:
                    if detail['contact_point'].find('note: ') == -1:
                        if detail['contact_point'].find('middle_name: ') == -1:
                            contact_point.append(detail['contact_point'])

                            node = Node(
                                'Contact',
                                name=name,
                                created_timestamp=created_timestampe,
                                updated_timestamp=updated_timestamp,
                                contact_point=contact_point,
                                graph_information=[usr, 'facebook'],
                                userProfileProperty = userProfileProperty
                            )
                            graph.create(node)

        # join the contact with the same name
        graph.run(
            'MATCH (c:Contact {graph_information:[\'' + usr + '\', \'facebook\']}) '
            'WITH c.name AS name, COLLECT(c) AS contacts, SIZE(COLLECT(c)) AS nbr_nodes,c '
            'WHERE SIZE(contacts) > 1 AND '
            ' c.userProfileProperty = \'' + userProfileProperty + '\' ' 
            'WITH name as name, contacts as contacts, nbr_nodes AS nbr_nodes '
            'UNWIND RANGE(1, nbr_nodes - 1) as idx '
            'CALL apoc.refactor.mergeNodes([contacts[0], contacts[idx]], '
            '{properties: {name:\'combine\', created_timestampe:\'overwrite\', updated_timestamp:\'overwrite\', contact_point:\'combine\'}}) '
            'YIELD node RETURN name, max(idx) + 1 AS `Nbr Nodes Merged`'
        )

        # create a relationship between a friend and his personal telephone number or email
        graph.run(
            'MATCH (n:Contact {graph_information:[\'' + usr + '\', \'facebook\']}) '
            'MATCH (m:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) '
            'WHERE n.name = m.name AND '
            'n.userProfileProperty=\'' + userProfileProperty + '\' AND '
            'm.userProfileProperty=\'' + userProfileProperty + '\' '
            'SET m.phoneContacts = n.contact_point'
        )


def createLocationNode(path, usr, userProfileProperty):
    file = path + '/' + 'location/location_history.json'

    if os.path.exists(file):
        locations = json.loads(open(file).read())
        locations = locations['location_history']

        placesConstructor(locations, usr, userProfileProperty)


def createUserLocationNode(path, usr, userProfileProperty):
    file = path + '/' + 'your_places/places_you\'ve_created.json'

    if os.path.exists(file):
        places = json.loads(open(file).read())
        places = places['your_places']

        placesConstructor(places, usr, userProfileProperty)


def placesConstructor(locations, usr, userProfileProperty):
    for location in locations:
        name = location['name'].encode('latin1')
        creation_timestamp = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(location['creation_timestamp']))
        latitude = str(location['coordinate']['latitude'])
        longitude = str(location['coordinate']['longitude'])

        if 'address' in location and 'url' in location:
            url = location['url']
            address = location['address'].encode('latin1')
            node = Node(
                'Place',
                name=name,
                timestamp=creation_timestamp,
                url=url, address=address,
                place_latitude=latitude,
                place_longitude=longitude,
                graph_information=[usr, 'facebook'],
                userProfileProperty = userProfileProperty
            )
            graph.create(node)
        else:
            node = Node(
                'Place',
                name=name,
                timestamp=creation_timestamp,
                place_latitude=latitude,
                place_longitude=longitude,
                graph_information=[usr, 'facebook'],
                userProfileProperty=userProfileProperty
            )
            graph.create(node)

    graph.run(
        'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
        'MATCH (p:Place {graph_information: [\'' + usr + '\',\'facebook\']}) '
        'WHERE '
        ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' p.userProfileProperty=\'' + userProfileProperty + '\' '
        'MERGE (u)-[:LOCATED_AT]->(p)'
    )


def createDmNode(path, usr, userProfileProperty):
    file = path + '/messages/inbox'

    if os.path.exists(file):
        for dirpath, dirnames, files in os.walk(file, topdown=False):
            for file in os.listdir(dirpath):
                if file.endswith(".json"):
                    currentFile = dirpath + '/' + file
                    direct_messages = json.loads(open(currentFile).read())
                    participants = []

                    for participant in direct_messages['participants']:

                        participants.append(participant['name'].encode('latin1'))

                        node = Node(
                            'DM_Participant',
                            name = participant['name'].encode('latin1'),
                            graph_information=[usr, 'facebook'],
                            userProfileProperty=userProfileProperty
                        )
                        graph.create(node)

                    next =  'last'
                    for message in direct_messages['messages']:
                        content = ''
                        if 'content' in message:
                            content = message['content'].encode('latin1').decode('utf8')

                        node = Node(
                            'Direct_Message',
                            sender=message['sender_name'].encode('latin1'),
                            timestamp=time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(message['timestamp_ms']/ 1000)),
                            content=content,
                            participants = participants,
                            next = next,
                            graph_information=[usr, 'facebook'],
                            userProfileProperty=userProfileProperty
                        )
                        graph.create(node)

                        next = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(message['timestamp_ms']/ 1000))

        graph.run(
            'MATCH (n:Direct_Message {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (m:Direct_Message {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE n.timestamp = m.next AND '
            ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' m.userProfileProperty=\'' + userProfileProperty + '\' '                                                                      
            'MERGE (n)-[r:REPLAY]-(m)  '          
            'REMOVE m.next '
        )

        graph.run(
            'MATCH (n:DM_Participant {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE n.name = u.name AND '
            ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' '                                                 
            'DETACH DELETE n '
        )

        graph.run(
            'MATCH (n:fbUser {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (u:Direct_Message {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '                                                                      
            ' ANY(participant IN u.participants WHERE participant = n.name) AND '
            ' not exists( ()<-[:REPLAY]-(u) )'
            'MERGE (n)-[r:PUBLISHED {relationship_type:[\'direct message\']}]->(u) '
        )

        graph.run(
            'MATCH (n:DM_Participant {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'MATCH (u:Direct_Message {graph_information: [\'' + usr + '\',\'facebook\']}) '
            'WHERE '
            ' n.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '                                                          
            ' ANY(participant IN u.participants WHERE participant = n.name) AND '
            ' not exists( ()<-[:REPLAY]-(u) )'
            'MERGE (n)-[r:PUBLISHED]->(u) '
        )

        graph.run(
            'MATCH (n:Direct_Message{graph_information: [\'' + usr + '\',\'facebook\']})<-[r:PUBLISHED]-() '
            'WHERE '
            ' n.userProfileProperty=\'' + userProfileProperty + '\' '                                                         
            'WITH count(r) AS degree, n  '
            'SET n.nodeDegree = degree '
        )


def normalizeDump(usr, userProfileProperty):
    graph.run(
        'MATCH (n:RemovedFriend {graph_information: [\'' + usr + '\',\'facebook\']}) '
        'WHERE '
        ' n.userProfileProperty=\'' + userProfileProperty + '\' '
        'REMOVE n:Friend '
    )

    graph.run(
        'MATCH (u:fbUser {graph_information: [\'' + usr + '\',\'facebook\']})--(uf:Friend) '
        'MATCH (n:fbUser {graph_information: [\'' + usr + '\',\'facebook\']})--(nf:Friend) '                                                           
        'WHERE '
        ' u.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' not n.userProfileProperty =\'' + userProfileProperty + '\'AND '
        ' uf.name = n.name AND '
        ' nf.name = u.name '
        'MERGE (u)-[r:FBUSERFRIEND {relationship_type:[\'friend\']}]->(n) '
    )

    graph.run(
        'MATCH (p:Post)--(u:fbUser)--(n:fbUser {graph_information: [\'' + usr + '\',\'facebook\']} ) '
        'WHERE '
        ' p.content CONTAINS n.name OR '
        ' p.title CONTAINS n.name OR '
        ' ANY(tags IN p.tags WHERE tags = n.name) '                                                   
        'MERGE (p)-[:TAG {relationship_type:[\'TAG\']}]->(n) '
    )

    graph.run(
        'MATCH (p:Comment)--(u:fbUser)--(n:fbUser {graph_information: [\'' + usr + '\',\'facebook\']} ) '
        'WHERE '
        ' p.content CONTAINS n.name OR '
        ' p.title CONTAINS n.name '
        'MERGE (p)-[:TAG {relationship_type:[\'TAG\']}]->(n) '
    )

    graph.run(
        'MATCH (p:Direct_Message)--(u:fbUser)--(n:fbUser {graph_information: [\'' + usr + '\',\'facebook\']} ) '
        'WHERE '
        ' ANY(participant IN p.participants WHERE participant = n.name) '                                                   
        'MERGE (p)-[:TAG {relationship_type:[\'TAG\']}]->(n) '
    )

    graph.run(
        'MATCH (p:FriendPost)--(u:fbUser)--(n:fbUser {graph_information: [\'' + usr + '\',\'facebook\']} ) '
        'WHERE '
        ' p.content CONTAINS n.name OR '
        ' p.title CONTAINS n.name OR '
        ' ANY(tags IN p.tags WHERE tags = n.name) '                   
        'MERGE (p)<-[:TAG {relationship_type:[\'TAG\']}]-(n) '
    )

if __name__ == '__main__':

    path = str(sys.argv[1])
    usr = str(sys.argv[2])
    wordFrecOption = str(sys.argv[3])

    try:
        entries = os.listdir(path)
        extract(entries)
    except Exception as e:
        print ("Error during the extraction.")

    #########################################

    try:
        userProfileProperty = createUserNode(path, usr)

        createFriendsNode(path, usr, userProfileProperty)

        createRemovedFriendNode(path, usr, userProfileProperty)

        createPostNode(path, usr, userProfileProperty)

        createFriendPostNode(path, usr, userProfileProperty)

        createCommentsNode(path, usr, userProfileProperty)

        setNodeDegree(usr, userProfileProperty)

        taggedTogether(usr, userProfileProperty)

        createAddressBookNode(path, usr, userProfileProperty)

        createLocationNode(path, usr, userProfileProperty)

        createUserLocationNode(path, usr, userProfileProperty)

        normalizeDump(usr, userProfileProperty)

        createDmNode(path, usr, userProfileProperty)

        wordsFrequency.getWordsForWordFrequency(usr, userProfileProperty, 'facebook', wordFrecOption)

        # remove this comments to enable email sending when upload is finished. You must create a gmail email to use this option
        # contentToSend = 'Your dump has been successfully loaded. Logged as ' + usr + ' and choose facebook from the social network dropdown to navigate the dump uploaded'
        # ms.send(contentToSend, usr)

        print('Dump successfully uploaded')

    except Exception as e:
         print ("Error during the creation of graph. Please retry or choose another file")