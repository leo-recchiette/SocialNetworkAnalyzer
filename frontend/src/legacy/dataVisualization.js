import $ from 'jquery'
import { sna } from './bridge.js'
import { clearDataSpace, noDataFoundVisualization } from './dom.js'


function dataVisualization (data)
{
    let dts =  JSON.parse(sna.dataToSearch);

    if (data.length>0)
    {
        clearDataSpace();

        if ('Counter' in data[0])
            if (data[0]['Counter']==0)
                noDataFoundVisualization();
            else
            {
                if (sna.dataViz2 === 'contacts')
                    $('.data').html(
                        '<div class="data-item">' +
                        '<span> Try to select a node </span>' +
                        '</div>'
                    );
                else if (sna.dataViz2 === 'links')
                    $('.data').html(
                        '<div class="data-item">' +
                        '<span> Try to select a link </span>' +
                        '</div>'
                    );
            }
        else
        {
            if (dts['sn'] === 'facebook')
                if ( dts['dataViz2'] === 'contacts' )
                    getFacebookContacts(data, dts['graphType']);
                else
                    getFacebookLinks(data, dts['graphType']);
            else if (dts['sn'] === 'twitter')
                if ( dts['dataViz2'] === 'contacts' )
                    getTwitterContacts(data, dts['graphType']);
                else
                    getTwitterLinks(data, dts['graphType']);
            else if (dts['sn'] === 'mbox')
                if ( dts['dataViz2'] === 'contacts' )
                    getMboxContacts(data, dts['graphType']);
                else
                    getMboxLinks(data, dts['graphType']);
        }
    }
    else
    {
        noDataFoundVisualization();
    }

}

/**********************  FACEBOOK **********************/

function getFacebookContacts(data, graphType)
{
    if (graphType == 'relNet')
        getFacebookContactsForRelationshipNetwork(data);
    else if (graphType == 'trafficNet')
        getFacebookContactsForTrafficNetwork(data);
    else if (graphType == 'map')
        getFacebookContactsForMap(data);
    else
        visualizeWords(data);
}

