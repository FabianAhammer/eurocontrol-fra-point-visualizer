
var map = L.map('map').setView([48, 12], 5);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
let index = null;
let markers = L.geoJSON(null, {
    pointToLayer: createClusterIcon
}).addTo(map);
setup_geo_json_layer(map);
ready = false;
// Add initial markers

// Zoom to expand the cluster clicked by user.
markers.on('click', function (e) {
    var clusterId = e.layer.feature.properties.cluster_id;
    var center = e.latlng;
    var expansionZoom;
    if (clusterId) {
        expansionZoom = index.getClusterExpansionZoom(clusterId);
        map.flyTo(center, expansionZoom);
    }
});


async function setup_geo_json_layer(map) {
    let uri = "http://localhost:8050/static/eurocontrol-2410-fra-points-03oct2024.json"
    // let uri = "https://cdn.rawgit.com/mapbox/supercluster/v4.0.1/test/fixtures/places.json"
    geo_json = await (await fetch(uri)).json();
    index = new Supercluster({
        radius: 100, // Cluster radius in pixels
        minZoom: 2,
        minPoints: 8
    }).load(geo_json.features);
    ready = true;
    updateMarkers();
    map.on('moveend', updateMarkers);
}

// Function to create markers or clusters
function updateMarkers() {
    if (!ready) return;
    var bounds = map.getBounds();
    var bbox = [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()];
    var zoom = map.getZoom();
    var clusters = index.getClusters(bbox, zoom);
    markers.clearLayers();
    markers.addData(clusters);
}

function createClusterIcon(feature, latlng) {
    if (!feature.properties.cluster) {
        const flag = L.icon({ iconUrl: `./resources/${feature.properties.role}.svg`, iconSize: [24, 24] });
        return L.marker(latlng, { icon: flag });
    }

    var count = feature.properties.point_count;
    var size =
        count < 100 ? 'small' :
            count < 1000 ? 'medium' : 'large';
    var icon = L.divIcon({
        html: '<div><span>' + feature.properties.point_count_abbreviated + '</span></div>',
        className: 'marker-cluster marker-cluster-' + size,
        iconSize: L.point(40, 40)
    });

    return L.marker(latlng, {
        icon: icon
    });
}
