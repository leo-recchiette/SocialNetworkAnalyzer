#! /usr/bin/env python
# coding=utf-8

import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

import json

import dbConnector as dbc

db = dbc.sqlHelper()

def logging (usr, pwd):
    cursor = db.cursor()
    finduser = "select * from users where mail='" + usr + "'"
    cursor.execute(finduser)

    records = cursor.fetchall()

    if cursor.rowcount == 1:
        matchpwd = "select * from users where mail= %s and password= %s;"
        cursor.execute(matchpwd, (usr, pwd))
        records = cursor.fetchall()
        if cursor.rowcount == 1:
            # 1 meens user exist and the pwd matchs
            return 1
        else:
            # -1 meens user exist but pwd doesn't match
            return -1
    elif cursor.rowcount == 0:
        # 1 meens user doesn't exist
        return 0
    else:
        'something else'

    cursor.close()
    db.close()


def register(usr, pwd):

    cursor = db.cursor()
    finduser = "select * from users where mail= '" + usr +"'"
    cursor.execute(finduser)

    records = cursor.fetchall()

    if cursor.rowcount == 1:
        # 1 meens user already exist and the pwd matchs
        return 1
    elif cursor.rowcount == 0:
        sql = "INSERT INTO users (mail, password) VALUES (%s, %s);"
        val = (usr, pwd)
        cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()
        return 0


def changePass(usr, pwd):
    cursor = db.cursor()
    sql = "UPDATE users SET password = %s WHERE mail = %s;"
    cursor.execute(sql, (pwd, usr))
    db.commit()
    cursor.close()
    db.close()
    return 1


def changeMail(usr, pwd):
    cursor = db.cursor()
    sql = "UPDATE users SET mail = %s WHERE mail = %s;"
    cursor.execute(sql, (pwd, usr))
    db.commit()
    cursor.close()
    db.close()

    graph = dbc.neo4jHelper()

    graph.run(
        'MATCH (n) '
        'WHERE '
        ' ANY(gi IN n.graph_information WHERE gi = \'' + usr + '\') '
        'SET  n.graph_information = [\'' + newMail + '\',  n.graph_information[1] ] '
    )

    return 1


if __name__ == '__main__':

    action = str(sys.argv[3])

    if action == 'login' or action == 'register' or action == 'change-password':
        usr = str(sys.argv[1])
        pwd = str(sys.argv[2])

        if action == 'login':
            print logging(usr, pwd)
        elif action == 'register':
            print register(usr, pwd)
        elif action == 'change-password':
            print changePass(usr, pwd)

    elif action == 'change-mail':
        usr = str(sys.argv[1])
        newMail = str(sys.argv[2])

        print changeMail(usr, newMail)