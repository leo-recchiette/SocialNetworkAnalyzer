import $ from 'jquery'
import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import OSM from 'ol/source/OSM'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import Feature from 'ol/Feature'
import Point from 'ol/geom/Point'
import { Style, Icon } from 'ol/style'
import { fromLonLat, transform } from 'ol/proj'
import 'ol/ol.css'
import { sna } from './bridge.js'
import { clearDataSpace } from './dom.js'
import { dataVisualization } from './dataVisualization.js'

function createWorldMap(data)
{
    $('.content').html(
        '<div id="map" class="map" style="height: 100%; width: 100%"></div>'
    )

    var map = new Map({
        target: 'map',
        layers: [
            new TileLayer({
                source: new OSM()
            })
        ],
        view: new View({
            center: fromLonLat([12.51, 41.89]),
            zoom:6
        })
    });

    let markers = getMarkers(data);

    var features = [];

    for (var i = 0; i < markers.length; i++) {
        var item = markers[i];
        var longitude = item.lng;
        var latitude = item.lat;

        var iconFeature = new Feature({
            geometry: new Point(transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'))
        });

        var iconStyle = new Style({
            image: new Icon(({
                anchor: [0.5, 1],
                src: "https://unpkg.com/leaflet@1.6.0/dist/images/marker-icon.png"
            }))
        });

        iconFeature.setStyle(iconStyle);
        features.push(iconFeature);

    }

    var vectorSource = new VectorSource({
        features: features
    });

    var vectorLayer = new VectorLayer({
        source: vectorSource
    });
    map.addLayer(vectorLayer);

    map.on('singleclick', function(evt){
        let features = map.getFeaturesAtPixel(evt.pixel);
        if (features.length > 0) {
            let coordinate = features[0].getGeometry().getCoordinates();
            let lat = transform(coordinate, 'EPSG:3857', 'EPSG:4326')[0];
            let lng = transform(coordinate, 'EPSG:3857', 'EPSG:4326')[1];

            sna.setDataViz1('selected');
            sna.setDataViz2('contacts');

            let dts = JSON.parse(sna.dataToSearch);

            dts['dataViz1'] = 'selected';
            dts['dataViz2'] = 'contacts';

            sna.dataToSearch = JSON.stringify(dts);


            $.ajax({
            url: 'server.php',
            dataType: 'json',
            data: {dataToSearch: sna.dataToSearch, lat, lng},
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

    let sn = sna.sn;

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

export { createWorldMap }