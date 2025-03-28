let map; // Variable global para el mapa

function inicializarMapa(lat, lon) {
    // Eliminar mapa anterior si existe
    if (map) {
        map.setTarget(null);
    }

    map = new ol.Map({
        target: 'mapContainer',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([lon, lat]),
            zoom: 15
        })
    });

    // Agregar marcador en la ubicación de la unidad
    const marker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
    });

    const vectorSource = new ol.source.Vector({
        features: [marker]
    });

    const vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: new ol.style.Style({
            image: new ol.style.Icon({
                anchor: [0.5, 1],
                src: 'https://cdn-icons-png.flaticon.com/32/684/684908.png'  // Icono de marcador
            })
        })
    });

    map.addLayer(vectorLayer);
}
