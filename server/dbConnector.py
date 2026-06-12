#  coding: utf-8
#! /usr/bin/env python

# Connection helpers for Neo4j (py2neo) and MySQL (mysql.connector).
#
# Connection details come from environment variables so the same code runs
# under docker-compose (which sets NEO4J_HOST=neo4j / MYSQL_HOST=mysql) and on a
# plain local install (defaults below point at localhost). Override any value
# via the environment instead of editing this file.

import os

from py2neo import Graph, NodeMatcher  # NodeMatcher kept available for callers

import mysql.connector


def neo4jHelper():
    # NOTE: py2neo expects host and port as SEPARATE arguments. Passing
    # host='localhost:7687' (as the original code did) builds the malformed URI
    # bolt://localhost:7687:7687 and never connects.
    return Graph(
        host=os.environ.get('NEO4J_HOST', 'localhost'),
        port=int(os.environ.get('NEO4J_PORT', '7687')),
        auth=(
            os.environ.get('NEO4J_USER', 'neo4j'),
            os.environ.get('NEO4J_PASSWORD', 'snapassword'),
        ),
    )


def sqlHelper():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', '127.0.0.1'),
        port=int(os.environ.get('MYSQL_PORT', '3306')),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', 'snapassword'),
        database=os.environ.get('MYSQL_DATABASE', 'sna_tool'),
        # Match the utf8mb4 schema (docker/mysql/init/01-schema.sql); without this
        # the connection negotiates utf8mb3 and 4-byte chars are rejected.
        charset='utf8mb4',
        # Pin the collation too: mysql-connector-python 8.0.x defaults utf8mb4 to
        # utf8mb4_0900_ai_ci, which only exists in MySQL 8.0 and makes the 5.7
        # server reject the connection ("Unknown collation: 'utf8mb4_0900_ai_ci'").
        # The schema uses utf8mb4_unicode_ci, which MySQL 5.7 supports.
        collation='utf8mb4_unicode_ci',
    )
