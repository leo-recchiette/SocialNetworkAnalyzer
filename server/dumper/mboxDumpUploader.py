#! /usr/bin/env python
# coding= UTF-8

import sys
import json
import mailbox
from datetime import datetime, timedelta
import re
import email

sys.path.append('~/anaconda2/envs/sna/lib/python2.7/site-packages')

from py2neo.data import Node

sys.path.append('~/sna/server/dataSearcher/nlp')
import wordsFrequency

sys.path.append('~/sna/server/')
import mailSender as ms

sys.path.append('~/sna/server/')
import dbConnector as dbc
graph = dbc.neo4jHelper()

# M_box functions


class emailobj:
    origin = None
    target = None
    cc = None
    bcc = None
    subject = ''
    date = None
    content = ''

    def __init__(self, origin, target, cc, bcc, subject, date, content):
        self.origin = origin
        self.target = target
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.date = date
        self.content = content

    def __repr__(self):
        return '<Event object ({} {} {} {} {} {} {})>'.format(self.origin, self.target, self.cc, self.bcc, self.subject, self.date, self.content)

    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.origin, self.target, self.cc, self.bcc, self.subject, self.date, self.content)


def retrievedata(mymail):
    emailArchive = []
    emailmsg = None

    for message in mymail:
        emailmsg = emailobj(normalizeContacts(message['from']),
                            normalizeContacts(message['to']),
                            normalizeContacts(message['cc']),
                            normalizeContacts(message['bcc']),
                            normalizeSubject(message['subject']),
                            normalizeDate(message['date']),
                            normalizeBody(message))
        emailArchive.append(emailmsg)
    return emailArchive


def normalizeContacts(contacts):
    if contacts == None :
        return []
    else:
        tl = re.findall(r'[a-zA-Z0-9_-]+[.|\w]\w+@[a-zA-Z0-9_-]+[.]\w+[.|\w+]+', contacts)
        return list(set(tl))


def normalizeSubject(mysubject):
    if mysubject == None:
        return None
    else:
        ee = email.Header.decode_header(mysubject)
        return re.sub('Re: |RE: ', '', ee[0][0])


def normalizeDate(mydatetime):
    try:
        filterdate = re.sub(r' \+.*$| -.*$', '', mydatetime)
        #print filterdate
        myTime = datetime.strptime(filterdate, '%a, %d %b %Y %H:%M:%S')
        if (myTime.year < 20):
            #add 2000 years
            years = 2000
            days_per_year = 365.24
            newtime = myTime + timedelta(days=(years*days_per_year))
            myTime = newtime
        return myTime.strftime('%Y/%m/%d %H:%M:%S')
    except (ValueError, TypeError, NameError):
        return ''


def normalizeBody(message):
    msgbody = getbody(message)
    msgbody = removeReplies(msgbody,message)
    #remove too many white spaces
    msgbody = re.sub('[ ]{2,}', ' ', msgbody)
    #msgbody = re.sub('(\n|<|>|}|{|\')',' ',msgbody)
    msgbody = re.sub('[^a-zA-Z0-9]+',' ', msgbody)
    #if(message['subject'] == 'Re: Bike sharing project'):
    #    print msgbody
    return msgbody


def getbody(message): #getting plain text 'email body'
    body = 'None'
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    return body


def removeReplies(msgbody,message):
    noReplies = msgbody
    #if message['In-Reply-To'] != None:
    #noReplies = ''.join(noReplies.partition('From:')[0:2])
    noReplies = re.sub(r' From:.*$| wrote:.*$| Original Message .*$| ha scritto:.*$| Da:.*$|-----Original Message-----.*$', '', noReplies)
    noReplies = re.sub('[_]{2,}', ' ', noReplies)
    return noReplies


def genEmailArch(emailsData):
    # emailArch [[origin],[target],[cc/bcc],'subject',date, 'content','urls','emails']
    emailArch = []
    for emailDir in emailsData:
        for emailmsg in emailDir:
            emailArch.append([
                list(set(emailmsg.origin)),
                list(set(emailmsg.target)),
                list(set(emailmsg.cc + emailmsg.bcc)),
                str(emailmsg.subject),
                emailmsg.date,
                emailmsg.content,
                infoInBody(emailmsg.content)[0],
                infoInBody(emailmsg.content)[1]
            ])
    return emailArch


def infoInBody(msgbody):
    urls = re.findall(ur'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', msgbody)
    myurls = []
    for url in urls:
        myurls.append(url[1])
    emails = re.findall(r'[a-zA-Z0-9_-]+[.|\w]\w+@[a-zA-Z0-9_-]+[.]\w+[.|\w+]+', msgbody);
    # msgbody = re.sub('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', msgbody)

    urlString = ''
    for url in myurls:
        urlString = urlString + url + '<newelem>'

    emailString = ''
    for email in emails:
        emailString = emailString + email + '<newelem>'

    return (urlString, emailString)


