import { sna } from './bridge.js'


/**********  FACEBOOK QUERIES ***************/

function createFacebookRelationshipNetworkQuery (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr)
{
    let fbCmd = '';

    let usrToDisplay = sna.fbUserType;

    if ( usrToDisplay==='All' )
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH (:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'MATCH x=(f)-[:FRIEND]-(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WHERE ' +
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.name=~ \'(?i).*' + person + '.*\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH (:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'MATCH x=(f)-[:FRIEND]-(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WHERE ' +
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '

        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:FRIEND]-(f) ' +
                'WHERE ' +
                ' f.name=~ \'(?i).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:FRIEND]-(f) ' +
                'WHERE ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
    }
    else if ( usrToDisplay==='Friend' )
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH (:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'MATCH (p)-[:TAG]-(f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'MATCH x=(f:Friend)-[:FRIEND]-(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WHERE ' +
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' +
                ' p.post CONTAINS \''+keyword+'\' OR p.comment CONTAINS \''+keyword+'\' ) AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.name=~ \'(?i).*' + person + '.*\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH (:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'MATCH (p)-[:TAG]-(f:Friend {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'MATCH x=(f:Friend)-[:FRIEND]-(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WHERE ' +
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '

        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:FRIEND]-(f:Friend) ' +
                'WHERE ' +
                ' f.name=~ \'(?i).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:FRIEND]-(f:Friend) ' +
                'WHERE ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
    }
    else if ( usrToDisplay==='remFriend' )
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH (:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'MATCH (p)-[:TAG]-(f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'MATCH x=(f:RemovedFriend)-[:FRIEND]-(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WHERE ' +
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' +
                ' p.post CONTAINS \''+keyword+'\' OR p.comment CONTAINS \''+keyword+'\' ) AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.name=~ \'(?ism).*' + person + '.*\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH (:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'MATCH (p)-[:TAG]-(f:RemovedFriend {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'MATCH x=(f:RemovedFriend)-[:FRIEND]-(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WHERE ' +
                ' ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '

        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:FRIEND]-(f:RemovedFriend) ' +
                'WHERE ' +
                ' f.name=~ \'(?i).*' + person + '.*\' AND ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:FRIEND]-(f:RemovedFriend) ' +
                'WHERE ' +
                ' ((f.timestamp>\'' + start_date + '\' AND f.timestamp<\'' + end_date + '\') OR ' +
                '  (f.removed_timestamp>\'' + start_date + '\' AND f.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' ((d.timestamp>\'' + start_date + '\' AND d.timestamp<\'' + end_date + '\') OR ' +
                '  (d.removed_timestamp>\'' + start_date + '\' AND d.removed_timestamp<\'' + end_date + '\')) AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:fbUser{graph_information:[\'' + usr +'\', \'facebook\']})-[:FBUSERFRIEND]-(b:fbUser) ' +
                'RETURN x,y,z '
        }
    }

    return fbCmd;
}

function createFacebookTrafficNetworkQuery (keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr)
{
    let fbCmd = '';

    let nodeToDisplay = sna.fbNodeType;

    if (nodeToDisplay === 'all')
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?ism).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' ( ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
    }
    else if(nodeToDisplay === 'post')
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:Post) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:Post) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' ( ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:Post) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:Post) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
    }
    else if (nodeToDisplay === 'friendPost')
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:FriendPost) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:FriendPost) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' ( ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:FriendPost) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:FriendPost) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
    }
    else if (nodeToDisplay === 'comment')
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:Comment) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:Comment) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' ( ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:Comment) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:Comment) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
    }
    else if (nodeToDisplay === 'dm')
    {
        if (keyword !== '' && person !== '') {
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:Direct_Message) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' (ANY(content IN p.content WHERE content =~ \'(?i).*' + person + '.*\') OR ' +
                ' ANY(title IN p.title WHERE title =~ \'(?i).*' + person + '.*\') OR  ' +
                ' ANY(tags IN p.tags WHERE tags =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword !== '' && person ===''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr + '\', \'facebook\']} )-[:PUBLISHED]-(p:Direct_Message) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' ( ANY(content IN p.content WHERE content =~ \'(?i).*' + keyword + '.*\') OR ' +
                ' p.content CONTAINS \''+keyword+'\' ) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person !== ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:Direct_Message) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                '(ANY(participant IN p.participants WHERE participant =~ \'(?i).*' + person + '.*\')) AND ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
        else if (keyword === '' && person === ''){
            fbCmd =
                'MATCH x=(:fbUser {graph_information:[\'' + usr +'\', \'facebook\']})-[:PUBLISHED]-(p:Direct_Message) ' +
                'OPTIONAL MATCH (p)-[:TAG]-(f {graph_information:[\'' + usr + '\', \'facebook\']}) ' +
                'WITH x,p,f ' +
                'WHERE ' +
                ' p.nodeDegree>=' + minNodevalue + ' AND ' +
                ' p.timestamp>\'' + start_date + '\' AND p.timestamp<\'' + end_date + '\' ' +
                'OPTIONAL match z=(p)-[:TAG]-(:fbUser) ' +
                'RETURN x,z '
        }
    }

    return fbCmd;
}

/**********  TWITTER QUERIES ***************/

function createTwitterRelationshipNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr)
{
    let twitterCmd = '';

    let usrToDisplay = sna.twUserType;

    if (usrToDisplay==='follower')
    {
        if (keyword !== '' && person !== '')
        {
            twitterCmd =
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f)-[:TAGGED_IN]-(t) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH j=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(:twUser)' +
                'WITH t,f,x,d,z,j ' +
                'RETURN x,z,j '
        }
        else if (keyword !== '' && person ==='')
        {
            twitterCmd =
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f)-[:TAGGED_IN]-(t {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH j=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(:twUser)' +
                'WITH t,f,x,d,z,j ' +
                'RETURN x,z,j '
        }
        else if (keyword === '' && person !== '')
        {
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                '  (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:twUser{graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(b:twUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword === '' && person === '')
        {
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                '  (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:twUser{graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(b:twUser) ' +
                'RETURN x,y,z '
        }
    }
    else if (usrToDisplay==='following')
    {
        if (keyword !== '' && person !== '')
        {
            twitterCmd =
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f)-[:TAGGED_IN]-(t) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH j=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(:twUser)' +
                'WITH t,f,x,d,z,j ' +
                'RETURN x,z,j '
        }
        else if (keyword !== '' && person ==='')
        {
            twitterCmd =
                'MATCH (u:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f)-[:TAGGED_IN]-(t) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH j=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(:twUser)' +
                'WITH t,f,x,d,z,j ' +
                'RETURN x,z,j '
        }
        else if (keyword === '' && person !== '')
        {
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                '  (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:twUser{graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(b:twUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword === '' && person === '')
        {
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOWING]-(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                '  (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:twUser{graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(b:twUser) ' +
                'RETURN x,y,z '
        }
    }
    else
    {
        if (keyword !== '' && person !== '')
        {
            twitterCmd =
                'MATCH (:twUser)-[:TWEETED]->(t)<-[:TAGGED_IN]-(f {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})--(f) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' AND ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH j=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(:twUser)' +
                'WITH t,f,x,d,z,j ' +
                'RETURN x,z,j '
        }
        else if (keyword !== '' && person ==='')
        {
            twitterCmd =
                'MATCH (:twUser)-[:TWEETED]->(t)<-[:TAGGED_IN]-(f {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})--(f) ' +
                'WHERE ' +
                ' t.full_text =~ \'(?ism).*' + keyword + '.*\' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                ' (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH j=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(:twUser)' +
                'WITH t,f,x,d,z,j ' +
                'RETURN x,z,j '
        }
        else if (keyword === '' && person !== '')
        {
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})--(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                '  (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:twUser{graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(b:twUser) ' +
                'RETURN x,y,z '
        }
        else if (keyword === '' && person === '')
        {
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})--(f) ' +
                'WHERE ' +
                ' exists(f.firstInteration) AND ' +
                ' (f.firstInteration>\'' + start_date + '\' AND f.firstInteration<\'' + end_date + '\') AND ' +
                ' f.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH y=(f)-[s:TAGGED_TOGETHER]-(d) ' +
                'WHERE ' +
                ' s.tagged_together>=' + minEdgeValue + ' AND ' +
                '  (d.firstInteration>\'' + start_date + '\' AND d.firstInteration<\'' + end_date + '\') AND ' +
                ' d.nodeDegree>=' + minNodevalue + ' ' +
                'OPTIONAL MATCH z=(a:twUser{graph_information:[\'' + usr +'\', \'twitter\']})-[:FOLLOW]-(b:twUser) ' +
                'RETURN x,y,z '
        }
    }


    return twitterCmd;
}

function createTwitterTrafficNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr)
{
    let twitterCmd = '';

    let nodeToDisplay = sna.tweetType;

    if (nodeToDisplay==='all')
    {
        if (keyword !== '' && person !== '') {
            twitterCmd =
                'MATCH (f)-[:TAGGED_IN]->(t {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?i).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword !== '' && person ===''){
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' t.full_text =~ \'(?i).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword === '' && person !== ''){
            twitterCmd =
                'MATCH (f)-[:TAGGED_IN]->(t {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword === '' && person === ''){
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
    }
    else if (nodeToDisplay==='tweet')
    {
        if (keyword !== '' && person !== '') {
            twitterCmd =
                'MATCH (f)-[:TAGGED_IN]->(t:Tweet {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?i).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword !== '' && person ===''){
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t:Tweet) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' t.full_text =~ \'(?i).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword === '' && person !== ''){
            twitterCmd =
                'MATCH (f)-[:TAGGED_IN]->(t:Tweet {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t:Tweet) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword === '' && person === ''){
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t:Tweet) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
    }
    else if (nodeToDisplay==='retweet')
    {
        if (keyword !== '' && person !== '') {
            twitterCmd =
                'MATCH (f)-[:TAGGED_IN]->(t:Retweet {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t:Retweet) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.full_text =~ \'(?i).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword !== '' && person ===''){
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t:Retweet) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' t.full_text =~ \'(?i).*' + keyword + '.*\' AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword === '' && person !== ''){
            twitterCmd =
                'MATCH (f)-[:TAGGED_IN]->(t:Retweet {graph_information:[\'' + usr +'\', \'twitter\']}) ' +
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t:Retweet) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' (f.name=~ \'(?i).*' + person + '.*\' OR f.screen_name=~ \'(?i).*' + person + '.*\') AND ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
        else if (keyword === '' && person === ''){
            twitterCmd =
                'MATCH x=(:twUser {graph_information:[\'' + usr +'\', \'twitter\']})-[:TWEETED]->(t:Retweet) ' +
                'OPTIONAL MATCH (t)-[:TAGGED_IN]-(f) ' +
                'WITH x,t,f ' +
                'WHERE ' +
                ' t.nodeDegree>= ' + minNodevalue + ' AND ' +
                ' t.created_at>\'' + start_date + '\' AND t.created_at<\'' + end_date + '\' ' +
                'RETURN x'
        }
    }
    return twitterCmd;
}

