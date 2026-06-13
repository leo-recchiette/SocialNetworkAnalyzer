#  coding: utf-8
#! /usr/bin/env python

# Runs a Cypher query (built by the frontend's allQueries.js) and returns the
# resulting graph as {nodes, rels} JSON for the Sigma.js visualization layer.
#
# This replaces the old neovis.js setup, where the browser connected to Neo4j
# directly over bolt and shipped the DB password to the client. The query is now
# proxied through server.php -> here, keeping credentials server-side like every
# other backend script (dbConnector reads them from the environment).
#
# IMPORTANT: node/rel ids are the integer ID() Neo4j assigns, emitted as strings.
# getData.py interpolates the clicked id straight into "ID(n) = <id>", so the
# visualization MUST key each node/edge by that exact value or node selection
# (the side .data panel) breaks silently. Neo4j 3.5 has no elementId(); the
# integer ID() is the right (and only) identifier here.

import json
import sys

sys.path.append('~/sna/server/')  # no-op (~ is not expanded); imports resolve via PYTHONPATH
import dbConnector as dbc

from py2neo.data import Node, Relationship, Path

graph = dbc.neo4jHelper()


def relType(rel):
    # py2neo 4.x returns relationships as instances of a class named after the
    # relationship type (e.g. FRIEND), so type(rel).__name__ is the type string.
    return type(rel).__name__


def main():
    cmd = sys.argv[1]

    # dedupe by integer identity: the same node/rel shows up across several
    # RETURNed paths (x, y, z) in the allQueries.js queries.
    nodes = {}
    rels = {}

    def addNode(node):
        if node is None:
            return
        nodes[node.identity] = {
            'id': str(node.identity),
            'labels': [str(label) for label in node.labels],
            'properties': dict(node),
        }

    def addRel(rel):
        if rel is None:
            return
        addNode(rel.start_node)
        addNode(rel.end_node)
        rels[rel.identity] = {
            'id': str(rel.identity),
            'from': str(rel.start_node.identity),
            'to': str(rel.end_node.identity),
            'type': relType(rel),
            'properties': dict(rel),
        }

    def walk(value):
        # OPTIONAL MATCH columns come back as None when nothing matched.
        if value is None:
            return
        if isinstance(value, Node):
            addNode(value)
        elif isinstance(value, Relationship):
            addRel(value)
        elif isinstance(value, Path):
            for node in value.nodes:
                addNode(node)
            for rel in value.relationships:
                addRel(rel)
        elif isinstance(value, (list, tuple)):
            for item in value:
                walk(item)

    for record in graph.run(cmd):
        for value in record.values():
            walk(value)

    print json.dumps({
        'nodes': list(nodes.values()),
        'rels': list(rels.values()),
    })


if __name__ == '__main__':
    main()