def genNodes(emailArch):
    nodes = {}
    idCount = 0
    for emailRow in emailArch:
        allnodes = list(set(emailRow[0] + emailRow[1] + emailRow[2]))
        for n in allnodes:
            if(n not in nodes):
                nodes[n] = idCount
                idCount += 1
    return nodes


def genEdges(emailArch, nodes):
    edges = {}
    edgesInfo = []

    idCount = 0
    for emailRow in emailArch:
        for origin in emailRow[0]:
            targetNodes = list(set(emailRow[1] + emailRow[2]))
            for target in targetNodes:
                tuplaKey = (nodes[origin], nodes[target])
                if (tuplaKey not in edges):
                    edges[tuplaKey] = idCount
                    idCount += 1

                edgesInfo.append([
                    edges[tuplaKey],
                    tuplaKey[0],
                    tuplaKey[1],
                    emailRow[3],
                    emailRow[4],
                    emailRow[5],
                    emailRow[6],
                    emailRow[7]])
    return edgesInfo


def genEdgesNodesJson(edges, nodes, myContacts):
    nodesDic = {}
    for k in nodes.keys():
        nodesDic[nodes[k]] = k

    myContactIds = []
    for myContact in myContacts:
        if myContact in nodes:
            myContactIds.append(nodes[myContact])

    undEdgesId = 0
    dicUndEdgesId = {}
    for k in edges:
        lista = [k[1], k[2]]
        lista.sort()
        tupla = tuple(lista)
        if tupla not in dicUndEdgesId:
            dicUndEdgesId[tupla] = undEdgesId
            undEdgesId = undEdgesId + 1

    arrEdgesDirected = []
    arrEdgesUndirected = []
    objDicDirectedNodes = {}
    objDicUndirectedNodes = {}
    arrCollSubj = collaborativeSubj(edges)
    for k in edges:
        objDic = {}

        # Directed case
        objDic['id'] = k[0]
        objDic['origin'] = k[1]
        objDic['target'] = k[2]
        objDic['originLbl'] = nodesDic[objDic['origin']]
        objDic['targetLbl'] = nodesDic[objDic['target']]
        objDic['subject'] = k[3]
        objDic['time'] = k[4]
        objDic['content'] = k[5]
        objDic['urls'] = k[6]
        objDic['emails'] = k[7]

        arrEdgesDirected.append(objDic)

        objDicDirectedNodes[objDic['origin']] = objDic['originLbl']
        objDicDirectedNodes[objDic['target']] = objDic['targetLbl']

        # Undirected case
        if ((not (k[1] in myContactIds)) and (not (k[2] in myContactIds))):
            if k[3] in arrCollSubj:
                lista = [k[1], k[2]]
                lista.sort()
                tupla = tuple(lista)
                objDic = {}
                objDic['id'] = dicUndEdgesId[tupla]
                objDic['origin'] = tupla[0]
                objDic['target'] = tupla[1]
                objDic['originLbl'] = nodesDic[objDic['origin']]
                objDic['targetLbl'] = nodesDic[objDic['target']]
                objDic['subject'] = k[3]
                objDic['time'] = k[4]
                objDic['content'] = k[5]
                objDic['urls'] = k[6]
                objDic['emails'] = k[7]

                arrEdgesUndirected.append(objDic)
                objDicUndirectedNodes[objDic['origin']] = objDic['originLbl']
                objDicUndirectedNodes[objDic['target']] = objDic['targetLbl']

    arrNodesDirected = []
    for k in objDicDirectedNodes.keys():
        objDic = {}
        objDic['id'] = k
        objDic['label'] = objDicDirectedNodes[k]
        arrNodesDirected.append(objDic)

    arrNodesUndirected = []
    for k in objDicUndirectedNodes.keys():
        objDic = {}
        objDic['id'] = k
        objDic['label'] = objDicUndirectedNodes[k]
        arrNodesUndirected.append(objDic)

    globalDic = {}
    internalDic = {}
    internalDic['directed'] = arrEdgesDirected
    internalDic['undirected'] = arrEdgesUndirected
    globalDic['edges'] = internalDic

    internalDic = {}
    internalDic['directed'] = arrNodesDirected
    internalDic['undirected'] = arrNodesUndirected
    globalDic['nodes'] = internalDic

    return globalDic


def collaborativeSubj(edges):
    dicSubj = {}

    for k in edges:
        if k[3] not in dicSubj:
            dicSubj[k[3]] = []
            dicSubj[k[3]].append(k[4])
        else:
            if k[4] not in dicSubj[k[3]]:
                dicSubj[k[3]].append(k[4])

    arrSubj = []
    for k in dicSubj.keys():
        if (int(len(dicSubj[k])) > 1):
            arrSubj.append(k)
    return arrSubj


