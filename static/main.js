let dataToSearch ;

$(function($scope)
{
    let usr = '';

    $('#exampleModal').modal('show');

    $( ".slider" ).slider({
        range: "max",
        min: 0,
        max: 50,
        value: 1
    });

    $('[data-toggle="tooltip"]').tooltip();

    $(function() {
        $( "#slider-range" ).slider({
            range: true,
            min: new Date('2000.01.01').getTime() / 1000,
            max: new Date(getTodayDate()).getTime() / 1000,
            step: 86400,
            values: [ new Date('2020.01.01').getTime() / 1000, new Date('2020.12.13').getTime() / 1000 ]
        });
    });

    $('.graphType').on('click',function()
    {
        $('.graphType').removeClass('graphType_selected');
        $(this).addClass('graphType_selected');
        enableDisableButtons();
        setEnvironment(usr);
    });

    $('.dataViz1').on('click',function()
    {

        $('.dataViz1').removeClass('dataViz1_selected');
        $(this).addClass('dataViz1_selected');

        clearDataSpace();

        let dts = JSON.parse(dataToSearch);

        dts['dataViz1'] = $('.dataViz1_selected').data('value');

        let ntd = getNodeToDisplay( dts['graphType'],  dts['sn']);

        dataToSearch = JSON.stringify(dts);

        let action = 'getData';

        $.ajax({
            url: 'server.php',
            dataType: 'json',
            data: {dataToSearch, action, ntd},
            type: 'post',
            beforeSend:function (){

                if ($('.dataViz1_selected').data('value') === 'selected')
                {
                    if ($('.dataViz2_selected').data('value') === 'contacts')
                        $('.data').append(
                            '<div class="data-item">' +
                            '<span> Try to select a node </span>' +
                            '</div>'
                        );
                    else if ($('.dataViz2_selected').data('value') === 'links')
                        $('.data').append(
                            '<div class="data-item">' +
                            '<span> Try to select a link </span>' +
                            '</div>'
                        );
                }
                else
                {
                    $('.data').html(
                        '<div class="row">' +
                        '<div class="col-4"></div>' +
                        '<div class="col-4">' +
                        '<div class="spinner-border text-dark" role="status" style="margin-top:5px; margin-left: 42%">' +
                        '<span class="sr-only"></span> '+
                        '</div>' +
                        '</div>' +
                        '<div class="col-4"></div>' +
                        '</div>')
                }


            },
            success: function (data) {
                dataVisualization (data);
            },
            error: function (){
                console.log('errore');
            },
        });

    });

    $('.dataViz2').on('click',function()
    {
        $('.dataViz2').removeClass('dataViz2_selected');
        $(this).addClass('dataViz2_selected');

        if ($('.dataViz2_selected').data('value')==='links')
        {
            $('.ordering-item option[value="timedesc"]').removeAttr('selected');
            $('.ordering-item option[value="tagcount"]').attr('selected', 'selected');

            $('.ordering-item option[value="timedesc"]').attr('disabled', 'disabled');
            $('.ordering-item option[value="timeasc"]').attr('disabled', 'disabled');
            $('.ordering-item option[value="name"]').attr('disabled', 'disabled');
            $('.ordering-item option[value="degree"]').attr('disabled', 'disabled');
        }
        else
        {
            $('.ordering-item option[value="tagcount"]').removeAttr('selected');
            $('.ordering-item option[value="timedesc"]').attr('selected', 'selected');

            $('.ordering-item option[value="timedesc"]').removeAttr('disabled');
            $('.ordering-item option[value="timeasc"]').removeAttr('disabled');
            $('.ordering-item option[value="name"]').removeAttr('disabled');
            $('.ordering-item option[value="degree"]').removeAttr('disabled');
        }

        clearDataSpace();

        let dts = JSON.parse(dataToSearch);

        dts['dataViz2'] = $('.dataViz2_selected').data('value');

        let ntd = getNodeToDisplay( dts['graphType'],  dts['sn']);

        dataToSearch = JSON.stringify(dts);

        let action = 'getData';

        $.ajax({
            url: 'server.php',
            dataType: 'json',
            data: {dataToSearch, action, ntd},
            type: 'post',
            beforeSend:function (){

                if ($('.dataViz1_selected').data('value') === 'selected')
                {
                    if ($('.dataViz2_selected').data('value') === 'contacts')
                        $('.data').append(
                            '<div class="data-item">' +
                            '<span> Try to select a node </span>' +
                            '</div>'
                        );
                    else if ($('.dataViz2_selected').data('value') === 'links')
                        $('.data').append(
                            '<div class="data-item">' +
                            '<span> Try to select a link </span>' +
                            '</div>'
                        );
                }
                else
                {
                    $('.data').html(
                        '<div class="row">' +
                        '<div class="col-4"></div>' +
                        '<div class="col-4">' +
                        '<div class="spinner-border text-dark" role="status" style="margin-top:5px; margin-left: 42%">' +
                        '<span class="sr-only"></span> '+
                        '</div>' +
                        '</div>' +
                        '<div class="col-4"></div>' +
                        '</div>')
                }
            },
            success: function (data) {
                dataVisualization (data);
            },
            error: function (){
                console.log('errore2');
            },
        });
    });

    $('#file-upload').on('change', function()
    {
        let i = $(this).prev('label').clone();
        let file = $('#file-upload')[0].files[0].name;
        $(this).prev('label').text(file);
    });

    $('.log').on('click', function ()
    {
        let user = $('.userMail').val();
        let pass = $('.userPassword').val();
        let action = 'login';

        $.ajax({
            url: 'server.php',
            dataType: 'json',
            cache: false,
            data: {user, pass, action},
            type: 'post',
            success: function(data){
                if (data['value']===1) {
                    usr = data['user_mail'];
                    console.log('Hi, ' + usr);

                    setSliders(usr);

                    $('#drawer-demo .login-item').hide();
                    $('.username').html(usr);
                    $('.drawer-item').show();
                    $('.logout').show();

                }
                else if (data['value']===-1) {
                    $('.userPassword')
                        .addClass('alert')
                        .removeClass('information')
                        .val('')
                        .attr("placeholder", 'Wrong password');

                    setTimeout(function () {
                        $('.userPassword')
                            .removeClass('alert')
                            .addClass('information')
                            .attr("placeholder",' Insert your password');
                    }, 3000);

                    console.log(data['user_mail'] + ' retype your password');
                }
                else if (data['value']===0){
                    $('.userMail')
                        .addClass('alert')
                        .removeClass('information')
                        .val('')
                        .attr("placeholder", data['user_mail']);

                    setTimeout(function () {
                        $('.userMail')
                            .removeClass('alert')
                            .addClass('information')
                            .attr("placeholder",' Insert your email');
                    }, 3000);
                }

            },
            error: function(){
                console.log('that\'s something wrong.Please try again');
            }
        })
    });

    $('.register').on('click', function ()
    {
        let user = $('.userMail').val();
        let pass = $('.userPassword').val();
        let action = 'register';


        let checkMail = validateEmail(user);

        if (checkMail)
        {
            if (pass === '')
            {
                $('.register')
                    .removeClass('btn-outline-light')
                    .addClass('btn-outline-danger');


                $('.register')
                    .html('Insert a valid password')
                    .css('font-size','small')
                    .css('height','48px');

                setTimeout(function () {
                    $('.register')
                        .addClass('btn-outline-light')
                        .removeClass('btn-outline-danger');

                    $('.register').html('Register').css('font-size','large');
                }, 3000);
            }
            else
                $.ajax({
                    url: 'server.php',
                    dataType: 'json',
                    cache: false,
                    data: {user, pass, action},
                    type: 'post',
                    success: function(data){
                        if (data['value']===1)
                        {
                            $('.register')
                                .removeClass('btn-outline-light')
                                .addClass('btn-outline-warning');


                            $('.register')
                                .html(data['user_mail'])
                                .css('font-size','small')
                                .css('height','48px');

                            setTimeout(function () {
                                $('.register')
                                    .addClass('btn-outline-light')
                                    .removeClass('btn-outline-warning');

                                $('.register').html('Register').css('font-size','large');
                            }, 3000);
                        }
                        else if (data['value']===0)
                        {
                            $('.register')
                                .removeClass('btn-outline-light')
                                .addClass('btn-outline-success');


                            $('.register')
                                .html(data['user_mail'])
                                .css('font-size','small')
                                .css('height','48px');

                            setTimeout(function () {
                                $('.register')
                                    .addClass('btn-outline-light')
                                    .removeClass('btn-outline-success')

                                $('.register').html('Register').css('font-size','large');
                            }, 3000);
                        }
                    },
                    error: function(){
                        console.log('that\'s something wrong.Please try again');
                    }
                })
        }
        else
        {
            $('.register')
                .removeClass('btn-outline-light')
                .addClass('btn-outline-danger');


            $('.register')
                .html('Insert a valid email')
                .css('font-size','small')
                .css('height','48px');

            setTimeout(function () {
                $('.register')
                    .addClass('btn-outline-light')
                    .removeClass('btn-outline-danger');

                $('.register').html('Register').css('font-size','large');
            }, 3000);
        }

    });

    $('.logout').on('click', function()
    {
        usr = '';

        clearContentSpace();
        clearDataSpace();

        $('.username').html('');

        $('.drawer-item').hide();
        $('.login-item').show();
    })

    $('.uploadDump').on('click', function()
    {
        let extension = $('#file-upload').val().split('.').pop().toLowerCase();
        if ($('#file-upload').val()===''){
            let alertmsg = 'Please select a file';
            responseMessage(alertmsg, 0);
        }
        else if ($.inArray(extension, ['zip', 'mbox']) == -1){
            let alertmsg = 'This extension is not allowed. Please select a correct file';
            responseMessage(alertmsg, 0);
        }
        else {
            let selected = $('input[name="wordFrecRadioOptions"]:checked');
            let wordFrecOption = $(selected).val();

            let file_data = $('#file-upload').prop('files')[0];
            let fd = new FormData();
            fd.append('file', file_data);
            // consistency checks made server side
            fd.append('user', usr);
            fd.append('wordFrecOption' , wordFrecOption);
            // upload dump on server
            $.ajax({
                url: 'server.php',
                dataType: 'text',
                cache: false,
                contentType: false,
                processData: false,
                data: fd,
                type: 'post',
                xhr: function() {
                    let xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener("progress", function(evt) {
                        if (evt.lengthComputable) {
                            let percentComplete = ((evt.loaded / evt.total) * 100);
                            percentComplete = Math.round(percentComplete);
                            $(".progress-bar").width(percentComplete + '%');
                            $(".progress-bar").html(percentComplete + '%');
                            if (percentComplete>=100) {
                                $('.upload-alert-msg')
                                    .show()
                                    .css({'color':'#f5f5f5ff','font-size':'xx-small', 'text-align':'center', 'margin-bottom':'10px'});;
                                $(".upload-alert-msg").html('Upload done. Waiting while data is processed');
                            }
                        }
                    }, false);


                    return xhr;
                },
                beforeSend:function(){
                    $('.upload-alert').show();
                    $('.progress').html('<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>').show()
                },
                success: function (php_script_response) {
                    setSliders(usr);
                    console.log(php_script_response);
                    responseMessage(php_script_response, 1);
                }
            });
        }

    });

    $('.searchData').on('click', function()
    {
        if (usr=='')
        {
            responseMessage('You must login before', 2)
        }
        else
        {
            let dts = '' ;
            let sn = $('.social').val();

            if (dataToSearch !== '' )
            {
                let pdts = JSON.parse(dataToSearch);
                dts = pdts['sn']
            }

            if (sn==dts)
                setEnvironment(usr);
            else
                setSliders(usr);
        }

    });

    $('.data').on('click', '.spoiler-btn',function(e)
    {
        e.preventDefault()
        $(this).parent().children('.spoiler-body').toggle()
    });

    $('.ordering-item').on('change', function()
    {
        let order_value = $('.ordering-item').val();
        let rangeValue = $('.dataViz1_selected').data('value');

        let action = 'getData';

        let dts = JSON.parse(dataToSearch);
        dts['sortValue'] = order_value;

        let ntd = getNodeToDisplay( dts['graphType'],  dts['sn']);

        dataToSearch = JSON.stringify(dts);

        if (rangeValue === 'filtered' || rangeValue === 'all')
            $.ajax({
            url: 'server.php',
            dataType: 'json',
            cache: false,
            data: {dataToSearch, action, ntd},
            type: 'post',
            beforeSend:function (){
                $('.data').html(
                    '<div class="row">' +
                    '<div class="col-4"></div>' +
                    '<div class="col-4">' +
                    '<div class="spinner-border text-dark" role="status" style="margin-top:5px; margin-left: 42%">' +
                    '<span class="sr-only"></span> '+
                    '</div>' +
                    '</div>' +
                    '<div class="col-4"></div>' +
                    '</div>')
            },
            success: function (data) {
                dataVisualization(data);
            },
            error: function ()
            {
                if (usr!=='')
                    $('.data').html(
                        '<div class="row">' +
                        '<div class="col-12">Select an element in the graph</div>' +
                        '</div>')
                else
                    clearDataSpace();
            }
        });
    });

    $(".block-physique").on('click', function()
    {
        viz.stabilize(); // to block the graph
    })

    $('.menu-title').on('click', function()
    {
        if ($('#collapseMenu').hasClass('show'))
        {
            $('.menu-title .material-icons').html('keyboard_arrow_down');
            $('.content').css('height','762px');
            $('.navigation').css('height','665px');

        }
        else
        {
            $('.menu-title .material-icons').html('keyboard_arrow_up');
            $('.content').css('height','662px');
            $('.navigation').css('height','565px');

        }
    })

    $('.title').on('click', function()
    {
        if ($('.manage-dumps-settings').hasClass('show') ||
            $('.upload-dump').hasClass('show') ||
            $('.manage-account-settings').hasClass('show')
        )
            $(".material-icons", this).html('keyboard_arrow_down');
        else
            $(".material-icons", this).html('keyboard_arrow_up');
    })

    $('.delete-dump').on('click', function()
    {
        let selected = $('input[name="social-to-delete"]:checked');
        let valueToDelete = $(selected).val();

        if ($(this).hasClass(valueToDelete)) {
            $.ajax({
                url: 'server.php',
                dataType: 'text',
                cache: false,
                data: {usr, valueToDelete},
                type: 'post',
                success: function (data) {
                    clearContentSpace();
                    clearDataSpace();

                    let actual = $(selected)
                                    .parent()
                                    .parent()
                                    .siblings('input');

                    let socialDeleted = $(actual).val();

                    $(actual).val(data).css('color','red');

                    setTimeout(function ()
                    {
                        $(actual).val(socialDeleted).css('color','white')
                    }, 3000)
                }
            });
        }
        else
            console.log('wrong')
    })

    $('.change').on('click', function()
    {
        let typedValue = '';
        let retypedValue = '';
        let action = '';

        if ($(this).parents().is('#manage-mail-settings'))
        {
            action = 'change-mail';
            typedValue = $(this).siblings().children('.new-mail').val();
            retypedValue = $(this).siblings().children('.new-mail-re').val();

        }
        else if ($(this).parents().is('#manage-password-settings'))
        {
            action = 'change-password';
            typedValue = $(this).siblings().children('.new-pass').val();
            retypedValue = $(this).siblings().children('.new-pass-re').val();
        }

        if (typedValue !== retypedValue )
        {
            $(this)
                .removeClass('btn-outline-light')
                .addClass('btn-outline-danger');
            $(this).html('Values don\'t match. Please reinsert');
            setTimeout(function () {
                $('.change')
                    .removeClass('btn-outline-danger')
                    .addClass('btn-outline-light');

                $('.change').html('Change');
            }, 3000);
        }
        else if (typedValue==='' || retypedValue==='')
        {
            $(this)
                .removeClass('btn-outline-light')
                .addClass('btn-outline-danger');
            $(this).html('One or more field are empty. Please retry');
            setTimeout(function () {
                $('.change')
                    .removeClass('btn-outline-danger')
                    .addClass('btn-outline-light');

                $('.change').html('Change');
            }, 3000);
        }

        else
            $.ajax({
                url: 'server.php',
                dataType: 'json',
                cache: false,
                data: {usr, typedValue, action},
                type: 'post',
                success: function (data) {
                    if (action == 'change-password')
                    {
                        $('.manage-password-settings .change')
                            .removeClass('btn-outline-light')
                            .addClass('btn-outline-success');
                        $('.manage-password-settings .change').html(data['value']);
                        setTimeout(function () {
                            $('.change')
                                .removeClass('btn-outline-success')
                                .addClass('btn-outline-light');

                            $('.change').html('Change');
                        }, 3000);
                    }
                    else if (action == 'change-mail')
                    {
                        usr = data['user_mail'];
                        $('.username').html(usr);
                        $('.manage-mail-settings .change')
                            .removeClass('btn-outline-light')
                            .addClass('btn-outline-success');
                        $('.manage-mail-settings .change').html(data['value']);
                        setTimeout(function () {
                            $('.change')
                                .removeClass('btn-outline-success')
                                .addClass('btn-outline-light');

                            $('.change').html('Change');
                        }, 3000);
                    }

                }
            });
    })

    $('.fb-user-type').on('change', function()
    {
        setEnvironment(usr);
    })

    $('.fb-map').on('change', function()
    {
        setEnvironment(usr);
    })

    $('.fb-node-type').on('change', function()
    {
        setEnvironment(usr);
    })

    $('.tw-user-type').on('change', function()
    {
        setEnvironment(usr);
    })

    $('.tw-node-type').on('change', function()
    {
        setEnvironment(usr);
    })

    $('.tweet-type').on('change', function()
    {
        setEnvironment(usr);
    })

    $('.social').on('change', function()
    {
        let sn = $('.social').val();

        if (sn==='facebook' || sn === 'twitter')
        {
            $('.label-info-nodes').attr('data-original-title', 'Node value rappresent how many times a specific person was tagged by the property of dump');
            $('.label-info-edges').attr('data-original-title', 'Edge value rappresent how many times two people are tagged together');
        }
        else
        {
            $('.label-info-nodes').attr("data-original-title","Node value is the sum of all connected edges weight");
            $('.label-info-edges').attr("data-original-title","Edge value equals the number of emails between two nodes");
        }
    })

    $('.app-help').on('click', function(){
        var e = jQuery.Event("keydown");
        e.which = 27; // # Some key code value
        $('.drawer').trigger(e);
    })
});

