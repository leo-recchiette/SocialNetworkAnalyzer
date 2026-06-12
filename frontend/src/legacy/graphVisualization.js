import $ from 'jquery'
import { sna } from './bridge.js'
import { clearDataSpace } from './dom.js'
import { dataVisualization } from './dataVisualization.js'

let viz;

function stabilizeGraph()
{
    if (viz) viz.stabilize(); // to block the graph
}

function getNodeDimension( sn, graphType )
{
    if (sn!=='twitter') return 'nodeDegree';

    else
    {
        if (sn === 'twitter' && graphType==='trafficNet')
            return sna.twNodeType;
        else return 'nodeDegree'
    }
}

function drawGraph(cmd, direction, dimension)
{
    $('.content').html('<div id="viz" style="height: 100%; width: 100%"></div>')

    let config = {
        container_id: "viz",
        // neovis.js runs in the browser and talks to Neo4j directly over bolt.
        // docker-compose maps the neo4j container's 7687 to localhost:7687, so
        // "localhost" is correct from the user's machine. The password must match
        // NEO4J_AUTH in docker-compose.yml (default: snapassword).
        server_url: "bolt://localhost:7687",
        server_user: "neo4j",
        server_password: "snapassword",
        arrows: direction,
        labels: {
            // facebook graph node
            'Friend': {
                'caption': 'name',
                'size': dimension,
            },
            'RemovedFriend': {
                'caption': 'name',
                'size': dimension,
            },
            'Post': {
                'caption': 'timestamp',
                'size': dimension,
            },
            'FriendPost': {
                'caption': 'timestamp',
                'size': dimension
            },
            'Comment': {
                'caption': 'timestamp',
                'size': dimension
            },
            'Direct_Message': {
                'caption': 'timestamp',
                'size': dimension,
            },
            'fbUser': {
                'caption': 'name',
            },
            // twitter graph node
            'twUser': {
                'caption': 'username'
            },
            'Liked_Tweet': {
                'caption': 'tweet'
            },
            'Tweet': {
                'caption': 'created_at',
                'size' : dimension
            },
            'Retweet': {
                'caption': 'created_at',
                'size' : dimension
            },
            'BothFollowType': {
                'caption': 'screen_name',
                'size': dimension
            },
            'Follower': {
                'caption': 'screen_name',
                'size': dimension
            },
            'Following': {
                'caption': 'screen_name',
                'size': dimension
            },
            // mbox graph node
            "Undirected_Node": {
                "size": dimension,
                "caption": "label"
            },
            "Directed_Node": {
                "size": dimension,
                "caption": "label"
            }
        },
        relationships: {
            // facebook graph relationships
            "PUBLISHED": {
                "thickness": "count",
                "caption": false // to show the label
            },
            "TAGGED_IN": {
                "thickness": "count",
                "caption": false
            },
            "FRIEND": {
                "thickness": "count",
                "caption": false
            },
            "TAG": {
                "thickness": "tagged_together",
                "caption": false
            },
            "TAGGED_TOGETHER": {
                "thickness": "tagged_together",
                "caption": false
            },
            "FBUSERFRIEND": {
                "thickness": "tagged_together",
                "caption": false
            },
            // twitter graph relationships
            "LIKED_TWEET": {
                "thickness": "count",
                "caption": false
            },
            "TWEETED": {
                "thickness": "count",
                "caption": false
            },
            "QUOTED": {
                "thickness": "count",
                "caption": false
            },
            "FOLLOW_FOR_ALL_USERS": {
                "thickness": "count",
                "caption": false
            },
            "FOLLOW": {
                "thickness": "count",
                "caption": false
            },
            "FOLLOWING": {
                "thickness": "count",
                "caption": false
            },
            "SAME_ACCOUNT": {
                "thickness": "count",
                "caption": false
            },
            // mbox graph relationships
            "UNDIRECTED_EDGE": {
                "thickness": "edge_weight",
                "caption": false
            },
            "DIRECTED_EDGE": {
                "thickness": "edge_weight",
                "caption": false
            }

        },
        initial_cypher: cmd,
    };

    viz = new window.NeoVis.default(config);
    viz.render();

    viz.registerOnEvent("completed", (e)=>{
        viz["_network"].on("click", (event)=>{
            let id;
            let dts;

            sna.setDataViz1('selected');

            if (event.nodes.length>0)
            {
                id = event.nodes[0];
                sna.setDataViz2('contacts');

                dts = JSON.parse(sna.dataToSearch);
                dts['dataViz2'] = 'contacts';
            }
            else
            {
                id = event.edges[0];
                sna.setDataViz2('links');

                dts = JSON.parse(sna.dataToSearch);
                dts['dataViz2'] = 'links';
            }

            dts['dataViz1'] = 'selected';

            sna.dataToSearch = JSON.stringify(dts);

            clearDataSpace();

            $.ajax({
                url: 'server.php',
                dataType: 'json',
                data: {dataToSearch: sna.dataToSearch, id},
                type: 'post',
                success: function (data) {
                    dataVisualization (data);
                },
                error: function () {
                    let selected = sna.dataViz2;

                    if (selected === 'contacts')
                        $('.data').append(
                            '<div class="data-item">' +
                                '<span> Try to select a node </span>' +
                            '</div>'
                        );
                    else
                        $('.data').append(
                            '<div class="data-item">' +
                            '<span> Try to select a link </span>' +
                            '</div>'
                        );

                },
            })
        });
    });

}

export { drawGraph, getNodeDimension, stabilizeGraph }