def convertToJSON(emailArch):
    emailsJSON = []
    for e in emailArch:
        emailObj = {}
        emailObj['from'] = e[0]
        emailObj['to'] = e[1]
        emailObj['cc'] = e[2]
        emailObj['subject'] = e[3]
        emailObj['time'] = e[4]
        emailObj['content'] = e[5]
        emailsJSON.append(emailObj)
    return emailsJSON


# UPLOAD on NEO4J

def createUndirectedGraph(usr, userProfileProperty, **resultDic):
    for nodes in resultDic['nodesEdges']['nodes']['undirected']:
        id = nodes['id']
        label = nodes['label']
        node = Node(
            'Undirected_Node',
            id=id,
            label=label,
            graph_information=[usr, 'mbox'],
            userProfileProperty= userProfileProperty
        )
        graph.create(node)

    for edge in resultDic['nodesEdges']['edges']['undirected']:
        graph.run(
            'MATCH (n:Undirected_Node {graph_information: [\'' + usr + '\',\'mbox\'], id:' + str(edge['origin']) + ', label:\'' + edge['originLbl'] + '\'}) '
            'MATCH (m:Undirected_Node {graph_information: [\'' + usr + '\',\'mbox\'], id:' + str(edge['target']) + ', label:\'' + edge['targetLbl'] + '\'}) '
            'WHERE '
            ' n.userProfileProperty = \'' + userProfileProperty +'\' AND '
            ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                     
            'MERGE (n)-[r:UNDIRECTED_EDGE {relationship_type:[\'undirected_edge\']}]-(m) '
            'ON CREATE SET r.edge_weight = 1 '
            'ON MATCH SET r.edge_weight = r.edge_weight + 1 '
            'RETURN null'
        )

    graph.run(
        'MATCH (n:Undirected_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WHERE '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' '                                                                  
        'SET n.nodeDegree = size((n)--())'
    )

    graph.run(
        'MATCH (n:Undirected_Node {graph_information: [\'' + usr + '\',\'mbox\']})-[r:UNDIRECTED_EDGE]-() '
        'WHERE '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' '                                                                   
        'WITH n AS node, sum(r.edge_weight) AS sum '
        'SET node.allEdgeWeightValue = sum'
    )


def createDirectedGraph(usr, userProfileProperty, **resultDic):
    for nodes in resultDic['nodesEdges']['nodes']['directed']:
        id = nodes['id']
        label = nodes['label']
        node = Node(
            'Directed_Node',
            id=id,
            label=label,
            graph_information=[usr, 'mbox'],
            userProfileProperty= userProfileProperty
        )
        graph.create(node)

    for edge in resultDic['nodesEdges']['edges']['directed']:
        graph.run(
            'MATCH (n:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\'], id:' + str(edge['origin']) + ', label:\'' + edge['originLbl'] + '\'}) '
            'MATCH (m:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\'], id:' + str(edge['target']) + ', label:\'' + edge['targetLbl'] + '\'}) '
            'WHERE '
            ' n.userProfileProperty = \'' + userProfileProperty +'\' AND '
            ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                                                                                                                    
            'MERGE (n)-[r:DIRECTED_EDGE {relationship_type:[\'directed_edge\']}]->(m) '
            'ON CREATE SET r.edge_weight = 1 '
            'ON MATCH SET r.edge_weight = r.edge_weight + 1 '
        )

    graph.run(
        'MATCH (n:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WHERE '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' '                                                                     
        'SET n.outNodeDegree = size((n)-->()) '
        'SET n.inNodeDegree = size((n)<--()) '
        'SET n.nodeDegree = n.inNodeDegree + n.outNodeDegree'
    )

    graph.run(
        'MATCH (m:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\']})<-[r:DIRECTED_EDGE]-() '
        'WHERE '
        ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                                 
        'WITH m AS node, sum(r.edge_weight) AS sum '
        'SET node.inEdgeWeightValue = sum '
    )

    graph.run(
        'MATCH (n:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '                                                                
        'WHERE not exists (n.inEdgeWeightValue) AND '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' '                                                                  
        'SET n.inEdgeWeightValue = 0 '
    )

    graph.run(
        'MATCH (m:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\']})-[r:DIRECTED_EDGE]->() '
        'WHERE '
        ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                                 
        'WITH m AS node, sum(r.edge_weight) AS sum '
        'SET node.outEdgeWeightValue = sum '
        'SET node.allEdgeWeightValue = node.outEdgeWeightValue+node.inEdgeWeightValue'
    )

    graph.run(
        'MATCH (n:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WHERE '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' '                                                                 
        'WITH n AS node '
        'WHERE not exists (node.outEdgeWeightValue) '
        'SET node.outEdgeWeightValue = 0 '
        'SET node.allEdgeWeightValue = node.outEdgeWeightValue + node.inEdgeWeightValue'
    )



