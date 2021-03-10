#  coding: utf-8
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

from py2neo.data import Node
import nlp
import json

sys.path.append('~/sna/server/')
import dbConnector as dbc
graph = dbc.neo4jHelper()

db = dbc.sqlHelper()


def getWordsForWordFrequency( usr, userProfileProperty , sn , wordFrecOption):

    documents = ''

    if sn == 'facebook':
        documents = getWordsForFacebook(usr, userProfileProperty)
    elif sn == 'twitter':
        documents = getWordsForTwitter(usr, userProfileProperty)
    elif sn == 'mbox':
        documents = getWordsForMbox(usr, userProfileProperty)

    # call the script to remove stop word and return tfidf frequency
    tfidfList = nlp.calculateTFIDF(documents)

    dataset = {}
    for word in tfidfList:
        if len(tfidfList[word]) == 1:
            dataset[word] = tfidfList[word][0]
        elif len(tfidfList[word]) > 1:
            m = 0
            for value in tfidfList[word]:
                m = m + value
            m = m / len(tfidfList[word])
            dataset[word] = m

    uploadWords(dataset , usr , userProfileProperty , sn , wordFrecOption)

##########  GET WORDS FROM SOCIAL ###########

def getWordsForFacebook(usr, userProfileProperty):

   return graph.run(
        'MATCH (p {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'facebook\']}) '
        'WHERE '
        ' p:Direct_Message or p:Comment or p:Post or p:FriendPost '
        'RETURN p.content AS document, p.timestamp AS timestamp ORDER BY p.timestamp ASC'
   ).data()


def getWordsForTwitter(usr, userProfileProperty):

    return graph.run(
        'MATCH (p {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'twitter\']}) '
        'WHERE '
        ' p:Tweet or p:Retweet or p:Post '                                                                                  
        'RETURN p.full_text AS document, p.created_at AS timestamp '
    ).data()


def getWordsForMbox(usr, userProfileProperty):
    return graph.run(
        'MATCH (p:Mail {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'mbox\']}) '
        'RETURN p.content AS document, p.time AS timestamp ORDER BY p.times ASC'
    ).data()


######## UPLOAD WORD ########

def uploadWords(dataset, usr , userProfileProperty, sn, wordFrecOption):
    if wordFrecOption == 'true':
        for word in dataset:
            w = Node("Word", word=word, value=str(round(dataset[word]*100,2)), userProfileProperty=userProfileProperty, graph_information=[usr, sn])
            graph.create(w)

        if sn == 'facebook':
            graph.run(
                'MATCH (w:Word {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'facebook\']}) '
                'MATCH (n {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'facebook\']} ) '
                'WHERE '
                ' (n:Post or n:Comment or n:FriendPost or n:Direct_Message) AND '
                ' n.content CONTAINS w.word '                                                                                                              
                'MERGE (n)<-[r:WORD {relationship_type:[\'WORD_USED_IN\']}]-(w) '
            )
        elif sn == 'twitter':
            graph.run(
                'MATCH (w:Word {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'twitter\']}) '
                'MATCH (n {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'twitter\']} ) '
                'WHERE '
                ' exists (n.full_text) AND ' +
                ' n.full_text CONTAINS w.word '
                'MERGE (n)<-[r:WORD {relationship_type:[\'WORD_USED_IN\']}]-(w) '
            )
        else:
            graph.run(
                'MATCH (w:Word {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'mbox\']}) '
                'MATCH (n:Mail {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'mbox\']} ) '
                'WHERE '
                ' n.content CONTAINS W.WORD '
                'MERGE (n)<-[r:WORD {relationship_type:[\'WORD_USED_IN\']}]-(w) '
            )

    else:
        cursor = db.cursor()
        for word in dataset:
            query = "INSERT INTO word_frequency (word , `value` , `user Profile Property` , `User Registered on SNA` , `Social Network`) VALUES (%s, %s, %s, %s, %s);"
            val = (word, str(round(dataset[word]*100,2)) , userProfileProperty , usr , sn )
            cursor.execute(query, val)
            db.commit()

        cursor.close()
        db.close()