function responseMessage (alertmsg, alertvalue)
{
    clearContentSpace();
    clearDataSpace();

    // change the uploadDump button
    if (alertvalue===0) {
        $('.uploadDump')
            .removeClass('btn-outline-light')
            .addClass('btn-outline-danger')
            .css('font-size', 'small');
        $('.uploadDump').html(alertmsg);
        setTimeout(function () {
            $('.uploadDump')
                .removeClass('btn-outline-danger')
                .addClass('btn-outline-light')
                .css('font-size', 'large');
            $('.upload-alert-msg').css('display', 'none');
            $('.uploadDump').html('Upload file');
        }, 3000);
    }
    // dump correctly upload
    else if (alertvalue===1){
        $('.progress').css('display', 'none');
        $('.upload-alert-msg')
            .html(alertmsg)
            .removeAttr('style')
            .css({'color':'#7CFC00','font-size':'small', 'text-align':'center', 'margin-bottom':'10px'});
        setTimeout(function () {
            $('.upload-alert-msg').css('display', 'none');
            $('.upload-alert').css('display', 'none');
        }, 6000);

    }
    // change the searchData button
    else if (alertvalue===2) {
        $('.searchData')
            .removeClass('btn-outline-dark')
            .addClass('btn-outline-danger');
        $('.searchData').html(alertmsg);
        setTimeout(function () {
            $('.searchData')
                .removeClass('btn-outline-danger')
                .addClass('btn-outline-dark');
            $('.search_alert').css('display', 'none');
            $('.searchData').html('Search');
        }, 3000);
    }
}