def createAllEmailsNode(usr, userProfileProperty, **resultDic):
    for mail in resultDic['allEmails']:
        cc = []
        to = []

        sender = mail['from'][0]
        content = mail['content']
        time = mail['time']
        subject = mail['subject']

        for target in mail['to']:
            to.append(target)

        for carbonCopy in mail['cc']:
            cc.append(carbonCopy)

        node = Node(
            'Mail',
            sender = sender,
            to = to,
            time = time,
            subject = subject,
            content = content,
            cc = cc,
            graph_information = [usr, 'mbox'],
            userProfileProperty= userProfileProperty
        )
        graph.create(node)

    graph.run(
        'MATCH (m:Mail {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'MATCH (n:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WHERE '
        ' m.sender = n.label AND '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' AND '
        ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                                 
        'MERGE (n)-[s:SEND {relationship_type:[\'send\']}]->(m) '
    )

    graph.run(
        'MATCH (m:Mail {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'MATCH (n:Directed_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WHERE '
        ' ANY(cc IN m.cc WHERE cc = n.label) OR '
        ' ANY(to IN m.to WHERE to = n.label) AND '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' AND '
        ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                                 
        'MERGE (n)<-[s:RECIEVE {relationship_type:[\'recieve\']}]-(m) '
    )

    graph.run(
        'MATCH (m:Mail {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'MATCH (n:Undirected_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WHERE '
        ' m.sender = n.label AND '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' AND '
        ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                                   
        'MERGE (n)-[s:SEND {relationship_type:[\'send\']}]->(m) '
    )

    graph.run(
        'MATCH (m:Mail {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'MATCH (n:Undirected_Node {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WHERE '
        ' ANY(cc IN m.cc WHERE cc = n.label) OR '
        ' ANY(to IN m.to WHERE to = n.label) AND '
        ' n.userProfileProperty = \'' + userProfileProperty +'\' AND '
        ' m.userProfileProperty = \'' + userProfileProperty +'\' '                                                                   
        'MERGE (n)<-[s:RECIEVE {relationship_type:[\'recieve\']}]-(m) '
    )

    graph.run(
        'MATCH (u:Undirected_Node)--(m:Mail {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WITH min(m.time) AS min, u, m '
        'WHERE '
        ' u.userProfileProperty = \'' + userProfileProperty +'\' AND '
        ' m.userProfileProperty = \'' + userProfileProperty +'\' '
        'SET u.firstInteration = min '
    )

    graph.run(
        'MATCH (u:Directed_Node)--(m:Mail {graph_information: [\'' + usr + '\',\'mbox\']}) '
        'WITH min(m.time) AS min, u, m '
        'WHERE '
        ' u.userProfileProperty = \'' + userProfileProperty + '\' AND '
        ' m.userProfileProperty = \'' + userProfileProperty + '\' '
        'SET u.firstInteration = min '
    )

if __name__ == '__main__':
    functionName = str(sys.argv[1])
    mboxUrl = str(sys.argv[2])
    mboxMyContacts = str(sys.argv[3])
    usr = str(sys.argv[4])
    wordFrecOption = str(sys.argv[5])

    if functionName == 'getNodesEdges':
        emailData = []
        # for mboxUrl in mboxUrls:
        emailData.append(retrievedata(mailbox.mbox(mboxUrl)))
        emailArch = genEmailArch(emailData)
        nodes = genNodes(emailArch)
        edges = genEdges(emailArch, nodes)
        allData = genEdgesNodesJson(edges, nodes, mboxMyContacts)

        resultDic = {}
        resultDic['allEmails'] = convertToJSON(emailArch)
        resultDic['nodesEdges'] = allData

        ##########################################################

        try:
            createUndirectedGraph(usr, mboxMyContacts, **resultDic)
            createDirectedGraph(usr, mboxMyContacts, **resultDic)

            createAllEmailsNode(usr, mboxMyContacts, **resultDic)

            wordsFrequency.getWordsForWordFrequency(usr, mboxMyContacts, 'mbox', wordFrecOption)

            # remove this comments to enable email sending when upload is finished. You must create a gmail email to use this option
            # contentToSend = 'Your dump has been successfully loaded. Logged as ' + usr + ' and choose mbox from the social network dropdown to navigate the dump uploaded'
            # ms.send(contentToSend, usr)

            print 'Dump successfully uploaded'
        except Exception as e:
            print "Error during the creation of graph. Please retry or choose another file"
