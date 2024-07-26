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
        },
        function1: function(feature, context) {
            if (!feature?.properties?.name)
                return true
            return context.hideout.length == 0 || context.hideout.find(e => feature.properties.name.toLowerCase().includes(e.toLowerCase()))
        }
    }
});