function setSliders(usr)
{
    let sn = $('.social').val();

    $.ajax({
        url: 'server.php',
        dataType: 'json',
        data: {usr, sn},
        type: 'post',
        success: function (data) {

            $( "#amountNode" ).html('0');
            $( ".nodeSlider" ).slider({
                range: "max",
                min: 0,
                max: data[2],
                value: 0,
                change: function( event, ui ){
                    setEnvironment(usr)
                },
                slide: function( event, ui ) {
                    $( "#amountNode" ).html(ui.value );
                }
            });

            $( "#amountEdge" ).html('0' );
            $( ".edgeSlider" ).slider({
                range: "max",
                min: 0,
                max: data[3],
                value: 0,
                change: function( event, ui ){
                    setEnvironment(usr)
                },
                slide: function( event, ui ) {
                    $( "#amountEdge" ).html(ui.value );
                }
            });

            $( "#amount" ).html(getTodayDate('notoday') +' - '+ getTodayDate('today'));
            $( "#slider-range" ).slider({
                range: true,
                min: new Date(data[0]).getTime() / 1000,
                max: new Date(data[1]).getTime() / 1000,
                step: 86400,
                values: [ new Date(getTodayDate('notoday')).getTime() / 1000, new Date(getTodayDate('today')).getTime() / 1000 ],
                change: function( event, ui ){
                    setEnvironment(usr)
                },
                slide: function( event, ui ) {
                    let startDate = formatDate(new Date(ui.values[ 0 ] *1000).toDateString());
                    let endDate = formatDate(new Date(ui.values[ 1 ] *1000).toDateString());
                    $( "#amount" ).html(startDate + ' - ' + endDate );
                }
            });

            setEnvironment(usr);
        },
        error: function (){
            dataToSearch = '';
            noDataFoundVisualization();
        },
    });
}

