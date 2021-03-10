#  coding: utf-8
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

from py2neo.data import Node
import json

sys.path.append('~/sna/server/')
import dbConnector as dbc
graph = dbc.neo4jHelper()

db = dbc.sqlHelper()


def retrieveWord(keyword, person, start_date, end_date , minNodevalue, minEdgeValue , sn , graphType , usr , dataViz1 , dataViz2):
    cursor = db.cursor()

    query = "SELECT COUNT(*) FROM tesi.word_frequency WHERE `User Registered on SNA` = %s and `Social Network`=%s;"
    cursor.execute(query , (usr , sn))
    result = cursor.fetchone()

    if result[0] > 0:
        query = "SELECT * FROM tesi.word_frequency WHERE `User Registered on SNA` = %s and `Social Network`=%s;"
        cursor.execute(query, (usr, sn))
        rows = cursor.fetchall()

        uploadWordsFromSQL(rows , usr , sn)

        query = "DELETE FROM tesi.word_frequency WHERE `User Registered on SNA` = %s and `Social Network`=%s;"
        cursor.execute(query, (usr, sn))
        db.commit()

        return getDataFromSocialNetwork(keyword, person, start_date, end_date , minNodevalue, minEdgeValue , sn , graphType , usr , dataViz1 , dataViz2)
    else:
        return getDataFromSocialNetwork(keyword, person, start_date, end_date , minNodevalue, minEdgeValue , sn , graphType , usr , dataViz1 , dataViz2)

    cursor.close()
    db.close()


def uploadWordsFromSQL(rows , usr , sn):
    userProfileProperty = rows[0][2]

    for row in rows:
        w = Node("Word", word=row[0], value=row[1], userProfileProperty=row[2], graph_information=[row[3], row[4]])
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
            ' exists (n.full_text) AND ' 
            ' n.full_text CONTAINS w.word '
            'MERGE (n)<-[r:WORD {relationship_type:[\'WORD_USED_IN\']}]-(w) '
        )
    else:
        graph.run(
            'MATCH (w:Word {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'mbox\']}) '
            'MATCH (n:Mail {userProfileProperty:\'' + userProfileProperty + '\', graph_information:[\'' + usr + '\', \'mbox\']} ) '
            'WHERE '
            ' n.content CONTAINS w.word '
            'MERGE (n)<-[r:WORD {relationship_type:[\'WORD_USED_IN\']}]-(w) '
        )


def getDataFromSocialNetwork(keyword, person, start_date, end_date , minNodevalue, minEdgeValue , sn , graphType , usr , dataViz1 , dataViz2):
    if sn == 'facebook':
        return graph.run(
            'MATCH (n {graph_information:[\'' + usr + '\', \'facebook\']})-[:WORD]-(w:Word {graph_information:[\'' + usr + '\', \'facebook\']}) '
            'WHERE '
            ' exists(n.content) AND '
            ' (ANY(word IN split(n.content, \' \') WHERE word = w.word)) AND '                                                                                                                           
            ' (n.timestamp>\'' + start_date + '\' AND n.timestamp<\'' + end_date + '\') ' +
            'RETURN DISTINCT split(split(n.timestamp, \' \')[0],\'/\')[0]+\'/\'+split(split(n.timestamp, \' \')[0],\'/\')[1] as timestamp, '
            'w.word as word, w.value as value , toFloat(w.value) as floatVal ORDER BY timestamp, floatVal DESC'
        ).data()
    elif sn == 'twitter':
        return graph.run(
            'MATCH (n {graph_information:[\'' + usr + '\', \'twitter\']})-[:WORD]-(w:Word {graph_information:[\'' + usr + '\', \'twitter\']}) '
            'WHERE '
            ' exists(n.full_text) AND '
            ' ANY(word IN split(n.full_text, \' \') WHERE word = w.word ) AND '                                                                                                                          
            ' (n.created_at>\'' + start_date + '\' AND n.created_at<\'' + end_date + '\') ' +
            'RETURN DISTINCT split(split(n.created_at, \' \')[0],\'/\')[0]+\'/\'+split(split(n.created_at, \' \')[0],\'/\')[1] as timestamp, '
            'w.word as word, w.value as value , toFloat(w.value) as floatVal ORDER BY timestamp, floatVal DESC'
        ).data()
    elif sn == 'mbox':
        return graph.run(
            'MATCH (n:Mail {graph_information:[\'' + usr + '\', \'mbox\']})-[:WORD]-(w:Word {graph_information:[\'' + usr + '\', \'mbox\']} ) '
            'WHERE '
            ' ANY(word IN split(n.content, \' \') WHERE word = w.word ) AND '                                                                                                                             
            ' n.time > \''+start_date+'\' AND n.time < \''+end_date+'\' '
            'RETURN DISTINCT split(split(n.time, \' \')[0],\'/\')[0]+\'/\'+split(split(n.time, \' \')[0],\'/\')[1] as timestamp, '
            'w.word as word, w.value as value , toFloat(w.value) as floatVal ORDER BY timestamp, floatVal DESC'
        ).data()


data = str(sys.argv[1])

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


    print json.dumps(
        retrieveWord(keyword, person, start_date, end_date , minNodevalue, minEdgeValue , sn , graphType , usr , dataViz1 , dataViz2)
    )
