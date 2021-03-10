function createWorldMap(data)
{
    $('.content').html(
        '<div id="map" class="map" style="height: 100%; width: 100%"></div>'
    )

    var map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([12.51, 41.89]),
            zoom:6
        })
    });

    let markers = getMarkers(data);

    var features = [];

    for (var i = 0; i < markers.length; i++) {
        var item = markers[i];
        var longitude = item.lng;
        var latitude = item.lat;

        var iconFeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'))
        });

        var iconStyle = new ol.style.Style({
            image: new ol.style.Icon(({
                anchor: [0.5, 1],
                //src: "http://cdn.mapmarker.io/api/v1/pin?text=P&size=50&hoffset=1"
                src: "https://unpkg.com/leaflet@1.6.0/dist/images/marker-icon.png"
            }))
        });

        iconFeature.setStyle(iconStyle);
        features.push(iconFeature);

    }

    var vectorSource = new ol.source.Vector({
        features: features
    });

    var vectorLayer = new ol.layer.Vector({
        source: vectorSource
    });
    map.addLayer(vectorLayer);

    map.on('singleclick', function(evt){
        let features = map.getFeaturesAtPixel(evt.pixel);
        if (features.length > 0) {
            let coordinate = features[0].getGeometry().getCoordinates();
            let lat = ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326')[0];
            let lng = ol.proj.transform(coordinate, 'EPSG:3857', 'EPSG:4326')[1];

            $('.dataViz1').removeClass('dataViz1_selected');
            $('.selected').addClass('dataViz1_selected');

            $('.dataViz2').removeClass('dataViz2_selected');
            $('.contacts').addClass('dataViz2_selected');

            let dts = JSON.parse(dataToSearch);

            dts['dataViz1'] = $('.dataViz1_selected').data('value');
            dts['dataViz2'] = $('.dataViz2_selected').data('value');

            dataToSearch = JSON.stringify(dts);


            $.ajax({
            url: 'server.php',
            dataType: 'json',
            data: {dataToSearch, lat, lng},
            type: 'post',
            success: function (data) {
                clearDataSpace();
                dataVisualization (data);
            },
            error: function (data) {
                clearDataSpace()
                $('.data').append(
                    '<div class="data-item">' +
                    '<span> Try to select a place on the map </span>' +
                    '</div>'
                );
            },
        })
        }
    });
}

function getMarkers(data)
{
    let mapMarkers = [];

    let sn = $('.social').val();

    for (let index = 0; index < data.length; index ++)
    {
        if (sn === 'facebook')
        {
            if ('post' in data[index]['p']) {
                let placeName = data[index]['p']['place_address']
                let latitude = data[index]['p']['place_latitude'];
                let longitude = data[index]['p']['place_longitude'];

                mapMarkers.push({name: placeName, lat: latitude, lng: longitude});
            }

            else
            {
                let placeName = data[index]['p']['name']
                let latitude = data[index]['p']['place_latitude'];
                let longitude = data[index]['p']['place_longitude'];

                mapMarkers.push({name: placeName, lat: latitude, lng: longitude});
            }
        }
        if (sn === 'twitter')
        {
            let latitude = data[index]['place']['latitude'];
            let longitude = data[index]['place']['longitude'];

            mapMarkers.push({lat: latitude, lng: longitude});
        }

    }
    return mapMarkers;
}