function setEnvironment(usr)
{
    clearDataSpace();

    if (usr !=='') {
        let {keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, graphType, dataViz1, dataViz2, sortValue} = setVariableForSearching();

        let {cmd, direction} = createQueryForDrawing(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType);

        dataToSearch = dataToSearchJSONCreator(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr, graphType, dataViz1, dataViz2, sortValue);

        let dimension = getNodeDimension(sn, graphType);

        let ntd = getNodeToDisplay(graphType, sn);

        if (graphType === 'relNet' || graphType === 'trafficNet')
        {

            if (sn === 'facebook') {
                $('.tw-filtering-rel').hide();
                $('.tw-filtering-trafficNet').hide();
                $('.fb-filtering-map').hide();

                if (graphType === 'relNet') {
                    $('.fb-filtering-trafficNet').hide();
                    $('.fb-filtering-rel').show();
                }
                else if (graphType === 'trafficNet') {
                    $('.fb-filtering-rel').hide();
                    $('.fb-filtering-trafficNet').show();
                }
            }
            else if (sn === 'twitter') {
                $('.fb-filtering-rel').hide();
                $('.fb-filtering-trafficNet').hide();
                $('.fb-filtering-map').hide();

                if (graphType === 'relNet') {
                    $('.tw-filtering-trafficNet').hide();
                    $('.tw-filtering-rel').show();
                } else if (graphType === 'trafficNet') {
                    $('.tw-filtering-rel').hide();
                    $('.tw-filtering-trafficNet').show();
                }
            }
            else if (sn === 'mbox') {
                $('.fb-filtering-rel').hide();
                $('.fb-filtering-trafficNet').hide();
                $('.tw-filtering-rel').hide();
                $('.tw-filtering-trafficNet').hide();
            }

            $('.block-physique').show();
            drawGraph(cmd, direction, dimension);
        }
        else if (graphType === 'map')
        {
            let data = [];
            clearContentSpace();
            $('.block-physique').hide();

            let markersToDisplay = '';

            if (sn === 'facebook') {
                $('.fb-filtering-rel').hide();
                $('.fb-filtering-trafficNet').hide();
                $('.fb-filtering-map').show()
                    .css('padding-left', '37px');

                let selected = $('input[name="fb-map"]:checked');
                let snMarkers = $(selected).val();

                markersToDisplay = snMarkers;
            } else if (sn === 'twitter') {
                $('.tw-filtering-rel').hide();
                $('.tw-filtering-trafficNet').hide();
                $('.fb-filtering-map').hide();

                let selected = $('input[name="fb-map"]:checked');
            }

            let action = 'getMarker';
            $.ajax({
                url: 'server.php',
                dataType: 'json',
                data: {dataToSearch, action, markersToDisplay},
                type: 'post',
                success: function (data) {
                    createWorldMap(data);
                },
                error: function () {
                    dataToSearch = '';
                    noDataFoundVisualization();
                },
            });

        }
        else if (graphType === 'wordFrec')
        {
            $('.block-physique').hide();
            $('.fb-filtering-rel').hide();
            $('.fb-filtering-trafficNet').hide();
            $('.fb-filtering-map').hide();
            $('.tw-filtering-rel').hide();
            $('.tw-filtering-trafficNet').hide();

            clearContentSpace();
            getWords(dataToSearch);
        }

        $('.dataViz1').removeClass('dataViz1_selected');
        $('.selected').addClass('dataViz1_selected');

        $('.dataViz2').removeClass('dataViz2_selected');
        $('.contacts').addClass('dataViz2_selected');

        let dts = JSON.parse(dataToSearch);

        dts['dataViz2'] = $('.dataViz2_selected').data('value');
        dts['dataViz1'] = $('.dataViz1_selected').data('value');

        dataToSearch = JSON.stringify(dts);


        if (graphType === 'relNet' || graphType === 'trafficNet'|| graphType === 'map' )
        {
            let action = 'getData';
            $.ajax({
                url: 'server.php',
                dataType: 'json',
                data: {dataToSearch, action, ntd},
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
                success: function (data) {
                    dataVisualization(data);
                },
                error: function () {
                    console.log('errore');
                },
            });
        }
    }
}

