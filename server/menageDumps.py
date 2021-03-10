#  coding: utf-8
#! /usr/bin/env python

import json
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

import dbConnector as dbc
graph = dbc.neo4jHelper()

db = dbc.sqlHelper()

def deleteSQLstoredData(usr, valueToDelete):
    cursor = db.cursor()

    if valueToDelete == 'all':
        sql = "DELETE FROM word_frequency WHERE `User Registered on SNA`=%s;"
        val = (usr)
        cursor.execute(sql, val)
    else:
        sql = "DELETE FROM word_frequency WHERE `User Registered on SNA`=%s AND `Social Network`= %s;"
        val = (usr, valueToDelete)
        cursor.execute(sql, val)

    db.commit()
    cursor.close()


usr = str(sys.argv[1])
valueToDelete = str(sys.argv[2])


if __name__ == '__main__':

    if valueToDelete=='all':
        isEmpty = graph.run(
            'MATCH (n) '
            'WHERE '
            ' ANY(info IN n.graph_information WHERE info = \'' + usr + '\') '
            'RETURN count(n) as counter'
        ).data()

        if isEmpty[0]['counter'] > 0:
            graph.run(
                'MATCH (n) '
                'WHERE '
                ' ANY(info IN n.graph_information WHERE info = \'' + usr + '\') '
                'DETACH DELETE n'
            )
            print ('Delete all dumps')
        else:
            print ('Nothing to delete')
    else:
        isEmpty = graph.run(
                    'MATCH (n {graph_information:[\'' + usr + '\', \''+ valueToDelete +'\']}) RETURN count(n) as counter'
                ).data()

        if isEmpty[0]['counter']>0 :
            graph.run(
                'MATCH (n {graph_information:[\'' + usr + '\', \''+ valueToDelete +'\']}) DETACH DELETE n'
            )

            deleteSQLstoredData(usr, valueToDelete)

            print ('Delete')
        else:
            print ('Nothing to delete')
