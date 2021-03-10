#  coding: utf-8
#! /usr/bin/env python

import json
import sys

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

from py2neo import Graph, NodeMatcher

import mysql.connector

def neo4jHelper():
    return Graph(host='localhost:7687', auth=('neo4j', '*******'))

def sqlHelper():
    return mysql.connector.connect(
        user='root',
        password='*******',
        host='127.0.0.1',
        database='sna_tool'
    )