function setVariableForSearching()
{
    let keyword = $('.searchKeyword').val();
    let person = $('.searchPerson').val();
    let sn = $('.social').val();
    let minNodevalue = $( ".nodeSlider" ).slider('value');
    let minEdgeValue = $( ".edgeSlider" ).slider('value');
    let start_date = formatDate(new Date($( "#slider-range" ).slider('values')[0] *1000).toDateString());
    let end_date = formatDate(new Date($( "#slider-range" ).slider('values')[1] *1000).toDateString());
    let graphType = $('.graphType_selected').data('value');
    let dataViz1 = $('.dataViz1_selected').data('value');
    let dataViz2 = $('.dataViz2_selected').data('value');
    let sortValue =  $('.ordering-item').val();

    return {keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn , graphType, dataViz1, dataViz2, sortValue}
}

function noDataFoundVisualization()
{
    $('.data').html(
        '<div class="noDataFound"><i class=" text-center material-icons">error</i></div>' +
        '<div class="noDataFound">There isn’t any data that can satisfy your research</div>'
    );
}

function dataToSearchJSONCreator(keyword, person, start_date, end_date, minNodevalue, minEdgeValue, sn, usr , graphType, dataViz1, dataViz2, sortValue)
{
    let obj = new Object();
    obj.keyword = keyword;
    obj.person = person;
    obj.start_date = start_date;
    obj.end_date = end_date;
    obj.minNodevalue = minNodevalue;
    obj.minEdgeValue = minEdgeValue;
    obj.sn = sn;
    obj.graphType = graphType;
    obj.dataViz1 = dataViz1;
    obj.dataViz2 = dataViz2;
    obj.usr = usr;
    obj.sortValue = sortValue;

    return JSON.stringify(obj);
}

