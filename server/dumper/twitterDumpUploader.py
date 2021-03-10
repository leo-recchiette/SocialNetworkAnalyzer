#! /usr/bin/env python
# coding= UTF-8
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

import json
import os
from zipfile import ZipFile
import re
import time
import requests

sys.path.append('~/sna/server/dataSearcher/nlp')
import wordsFrequency

from py2neo.data import Node

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
    accountDisplayName = ''
    username = ''
    email = ''
    accountId = ''
    createdAt = ''
    createdVia = ''
    graph_information = [usr, 'twitter']
    userCreationIp = ''
    birthDate = ''
    age = ''
    location = ''
    bio = ''
    website = ''


    # in account.js
    file = path + '/' + 'account.js'

    if os.path.exists(file):
        config = open(file).read()
        config = json.loads(config.replace('window.YTD.account.part0 = ', ''))
        accountDisplayName = config[0]['account']['accountDisplayName']
        username = '@' + config[0]['account']['username']
        email = config[0]['account']['email']
        #phoneNumber = config[0]['account']['phoneNumber']
        accountId = config[0]['account']['accountId']
        createdAt = time.strftime('%Y/%m/%d %H:%M:%S', time.strptime(config[0]['account']['createdAt'][:-5], '%Y-%m-%dT%H:%M:%S'))
        createdVia = config[0]['account']['createdVia']

    # in account-creation-ip.js
    file = path + '/' + 'account-creation-ip.js'

    if os.path.exists(file):
        config = open(file).read()
        config = json.loads(config.replace('window.YTD.account_creation_ip.part0 = ', ''))
        userCreationIp = config[0]['accountCreationIp']['userCreationIp']

    # in ageinfo.js
    file = path + '/' + 'ageinfo.js'

    if os.path.exists(file):
        config = open(file).read()
        config = json.loads(config.replace('window.YTD.ageinfo.part0 = ', ''))
        if 'ageInfo' in config[0]['ageMeta']:
            birthDate = config[0]['ageMeta']['ageInfo']['birthDate']
            age = config[0]['ageMeta']['ageInfo']['age'][0]


    # in profile.js
    file = path + '/' + 'profile.js'

    if os.path.exists(file):
        config = open(file).read()
        config = json.loads(config.replace('window.YTD.profile.part0 = ', ''))
        location = config[0]['profile']['description']['location']
        bio = config[0]['profile']['description']['bio']
        website = config[0]['profile']['description']['website']

    node = Node("twUser",
                account_display_name=accountDisplayName,
                username=username,
                email=email,
                account_id=accountId,
                created_at=createdAt,
                created_via=createdVia,
                user_creation_ip=userCreationIp,
                age=age,
                birth_date=birthDate,
                location=location,
                bio=bio,
                website=website,
                graph_information=graph_information,
                userProfileProperty = email
                )
    graph.create(node)

    return email