function getFacebookContactsForRelationshipNetwork(data)
{
    for (let i = 0 ;i<data.length; i++)
    {
        $('.data').append(
            '<div class="data-item data-item-'+ i +'">' +
            '<span class=\'dataKey\'>Name: </span>' +
            '<span class=\'dataValue\'>' + data[i]['node']['name'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Node degree: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['node']['nodeDegree'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Tagged together count: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['taggedTogetherValue'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Dump profile: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['propertyDump'] + '</span>' +
            '<br>' +
            '</div>'
        );

        if ('removed_timestamp' in data[i]['node'])
            $('.data-item-'+i).append(
                '<span class=\'dataKey\'>Removed timestamp: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[i]['node']['removed_timestamp'] + '</span>' +
                '<br>'
            )
        else
            $('.data-item-'+i).append(
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[i]['node']['timestamp'] + '</span>' +
                '<br>'
            )

        if ('phoneContacts' in data[i]['node'])
        {
            $('.data-item-'+i).append(
                '<span class=\'dataKey\'>Contacts: </span>' +
                '<span class="dataValue phoneNumber-'+i+'"> </span>'
            )

            for (let index = 0 ; index< data[i]['node']['phoneContacts'].length; index++)
                $('.phoneNumber-'+i).append(
                    data[i]['node']['phoneContacts'][index] + '<br> ');
        }

        if ('taggedWith' in data[0])
            if (data[0]['taggedWith'].length > 0)
            {
                $('.data-item').append(
                    '<div class="spoiler-btn">click to show/hide people tagged in this content </div>' +
                    '<div class="spoiler-body"></div>' +
                    '</div>'
                )

                for (let i = 0; i < data[0]['taggedWith'].length; i++) {
                    $('.spoiler-body').append(
                        '<div class="istaggedWith">' + data[0]['taggedWith'][i] + '</div>'
                    )
                }
            }

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getFacebookContactsForTrafficNetwork(data)
{
    let dv = sna.dataViz1;

    if (dv ==='selected')
    {
        if ('node' in data[0])
        {
            $('.data').html(
                '<div class="data-item">' +
                '<span class=\'dataKey\'>Content: </span>' +
                '<span class=\'dataValue\'>' + data[0]['node']['content'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Node degree: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[0]['nodeDegree'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue\'>' + data[0]['node']['timestamp'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[0]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            );

            if (data[0]['taggedWith'].length > 0 )
            {
                $('.data-item').append(
                    '<div class="spoiler-btn">click to show/hide people tagged in this content </div>' +
                    '<div class="spoiler-body"></div>' +
                    '</div>'
                )

                for (let i = 0; i < data[0]['taggedWith'].length; i++) {
                    $('.spoiler-body').append(
                        '<div class="istaggedWith">' + data[0]['taggedWith'][i] + '</div>'
                    )
                }
            }
        }
        else if ('StartOfConversation' in data[0])
        {
            $('.data').html(
                '<div class="data-item">' +
                '<span class=\'dataKey\'>Participants: </span>' +
                '<span class=\'dataValue participants\'></span>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[0]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            )

            for (let i = 0 ; i< data[0]['StartOfConversation']['participants'].length; i++)
                $('.participants').append(
                    data[0]['StartOfConversation']['participants'][i] + '<br> ');

            $('.data-item').append(
                '<span class=\'dataKey\'>Node degree: </span>' +
                '<span class=\'dataValue\'>' + data[0]['StartOfConversation']['nodeDegree'] + '</span>' +
                '<br>'
            )

            $('.data').append('<hr>');


            for (let i=0 ; i<data.length ; i++)
            {
                if ( i == 0 )
                {
                    $('.data').append(
                        '<div class="data-item">' +
                        '<span class=\'dataKey\'>Sender: </span>' +
                        '<span class=\'dataValue\'>' + data[0]['StartOfConversation']['sender'] + '</span>' +
                        '<br>' +
                        '<span class=\'dataKey\'>Timestamp: </span>' +
                        '<span class=\'dataValue\'>' + data[0]['StartOfConversation']['timestamp'] + '</span>' +
                        '<br>' +
                        '<span class=\'dataKey\'>Content: </span>' +
                        '<span class=\'dataValue\'>' + data[0]['StartOfConversation']['content'] + '</span>' +
                        '<br>' +
                        '</div>'
                    )
                }
                else
                {
                    $('.data').append(
                        '<hr>' +
                        '<div class="data-item">' +
                        '<span class=\'dataKey\'>Sender: </span>' +
                        '<span class=\'dataValue\'>' + data[i]['Replay']['sender'] + '</span>' +
                        '<br>' +
                        '<span class=\'dataKey\'>Timestamp: </span>' +
                        '<span class=\'dataValue\'>' + data[i]['Replay']['timestamp'] + '</span>' +
                        '<br>' +
                        '<span class=\'dataKey\'>Content: </span>' +
                        '<span class=\'dataValue\'>' + data[i]['Replay']['content'] + '</span>' +
                        '<br>' +
                        '</div>'
                    )
                }
            }
        }
    }
    else
    {
        for (let i = 0 ; i < data.length ; i++)
        {
            $('.data').append(
                '<div class="data-item-'+ i +'">' +
                '<span class=\'dataKey\'>Content: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['content'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Node degree: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[i]['node']['nodeDegree'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['timestamp'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[i]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            );

            if ('participants' in data[i]['node'])
            {
                $('.data-item-'+i).append(
                    '<div class="data-item-'+ i +'">' +
                    '<span class=\'dataKey\'>Participants: </span>' +
                    '<span class="dataValue participants-'+i+'"></span>' +

                    '</div>'
                )

                for (let j = 0 ; j< data[i]['node']['participants'].length; j++)
                    $('.participants-'+i).append(
                        data[i]['node']['participants'][j] + '<br> ');
            }
            if (data[i]['taggedWith'].length > 0 )
            {
                $('.data-item-'+i).append(
                    '<div class="spoiler-btn">click to show/hide people tagged in this content </div>' +
                    '<div class="spoiler-body spoiler-body-'+i+'"></div>' +
                    '</div>'
                )

                for (let j = 0; j < data[i]['taggedWith'].length; j++) {
                    $('.spoiler-body-'+i).append(
                        '<div class="istaggedWith">' + data[i]['taggedWith'][j] + '</div>'
                    )
                }
            }

            if (i< data.length - 1 )
                $('.data').append('<hr>');
        }
    }

}

function getFacebookContactsForMap(data) {
    for (let i = 0 ; i< data.length ; i++ )
    {
        if ( 'content' in data[i]['place'] )
        {
            $('.data').append(
                '<div class="data-item">' +
                '<span class=\'dataKey\'>Content: </span>' +
                '<span class=\'dataValue\'>' + data[i]['place']['content'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Node degree: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[i]['place']['nodeDegree'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue\'>' + data[i]['place']['timestamp'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Place name: </span>' +
                '<span class=\'dataValue\'>' + data[i]['place']['place_name'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[0]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            );
        }
        else
        {
            $('.data').append(
                '<div class="data-item data-item-'+ i +'">' +
                '<span class=\'dataKey\'>Name: </span>' +
                '<span class=\'dataValue\'>' + data[i]['place']['name'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Latitude: </span>' +
                '<span class=\'dataValue\'>' + data[i]['place']['place_latitude'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Longitude: </span>' +
                '<span class=\'dataValue\'>' + data[i]['place']['place_longitude'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[i]['place']['timestamp'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' +  data[0]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            );
        }

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getFacebookLinks(data, graphType)
{
    if (graphType == 'relNet')
        getFacebookLinksForRelationshipNetwork(data);
    else if (graphType == 'trafficNet')
        getFacebookLinksForTrafficNetwork(data);
    else if (graphType == 'map')
        getFacebookLinksForMap(data);
    else
    {}
}

function getFacebookLinksForRelationshipNetwork(data)
{
    $('.data').html(
        '<div class="row">' +
        '<div class="col-4"></div>' +
        '<div class="col-4"></div>' +
        '<div class="col-4" ><b>Tagged together</b></div>' +
        '</div>'

    )

    for (let i=0 ; i < data.length; i++)
    {
        $('.data').append(
            '<div class="row data-item data-item'+ i +'">' +

            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_1']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_2']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;"><b>'+data[i]['link']+'</b></div>' +
            '</div>'
        );

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getFacebookLinksForMap(data)
{

    console.log(data);
    $('.data').html(
        '<div class="data-item">' + data[0]['place'] + '</div>'
    );
}

/**********************  TWITTER  **********************/

function getTwitterContacts(data, graphType)
{
    if (graphType == 'relNet')
        getTwitterContactsForRelationshipNetwork(data);
    else if (graphType == 'trafficNet')
        getTwitterContactsForTrafficNetwork(data);
    else if (graphType == 'map')
        getTwitterContactsForMap(data)
    else
        visualizeWords(data);
}

function getTwitterContactsForRelationshipNetwork(data)
{
    for (let i = 0 ; i< data.length ;i ++)
    {
        $('.data').append(
            '<div class="data-item data-item-'+ i +'">' +
            '<span class=\'dataKey\'>Name: </span>' +
            '<span class=\'dataValue\'>' + data[i]['node']['name'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Account name: </span>' +
            '<span class=\'dataValue\'>' + data[i]['node']['screen_name'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Twitter profile: </span>' +
            '<a class=\'dataValue\'><a href="'+data[i]['node']['user_link']+'" target="_blank">link</a></span>' +
            '<br>' +
            '<span class=\'dataKey\'>Node degree: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['node']['nodeDegree'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Tagged together count: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['taggedTogetherValue'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Dump profile: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['propertyDump'] + '</span>' +
            '<br>' +
            '</div>'
        );

        if ('taggedWith' in data[0] )
            if (data[0]['taggedWith'].length > 0 )
            {
                $('.data-item').append(
                    '<div class="spoiler-btn">click to show/hide people tagged in this tweet </div>' +
                    '<div class="spoiler-body"></div>' +
                    '</div>'
                )

                for (let i = 0; i < data[0]['taggedWith'].length; i++) {
                    $('.spoiler-body').append(
                        '<div class="istaggedWith">' + data[0]['taggedWith'][i] + '</div>'
                    )
                }
            }

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getTwitterContactsForTrafficNetwork(data)
{
    for (let i = 0 ;i < data.length; i++) {
        $('.data').append(
            '<div class="data-item-'+i+'">' +
            '<span class=\'dataKey\'>Content: </span>' +
            '<span class=\'dataValue\'>' + data[i]['node']['full_text'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Timestamp: </span>' +
            '<span class=\'dataValue\'>' + data[i]['node']['created_at'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Node degree: </span>' +
            '<span class=\'dataValue nodeDegree\'>' + data[i]['nodeDegree'] + '</a></span>' +
            '<br>' +
            '<span class=\'dataKey\'>Dump profile: </span>' +
            '<span class=\'dataValue nodeDegree\'>' + data[i]['propertyDump'] + '</span>' +
            '<br>' +
            '</div>'
        );

        if (data[i]['node']['hashtags_text'] !== '')
            $('.data-item-'+i).append(
                '<span class=\'dataKey\'>Hashtags text: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['node']['hashtags_text'] + '</span>' +
                '<br>'
            )

        if (data[i]['taggedWith'].length > 0) {
            $('.data-item-'+i).append(
                '<div class="spoiler-btn">click to show/hide people tagged in this tweet </div>' +
                '<div class="spoiler-body spoiler-body-'+i+'"></div>' +
                '</div>'
            )

            for (let j = 0; j < data[i]['taggedWith'].length; j++) {
                $('.spoiler-body-'+i).append(
                    '<div class="istaggedWith">' + data[i]['taggedWith'][j] + '</div>'
                )
            }
        }

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getTwitterContactsForMap(data)
{
    for (let i = 0 ; i < data.length; i++)
    {
        $('.data').append(
            '<div class="data-item-'+i+'">' +
            '<span class=\'dataKey\'>Content: </span>' +
            '<span class=\'dataValue\'>' + data[i]['place']['full_text'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Timestamp: </span>' +
            '<span class=\'dataValue\'>' + data[i]['place']['created_at'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Latitude: </span>' +
            '<span class=\'dataValue\'>' + data[i]['place']['latitude'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Longitude: </span>' +
            '<span class=\'dataValue\'>' + data[i]['place']['longitude'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Retweet count: </span>' +
            '<span class=\'dataValue\'>' + data[i]['place']['retweet_count'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Node degree: </span>' +
            '<span class=\'dataValue\'>' + data[i]['place']['nodeDegree'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Dump profile: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['propertyDump'] + '</span>' +
            '<br>' +
            '</div>'
        );

        if ('url' in data[i]['place'])
            $('.data-item-'+i).append(
                '<span class=\'dataKey\'>External content: </span>' +
                '<span class=\'dataValue\'><a href=\'' + data[i]['place']['url'] + '\' target="_blank">link</a></span>' +
                '<br>'
            );

        if ('hashtags_text' in data[i]['place'] && data[i]['place']['hashtags_text'] !=='#')
            $('.data-item-'+i).append(
                '<span class=\'dataKey\'>Hashtags: </span>' +
                '<span class=\'dataValue\'>' + data[i]['place']['hashtags_text'] + '</span>' +
                '<br>'
            )



        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }

}

function getTwitterLinks(data, graphType)
{
    if (graphType == 'relNet')
        getTwitterLinksForRelationshipNetwork(data);
    else if (graphType == 'trafficNet')
        getTwitterLinksForTrafficNetwork(data);
    else if (graphType == 'map')
        getTwitterkLinksForMap(data);
    else
    {}
}

function getTwitterLinksForRelationshipNetwork(data)
{
    $('.data').html(
        '<div class="row">' +
        '<div class="col-4"></div>' +
        '<div class="col-4"></div>' +
        '<div class="col-4" ><b>Tagged together</b></div>' +
        '</div>'

    )

    for (let i=0 ; i < data.length; i++)
    {
        $('.data').append(
            '<div class="row data-item data-item'+ i +'">' +

            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_1']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_2']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;"><b>'+data[i]['link']+'</b></div>' +
            '</div>'
        );

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}


/**********************  MBOX  **********************/

function getMboxContacts(data, graphType)
{
    if (graphType == 'relNet')
        getMboxContactsForRelationshipNetwork(data);
    else if (graphType == 'trafficNet')
        getMboxContactsForTrafficNetwork(data);
    else if (graphType == 'map')
        getMboxContactsForMap(data)
    else
        visualizeWords(data);
}

function getMboxContactsForRelationshipNetwork(data)
{
    for (let i = 0 ; i< data.length ;i ++)
    {
        $('.data').append(
            '<div class="data-item data-item-'+ i +'">' +
            '<span class=\'dataKey\'>Name: </span>' +
            '<span class=\'dataValue\'>' + data[i]['node']['label'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Node degree: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['node']['nodeDegree'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Tagged together count: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['taggedTogetherValue'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Dump profile: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[0]['node']['userProfileProperty'] + '</span>' +
            '<br>' +
            '</div>'
        );

        if ('taggedWith' in data[0] )
            if (data[0]['taggedWith'].length > 0 )
            {
                $('.data-item').append(
                    '<div class="spoiler-btn">click to show/hide people tagged whit this person </div>' +
                    '<div class="spoiler-body"></div>' +
                    '</div>'
                )

                for (let i = 0; i < data[0]['taggedWith'].length; i++) {
                    $('.spoiler-body').append(
                        '<div class="istaggedWith">' + data[0]['taggedWith'][i] + '</div>'
                    )
                }
            }

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getMboxContactsForTrafficNetwork(data)
{
    for (let i = 0 ; i< data.length ;i ++)
    {
        $('.data').append(
            '<div class="data-item data-item-'+ i +'">' +
            '<span class=\'dataKey\'>Name: </span>' +
            '<span class=\'dataValue\'>' + data[i]['node']['label'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Node degree: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['node']['nodeDegree'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Tagged together count: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['taggedTogetherValue'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Dump profile: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[0]['node']['userProfileProperty'] + '</span>' +
            '<br>' +
            '</div>'
        );

        if ('taggedWith' in data[0] )
            if (data[0]['taggedWith'].length > 0 )
            {
                $('.data-item').append(
                    '<div class="spoiler-btn">click to show/hide people tagged whit this person </div>' +
                    '<div class="spoiler-body"></div>' +
                    '</div>'
                )

                for (let i = 0; i < data[0]['taggedWith'].length; i++) {
                    $('.spoiler-body').append(
                        '<div class="istaggedWith">' + data[0]['taggedWith'][i] + '</div>'
                    )
                }
            }

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getMboxLinks(data, graphType)
{
    if (graphType == 'relNet')
        getMboxLinksForRelationshipNetwork(data);
    else if (graphType == 'trafficNet')
        getMboxLinksForTrafficNetwork(data);
    else if (graphType == 'map')
        getMboxLinksForMap(data)
    else
    {}
}

function getMboxLinksForRelationshipNetwork(data)
{
    $('.data').html(
        '<div class="row">' +
        '<div class="col-4"></div>' +
        '<div class="col-4"></div>' +
        '<div class="col-4" ><b>Tagged together</b></div>' +
        '</div>'

    )

    for (let i=0 ; i < data.length; i++)
    {
        $('.data').append(
            '<div class="row data-item data-item'+ i +'">' +

            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_1']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_2']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;"><b>'+data[i]['link']+'</b></div>' +
            '</div>'
        );

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

function getMboxLinksForTrafficNetwork(data)
{
    $('.data').html(
        '<div class="row">' +
        '<div class="col-4"></div>' +
        '<div class="col-4"></div>' +
        '<div class="col-4" ><b>Tagged together</b></div>' +
        '</div>'

    )

    for (let i=0 ; i < data.length; i++)
    {
        $('.data').append(
            '<div class="row data-item data-item'+ i +'">' +

            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_1']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;">'+data[i]['name_2']+'</div>' +
            '<div class="col-4" style="word-wrap: break-word;"><b>'+data[i]['link']+'</b></div>' +
            '</div>'
        );

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}

/**********************  ALL  **********************/

function visualizeSingleWord(data, sn, word)
{
    $('.data').append('<p>The word <b>\"'+word+'\"</b> is present in this content in the selected range of time:</p>');

    if (sn === 'facebook')
        for (let i=0 ; i<data.length ; i++) {
            $('.data').append(
                '<div class="data-item-'+ i +'">' +
                '<span class=\'dataKey\'>Content: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['content'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Node degree: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['node']['nodeDegree'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['timestamp'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            );

            if (i< data.length - 1 )
                $('.data').append('<hr>');
        }
    else if (sn === 'twitter')
        for  (let i=0 ; i<data.length ; i++)
        {
            $('.data').append(
                '<div class="data-item-'+ i +'">' +
                '<span class=\'dataKey\'>Content: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['full_text'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Node degree: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['node']['nodeDegree'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['created_at'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            );

            if (i< data.length - 1 )
                $('.data').append('<hr>');
        }
    else
        for  (let i=0 ; i<data.length ; i++)
        {
            $('.data').append(
                '<div class="data-item-'+ i +'">' +
                '<span class=\'dataKey\'>Sender: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['sender'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>To: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['node']['to'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Timestamp: </span>' +
                '<span class=\'dataValue\'>' + data[i]['node']['time'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Subject: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['node']['subject'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Content: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['node']['content'] + '</span>' +
                '<br>' +
                '<span class=\'dataKey\'>Dump profile: </span>' +
                '<span class=\'dataValue nodeDegree\'>' + data[i]['propertyDump'] + '</span>' +
                '<br>' +
                '</div>'
            );

            if (i< data.length - 1 )
                $('.data').append('<hr>');
        }
}

function visualizeWords(data)
{
    clearDataSpace();

    let dts = JSON.parse(sna.dataToSearch);

    let dv = dts['dataViz1'];

    sna.dataToSearch = JSON.stringify(dts);

    if (dv === 'filtered')
        $('.data').append(
            '<div class="data-item"><b> Relevant words in the selected range of time</b></div><br>'
        )
    else if (dv === 'all')
        $('.data').append(
            '<div class="data-item"><b> All time Relevant words</b></div><br>'
        )

    for (let i = 0 ; i< data.length ;i ++)
    {
        $('.data').append(
            '<div class="data-item data-item-'+ i +'">' +
            '<span class=\'dataKey\'>Word: </span>' +
            '<span class=\'dataValue\'>' + data[i]['word'] + '</span>' +
            '<br>' +
            '<span class=\'dataKey\'>Value: </span>' +
            '<span class=\'dataValue nodeDegree\'>' +  data[i]['value'] + '%</span>' +
            '<br>' +
            '</div>'
        );

        if (i< data.length - 1 )
            $('.data').append('<hr>');
    }
}
export { dataVisualization, visualizeSingleWord }
