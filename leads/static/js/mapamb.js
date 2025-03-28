mapboxgl.accessToken = 'pk.eyJ1Ijoidml2aXMyIiwiYSI6ImNtOHJ6bWgxaDEzbXgyam9tZjZ5eDNjcDUifQ.ZSV7rDNcxZuEKXzWEFu7pQ';  // token

        let map = new mapboxgl.Map({
            container: 'mapContainer',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [-74.5, 40],  // Ejemplo de coordenadas
            zoom: 9
        });

        function obtenerColorEstado(estado) {
            switch (estado) {
                case "Prospecto":
                    return "#f7dc6f";
                case "Cliente Nuevo":
                    return "#2ecc71";
                case "Ya era Cliente":
                    return "#6bbbfa";
                case "Descartado":
                    return "#909497";
                default:
                    return "white";  
            }
        }

        function agregarPuntos(datos) {
            datos.forEach(unidad => {
                let color = obtenerColorEstado(unidad.estado);

                new mapboxgl.Marker({
                    color: color
                })
                .setLngLat([unidad.Longitud, unidad.Latitud])
                .addTo(map);
            });
        }

        // Llama a la función que obtenga y pase los datos a agregarPuntos
        // ejemplo: agregarPuntos(data);