def createTweetsNode(path, usr, userProfileProperty):
    file = path + '/' + 'tweet.js'

    if os.path.exists(file):
        config = open(file).read()
        tweets = json.loads(config.replace('window.YTD.tweet.part0 = ', ''))
        graph_information = [usr, 'twitter']
        for tweet in tweets:
            latitude = ''
            longitude = ''

            full_text = tweet['tweet']['full_text']
            created_at = time.strftime('%Y/%m/%d %H:%M:%S',
                                       time.strptime(tweet['tweet']['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            retweet_count = tweet['tweet']['retweet_count']
            hashtags_text = ''

            if 'coordinates' in tweet['tweet']:
                longitude = tweet['tweet']['coordinates']['coordinates'][0]
                latitude = tweet['tweet']['coordinates']['coordinates'][1]
            elif 'geo' in tweet:
                longitude = tweet['tweet']['geo']['coordinates'][0]
                latitude = tweet['tweet']['geo']['coordinates'][1]

            for tag in tweet['tweet']['entities']['hashtags']:
                hashtags_text = tag['text']

            url = ''
            for link in tweet['tweet']['entities']['urls']:
                url = link['url']

            user_mentions = []
            for mention in tweet['tweet']['entities']['user_mentions']:
                user_mentions.append(
                    mention['id'] + ' @' + mention['screen_name'] + ' ' + mention['name']
                )

            node = Node("Tweet",
                        full_text=full_text,
                        created_at=created_at,
                        retweet_count=retweet_count,
                        hashtags_text='#'+hashtags_text,
                        url=url,
                        user_mentions=user_mentions,
                        graph_information=graph_information,
                        latitude = latitude,
                        longitude = longitude,
                        userProfileProperty = userProfileProperty
                        )
            graph.create(node)

        graph.run(
            'MATCH (t:Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'MATCH (u:twUser {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'WHERE '
            ' t.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' u.userProfileProperty =\'' + userProfileProperty + '\' '                                                        
            'MERGE (u)-[r:TWEETED {relationship_type:[\'tweeted\']}]->(t) '
        )


def createFollowerNode(path, usr, userProfileProperty):
    file = path + '/' + 'follower.js'

    if os.path.exists(file):
        config = open(file).read()
        followers = json.loads(config.replace('window.YTD.follower.part0 = ', ''))
        graph_information = [usr, 'twitter']
        for follower in followers:
            accountId = follower['follower']['accountId']
            userLink = follower['follower']['userLink']

            node = Node("Follower",
                        account_id=accountId,
                        user_link=userLink,
                        graph_information=graph_information,
                        userProfileProperty = userProfileProperty
                        )
            graph.create(node)

    graph.run(
        'MATCH (f:Follower {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'MATCH (u:twUser {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE '
        ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' u.userProfileProperty =\'' + userProfileProperty + '\' '                                                  
        'MERGE (f)-[r:FOLLOW {relationship_type:[\'follow\']}]->(u) '
    )

    graph.run(
        'MATCH (f:Follower {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'MATCH (t:Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE '
        'ANY(user_mentions IN t.user_mentions WHERE user_mentions CONTAINS f.account_id) AND '
        ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' t.userProfileProperty =\'' + userProfileProperty + '\' '
        'MERGE (t)<-[r:TAGGED_IN {relationship_type:[\'tagged_in\']} ]-(f)'
    )


def createFollowingNode(path, usr, userProfileProperty):
    file = path + '/' + 'following.js'

    if os.path.exists(file):
        config = open(file).read()
        following = json.loads(config.replace('window.YTD.following.part0 = ', ''))
        graph_information = [usr, 'twitter']
        for follower in following:
            accountId = follower['following']['accountId']
            userLink = follower['following']['userLink']

            node = Node("Following",
                    account_id=accountId,
                    user_link=userLink,
                    graph_information=graph_information,
                        userProfileProperty=userProfileProperty
                    )
            graph.create(node)

        graph.run(
            'MATCH (f:Following {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'MATCH (u:twUser {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'WHERE '
            ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' u.userProfileProperty =\'' + userProfileProperty + '\' '                                                     
            'MERGE (u)-[r:FOLLOWING {relationship_type:[\'following\']}]->(f) '
        )

        graph.run(
            'MATCH (f:Following {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'MATCH (t:Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'WHERE ANY(user_mentions IN t.user_mentions WHERE user_mentions CONTAINS f.account_id) AND '
            ' t.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' f.userProfileProperty =\'' + userProfileProperty + '\' '
            'MERGE (t)<-[r:TAGGED_IN {relationship_type:[\'tagged_in\']} ]-(f)'
        )


def setFollowsName(path, usr, userProfileProperty):
    file = path + '/' + 'tweet.js'

    if os.path.exists(file):
        config = open(file).read()
        tweets = json.loads(config.replace('window.YTD.tweet.part0 = ', ''))

        for tweet in tweets:
            if len(tweet['tweet']['entities']['user_mentions']) > 0:
                mentions =tweet['tweet']['entities']['user_mentions'][0]
                query = \
                    'WITH {json} as data ' \
                    'MATCH (f) ' \
                    'WHERE ' \
                    '\'' + usr + '\' IN f.graph_information AND \'twitter\' IN f.graph_information AND ' \
                    'EXISTS(f.account_id) AND f.account_id=data.id AND ' \
                    'f.userProfileProperty=\'' + userProfileProperty + '\' ' \
                    'SET f.name=data.name, f.screen_name=\'@\' + data.screen_name RETURN null'
                graph.run(query, json=mentions)


def setSameAccount(usr, userProfileProperty):
    graph.run(
        'MATCH (f:Follower {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'MATCH (e:Following {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE '
        ' e.screen_name = f.screen_name AND e.account_id = f.account_id AND '
        ' f.userProfileProperty =\'' + userProfileProperty + '\' AND '
        ' e.userProfileProperty =\'' + userProfileProperty + '\' '
        'CREATE (n:BothFollowType) '
        'SET '
        ' n.nodeDegree = f.nodeDegree, '
        ' n.account_id = f.account_id, '
        ' n.userProfileProperty = f.userProfileProperty, '
        ' n.graph_information = f.graph_information, '
        ' n.user_link = f.user_link, '
        ' n.screen_name = f.screen_name, '
        ' n.name = f.name '
        'DETACH DELETE f,e '
    )

    graph.run(
        'MATCH (u:twUser {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'MATCH (f:BothFollowType {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE '
        ' f.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' u.userProfileProperty =\'' + userProfileProperty + '\' '
        'MERGE (u)-[:FOLLOWING {relationship_type:[\'following\']}]->(f) '
        'MERGE (f)-[:FOLLOW {relationship_type:[\'follow\']}]->(u) '
    )

    graph.run(
        'MATCH (f:BothFollowType {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'MATCH (t:Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE ANY(user_mentions IN t.user_mentions WHERE user_mentions CONTAINS f.account_id) AND '
        ' t.userProfileProperty=\'' + userProfileProperty + '\' AND '
        ' f.userProfileProperty =\'' + userProfileProperty + '\' '
        'MERGE (t)<-[r:TAGGED_IN {relationship_type:[\'tagged_in\']} ]-(f)'
    )


def setFirstInteration(usr, userProfileProperty):
    graph.run(
        'MATCH (t)-[:TAGGED_IN]-(f {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WITH t, min(t.created_at) as min, f '
        'WHERE '
        ' t.userProfileProperty = \''+ userProfileProperty +'\' AND '
        ' f.userProfileProperty = \''+ userProfileProperty +'\' '                                                                 
        'SET f.firstInteration = min '

    )


def createLikedTweetNode(path, usr, userProfileProperty):
    file = path + '/' + 'like.js'

    if os.path.exists(file):
        config = open(file).read()
        likes = json.loads(config.replace('window.YTD.like.part0 = ', ''))
        graph_information = [usr, 'twitter']
        for like in likes:
            tweetId = like['like']['tweetId']
            fullText = like['like']['fullText']
            expandedUrl = like['like']['expandedUrl']

            node = Node("Liked_Tweet",
                        tweet_id=tweetId,
                        full_text=fullText,
                        expanded_url=expandedUrl,
                        graph_information=graph_information,
                        userProfileProperty = userProfileProperty
                        )
            graph.create(node)

        graph.run(
            'MATCH (t:Liked_Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'MATCH (u:twUser {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'WHERE '
            ' t.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' u.userProfileProperty =\'' + userProfileProperty + '\' '                                                              
            'MERGE (u)-[r:TWEETED {relationship_type:[\'liked_tweet\']}]->(t) '
        )

        graph.run(
            'MATCH (t:Liked_Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'MATCH (f:Following {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'WHERE exists(f.screen_name) AND t.full_text CONTAINS f.screen_name AND '
            ' t.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' f.userProfileProperty =\'' + userProfileProperty + '\' '                                                                 
            'MERGE (t)<-[r:TAGGED_IN {relationship_type:[\'tagged_in\']} ]-(f) '
        )

        graph.run(
            'MATCH (t:Liked_Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'MATCH (f:Follower {graph_information: [\'' + usr + '\',\'twitter\']}) '
            'WHERE exists(f.screen_name) AND t.full_text CONTAINS f.screen_name AND '
            ' t.userProfileProperty=\'' + userProfileProperty + '\' AND '
            ' f.userProfileProperty =\'' + userProfileProperty + '\' '                                                                
            'MERGE (t)<-[r:TAGGED_IN {relationship_type:[\'tagged_in\']} ]-(f) '
        )


def setNodeDegree(usr, userProfileProperty):
    graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\',\'twitter\']})-[r:TAGGED_IN]->() '
        'WHERE '
        ' n.userProfileProperty =\'' + userProfileProperty + '\' '                                                   
        'WITH n, count((n)-[r]-()) as degree '
        'SET n.nodeDegree = degree RETURN n'
    )

    graph.run(
        'MATCH (n:Following {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE '
        ' not exists(n.nodeDegree) AND '
        ' n.userProfileProperty =\'' + userProfileProperty + '\' '                                                             
        'SET n.nodeDegree = 0 '
    )

    graph.run(
        'MATCH (n:Follower {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE '
        ' not exists(n.nodeDegree) AND '
        ' n.userProfileProperty =\'' + userProfileProperty + '\' '                                                            
        'SET n.nodeDegree = 0 '
    )

    graph.run(
        'MATCH (t:Tweet {graph_information: [\'' + usr + '\',\'twitter\']})-[:TAGGED_IN]-() '
        'WHERE '
        ' t.userProfileProperty =\'' + userProfileProperty + '\' '                                                 
        'WITH  t,count((t)-[:TAGGED_IN]-()) as nd '
        'SET t.nodeDegree = nd '
    )

    graph.run(
        'MATCH (t:Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE not exists(t.nodeDegree) AND '
        ' t.userProfileProperty =\'' + userProfileProperty + '\' '                                                       
        'SET t.nodeDegree = 0 '
    )

    graph.run(
        'MATCH (t:Liked_Tweet {graph_information: [\'' + usr + '\',\'twitter\']})-[:TAGGED_IN]-() '
        'WHERE '
        ' t.userProfileProperty =\'' + userProfileProperty + '\' '
        'WITH  t,count((t)-[:TAGGED_IN]-()) as nd '
        'SET t.nodeDegree = nd '
    )

    graph.run(
        'MATCH (t:Liked_Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE not exists(t.nodeDegree) AND '
        ' t.userProfileProperty =\'' + userProfileProperty + '\' '
        'SET t.nodeDegree = 0 '
    )


def setTaggedTogether(usr, userProfileProperty):
    graph.run(
        'MATCH (n {graph_information: [\'' + usr + '\',\'twitter\']})-[:TAGGED_IN]->(p)<-[:TAGGED_IN]-(m) '
        'WHERE n.screen_name<>m.screen_name AND '
        ' n.userProfileProperty =\'' + userProfileProperty + '\' AND '
        ' p.userProfileProperty =\'' + userProfileProperty + '\' AND '
        ' m.userProfileProperty =\'' + userProfileProperty + '\' '                                                     
        'MERGE (n)-[z:TAGGED_TOGETHER]->(m) '
        'ON CREATE SET z.tagged_together = 1 '
        'ON MATCH SET z.tagged_together = z.tagged_together + 1 '
        'RETURN null'
    )

    graph.run(
        'MATCH (a {graph_information: [\'' + usr + '\',\'twitter\']})-[r1:TAGGED_TOGETHER]->(b)-[r2:TAGGED_TOGETHER]->(a) '
        'WHERE ID(a)<ID(b) AND '
        ' a.userProfileProperty =\'' + userProfileProperty + '\' AND '
        ' b.userProfileProperty =\'' + userProfileProperty + '\' '
        'DELETE r2'
    )


def normalizeDump(usr, userProfileProperty):
    graph.run(
        'MATCH (t:Tweet {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'WHERE t.full_text=~ \'(?ism)RT @.*\' AND '
        ' t.userProfileProperty =\'' + userProfileProperty + '\' '
        'SET t:Retweet '
        'REMOVE t:Tweet '
    )

    graph.run(
        'MATCH (u:twUser {graph_information: [\'' + usr + '\',\'twitter\']})'
        'MATCH (v:twUser)--(f:Follower {graph_information: [\'' + usr + '\',\'twitter\']})'
        'WHERE'
        ' u.userProfileProperty = \''+ userProfileProperty +'\' AND '
        ' not v.userProfileProperty = \''+ userProfileProperty +'\' AND '
        ' u.account_id = f.account_id '
        'MERGE (u)-[r:FOLLOW]->(v) '
        'SET f.screen_name = u.username, f.name = u.account_display_name'
    )

    graph.run(
        'MATCH (u:twUser {graph_information: [\'' + usr + '\',\'twitter\']})'
        'MATCH (v:twUser)--(f:Following {graph_information: [\'' + usr + '\',\'twitter\']})'
        'WHERE'
        ' u.userProfileProperty = \'' + userProfileProperty + '\' AND '
        ' not v.userProfileProperty = \'' + userProfileProperty + '\' AND '
        ' u.account_id = f.account_id '
        'MERGE (u)-[r:FOLLOW]->(v) '
        'SET f.screen_name = u.username, f.name = u.account_display_name'
    )
#
    graph.run(
        'MATCH (f:Follower)--(v:twUser {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'MATCH (u:twUser) '
        'WHERE'
        ' not u.userProfileProperty = \'' + userProfileProperty + '\' AND '
        ' v.userProfileProperty = \'' + userProfileProperty + '\' AND '
        ' f.account_id = u.account_id '
        'MERGE (u)-[r:FOLLOW]->(v) '
        'SET f.screen_name = u.username, f.name = u.account_display_name'
    )

    graph.run(
        'MATCH (f:Following)--(v:twUser {graph_information: [\'' + usr + '\',\'twitter\']}) '
        'MATCH (u:twUser) '
        'WHERE'
        ' not u.userProfileProperty = \'' + userProfileProperty + '\' AND '
        ' v.userProfileProperty = \'' + userProfileProperty + '\' AND '
        ' f.account_id = u.account_id '
        'MERGE (u)-[r:FOLLOW]->(v) '
        'SET f.screen_name = u.username, f.name = u.account_display_name'
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

    if os.path.exists(path+'/data'):
        path = path + '/data'

    try:
        userProfileProperty = createUserNode(path, usr)

        createTweetsNode(path, usr, userProfileProperty)

        createFollowerNode(path, usr, userProfileProperty)

        createFollowingNode(path, usr, userProfileProperty)

        setFollowsName(path, usr, userProfileProperty)

        setSameAccount(usr, userProfileProperty)

        setFirstInteration(usr, userProfileProperty)

        createLikedTweetNode(path, usr, userProfileProperty)

        setNodeDegree(usr, userProfileProperty)

        setTaggedTogether(usr, userProfileProperty)

        normalizeDump(usr, userProfileProperty)

        wordsFrequency.getWordsForWordFrequency(usr, userProfileProperty, 'twitter', wordFrecOption)

        # remove this comments to enable email sending when upload is finished. You must create a gmail email to use this option
        # contentToSend = 'Your dump has been successfully loaded. Logged as ' + usr + ' and choose twitter from the social network dropdown to navigate the dump uploaded'
        # ms.send(contentToSend, usr)

        print 'Dump successfully uploaded'

    except Exception as e:
        print "Error during the creation of graph. Please retry or choose another file"

