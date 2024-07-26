window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng) {
            const flag = L.icon({
                iconUrl: `./assets/${feature.properties.role}.svg`,
                iconSize: [24, 24]
            });
            return L.marker(latlng, {
                icon: flag
            });
        }
    }
});