load_cycles();


const map = L.map('map').setView([48, 12], 5);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
let index = null;
let markers = L.geoJSON(null, {
    pointToLayer: createClusterIcon,
    onEachFeature
}).addTo(map);
const search_bar = document.getElementById("point-search");
let ready = false;
let searchTerm = null

map.on('moveend', updateMarkers);
search_bar.addEventListener("input", update_search)


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

async function update_search() {
    searchTerm = search_bar.value;
    updateMarkers();
}

async function load_cycles() {
    let uri = "http://localhost:8050/available"
    available_cycles = await (await fetch(uri)).json();
    let cycle_switch = document.getElementById("cycle-switch");
    bestOption = null
    available_cycles.sort((a, b) => a.split("-")[1] < b.split("-")[1]).forEach((e, i) => {
        if (!bestOption) {
            bestOption = e
        }
        cycle_switch.options[i] = new Option(e.split("-")[1], e);
    })

    cycle_switch.addEventListener("input", switch_cycle)

    setup_geo_json_layer(bestOption);
}

async function switch_cycle(newoption) {
    let cycle_switch = document.getElementById("cycle-switch");
    markers.clearLayers();
    setup_geo_json_layer(cycle_switch.value)
}

async function setup_geo_json_layer(option) {
    let uri = `http://localhost:8050/static/${option}`
    // let uri = "https://cdn.rawgit.com/mapbox/supercluster/v4.0.1/test/fixtures/places.json"
    geo_json = await (await fetch(uri)).json();
    index = new Supercluster({
        radius: 100, // Cluster radius in pixels
        minZoom: 2,
        minPoints: 8
    }).load(geo_json.features);
    ready = true;
    updateMarkers();
}

function onEachFeature(feature, layer) {
    if (feature.properties && feature.properties.tooltip) {
        layer.bindTooltip(`${feature.properties.tooltip}`)
        layer.bindPopup(`${feature.properties.tooltip}`)
    }
}

// Function to create markers or clusters
function updateMarkers() {
    if (!ready) return;
    var bounds = map.getBounds();
    var bbox = [bounds.getWest(), bounds.getSouth(), bounds.getEast(), bounds.getNorth()];
    var zoom = map.getZoom();
    var clusters = index.getClusters(bbox, zoom);
    markers.clearLayers();
    if (searchTerm) {
        console.log(clusters)
        markers.addData(index.points.filter(e => e?.properties?.name != null && e.properties.name.toUpperCase().includes(searchTerm.toUpperCase())));
    }
    else {
        markers.addData(clusters);
    }


}

function createClusterIcon(feature, latlng) {
    if (!feature.properties.cluster) {
        const flag = L.icon({ iconUrl: `./resources/${feature.properties.role}.svg`, iconSize: [24, 24] });
        return L.marker(latlng, { icon: flag, title: feature.properties.name });
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