function clearDataSpace()
{
    $('.data').html('');
}

function clearContentSpace()
{
    $('.content').html('');
}

function getTodayDate(when)
{
    let d = new Date();

    let month = d.getMonth()+1;
    let day = d.getDate();

    let today;
    if (when == 'today')
        today = d.getFullYear() + '.' +
            ((''+month).length<2 ? '0' : '') + month + '.' +
            ((''+day).length<2 ? '0' : '') + day;
    else
        today = d.getFullYear()-1 + '.' +
            ((''+month).length<2 ? '0' : '') + month + '.' +
            ((''+day).length<2 ? '0' : '') + day;

    return today.toString();
}

function formatDate(date)
{
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('/');
}

function validateEmail(email)
{
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function getNodeToDisplay(graphType, sn)
{
    let ntd = ''
    if (graphType ==='relNet')
    {
        if (sn==='facebook')
        {
            let selected = $('input[name="fb-user-type"]:checked');
            ntd = $(selected).val();
        }
        else if (sn==='twitter')
        {
            let selected = $('input[name="tw-user-type"]:checked');
            ntd = $(selected).val();
        }
        else if (sn==='mbox')
        {

        }
    }
    else if (graphType ==='trafficNet')
    {
        if (sn==='facebook')
        {
            let selected = $('input[name="fb-node-type"]:checked');
            ntd = $(selected).val();
        }
        else if (sn==='twitter')
        {
            let selected = $('input[name="tweet-type"]:checked');
            ntd = $(selected).val();
        }
        else if (sn==='mbox')
        {

        }
    }
    else if (graphType ==='map')
    {
        if (sn === 'facebook')
        {
            let selected = $('input[name="fb-map"]:checked');
            ntd = $(selected).val();
        }
        else if (sn==='twitter')
        {

        }
    }

    return ntd;
}

function enableDisableButtons()
{
    let graphType = $('.graphType_selected').data('value');

    if (graphType==='relNet')
    {
        $(".filtered").prop("disabled", false);
        $(".all").prop("disabled", false);
        $(".links").prop("disabled", false);
        $('.custom-select-ordering-item').prop("disabled", false);
        $(".contacts").prop("disabled", false);
        $('.dataViz1').removeClass('.dataViz1_selected');
        $('.filtered').addClass('.dataViz1_selected');
        $('.dataViz2').removeClass('.dataViz2_selected');
        $('.Contacts').addClass('dataViz1_selected');
    }
    else if (graphType==='trafficNet')
    {
        $('.dataViz1').removeClass('.dataViz1_selected');
        $('.selected').addClass('.dataViz1_selected');
        $(".links").prop("disabled", false);
        $('.custom-select-ordering-item').prop("disabled", false);
        $(".contacts").prop("disabled", false);
        $(".filtered").prop("disabled", true);
        $(".all").prop("disabled", true);
        $(".links").prop("disabled", true);
    }
    else if (graphType==='map')
    {
        $(".links").prop("disabled", true);
        $('.custom-select-ordering-item').prop("disabled", false);
        $(".contacts").prop("disabled", true);

        $(".filtered").prop("disabled", false);
        $(".all").prop("disabled", false);
    }
    else
    {
        $(".contacts").prop("disabled", true);
        $(".links").prop("disabled", true);
        $('.custom-select-ordering-item').prop("disabled", true);
    }
}

/* QUERY FILTERING */

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
    //console.log(cmd);
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