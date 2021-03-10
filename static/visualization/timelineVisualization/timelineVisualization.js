function getTimelineObject(year, month, tfidfWord , percentage, index)
{
    let obj = new Object();
    obj.custom_index = index,
    obj.id = year + '-' + month;
    obj.start = year + '-' + month+ '-02';
    obj.end = year + '-' + month + '-' + (new Date(year, month, 0).getDate()-2);
    obj.name = tfidfWord;
    obj.progress = percentage;

    return obj
}

function getWords(dataToSearch)
{
    let action = 'getTimelineObject';

    $.ajax({
        url: 'server.php',
        dataType: 'JSON',
        data: {dataToSearch, action},
        type: 'post',
        beforeSend: function () {
            $('.data').html(
                '<div class="row">' +
                '<div class="col-4"></div>' +
                '<div class="col-4">' +
                '<div class="spinner-border text-dark" role="status" style="margin-top:5px; margin-left: 42%">' +
                '<span class="sr-only"></span> ' +
                '</div>' +
                '</div>' +
                '<div class="col-4"></div>' +
                '</div>')
        },
        success:function (data){
            if (data.length>0)
               $('.data').html(
                        '<div class="data-item">' +
                        '<span> Try to select a word </span>' +
                        '</div>'
                    );
            else
                noDataFoundVisualization();

            $('#content').html('<svg id="gantt"></svg>');

            var tasks = [];

            let timelineIndex = 0 ;
            let actualColumn = 0 ;
            for (let index=0 ; index < data.length; index++)
                if (data[index]['Word'] != '' )
                {
                    let year = data[index]['timestamp'].split('/')[0];
                    let month = parseInt(data[index]['timestamp'].split('/')[1]);

                    if (actualColumn == month)
                        timelineIndex ++ ;
                    else
                    {
                        actualColumn = month;
                        timelineIndex = 0 ;
                    }


                    let timelineObj = getTimelineObject(year, month, data[index]['word'], data[index]['value'], timelineIndex);
                    tasks.push(timelineObj);
                }


            var gantt = new Gantt("#gantt", tasks, {
                padding: 12,
                bar_corner_radius: 0,
                on_click: function (task) {
                    showSingleTask(task, dataToSearch);
                },
                custom_popup_html: function(task) {
                    return ''
                }
            }).change_view_mode('Month');

        },
        error: function(){
            console.log('No word');
        }
    })
}

function showSingleTask (task, dataToSearch)
{
    $('.dataViz1').removeClass('dataViz1_selected');
    $('.selected').addClass('dataViz1_selected');

    $('.data').html(
        '<div class="data-item ">' +
        '<p class=\'dataHeader\'>You have selected </p>' +
        '<span class=\'dataKey\'>Word: </span>' +
        '<span class=\'dataValue\'>' + task.name + '</span>' +
        '<br>' +
        '<span class=\'dataKey\'>Percentage: </span>' +
        '<span class=\'dataValue\'>' + task.progress + '%</span>' +
        '<br>' +
        '</div>' +
        '<hr>'
    );

    let action = 'getSingleWordsFrequencyContent';

     let dts = JSON.parse(dataToSearch);

     let sn = dts['sn'];

      dataToSearch = JSON.stringify(dts);

    let word = task.name;
    $.ajax({
        url: 'server.php',
        dataType: 'JSON',
        data: {action, word, dataToSearch},
        type: 'post',
        success:function (data){
            visualizeSingleWord(data, sn, word)
        }
    });


}