/**********  MBOX QUERIES ***************/

function createMboxrRelationshipNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr)
{
    let mboxCmd;

    if (keyword !== '' && person !== '')
        mboxCmd =
            'MATCH (m:Mail {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' (m.subject =~\'(?i).*' + keyword + '.*\' OR m.content =~\'(?i).*' + keyword + '.*\') AND ' +
            ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
            'MATCH x=(n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
            ' n.label  =~\'(?i).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'

    else if (keyword !== '' && person ==='')
        mboxCmd =
            'MATCH (m:Mail {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' (m.subject =~\'(?i).*' + keyword + '.*\' OR m.content =~\'(?i).*' + keyword + '.*\') AND ' +
            ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
            'MATCH x=(n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'

    else if (keyword === '' && person !== '')
        mboxCmd =
            'MATCH x=(n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.label  =~\'(?i).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'

    else if (keyword === '' && person === '')
        mboxCmd =
            'MATCH x=(n)-[r:UNDIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'

    return mboxCmd;
}

function createMboxTrafficNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr)
{
    let mboxCmd;

    if (keyword !== '' && person !== '')
        mboxCmd =
            'MATCH (m:Mail {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' (m.subject =~\'(?i).*' + keyword + '.*\' OR m.content =~\'(?i).*' + keyword + '.*\') AND ' +
            ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
            'MATCH x=(n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
            ' n.label  =~\'(?i).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'

    else if (keyword !== '' && person ==='')
        mboxCmd =
            'MATCH (m:Mail {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' (m.subject =~\'(?i).*' + keyword + '.*\' OR m.content =~\'(?i).*' + keyword + '.*\') AND ' +
            ' m.time>=\'' + start_date + '\' AND m.time<=\'' + end_date + '\' ' +
            'MATCH x=(n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' exists((n)--(m)) AND exists((p)--(m)) AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'
    else if (keyword === '' && person !== '')
        mboxCmd =
            'MATCH x=(n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.label  =~\'(?i).*' + person + '.*\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'

    else if (keyword === '' && person === '')
        mboxCmd =
            'MATCH x=(n)-[r:DIRECTED_EDGE]-(p {graph_information:[\'' + usr +'\', \'mbox\']}) ' +
            'WHERE ' +
            ' n.firstInteration>=\'' + start_date + '\' AND n.firstInteration<=\'' + end_date + '\' AND ' +
            ' p.firstInteration>=\'' + start_date + '\' AND p.firstInteration<=\'' + end_date + '\' AND ' +
            ' n.nodeDegree>' + minNodevalue + ' AND p.nodeDegree>' + minNodevalue + ' AND ' +
            ' r.edge_weight>' + minEdgeValue + ' ' +
            'RETURN x'

    return mboxCmd;
}

/* ---- query routing (ported from the bottom of the old static/main.js) ---- */

function chooseArrow(graphType, sn)
{
    if (graphType==='trafficNet' || sn ==='twitter' & graphType==='relNet') return true;
    return false;
}

function createQueryForDrawing(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType)
{
    let direction;
    let cmd;

    direction = chooseArrow(graphType, sn);

    if (sn === 'facebook')
        cmd = createFacebookQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType);
    else if (sn === 'twitter')
        cmd = createTwitterQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType);
    else if (sn === 'mbox')
        cmd = createMboxQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType);

    return {cmd, direction};
}

function createFacebookQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType)
{
    let cmd;

    if (graphType==='relNet')
        cmd = createFacebookRelationshipNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr);
    else if (graphType==='trafficNet')
        cmd = createFacebookTrafficNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr);
    return cmd;
}

function createTwitterQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType)
{
    let cmd;

    if (graphType==='relNet')
        cmd = createTwitterRelationshipNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr);
    else if (graphType==='trafficNet')
        cmd = createTwitterTrafficNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr);
    return cmd;
}

function createMboxQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType)
{
    let cmd = '';

    if (graphType==='relNet')
        cmd = createMboxrRelationshipNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr);
    else if (graphType==='trafficNet')
        cmd = createMboxTrafficNetworkQuery(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr);

    return cmd;
}

export { createQueryForDrawing, chooseArrow }
