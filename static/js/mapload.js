
var url = window.location.href + '/mapa'

$.get(url, function(list) {
	
	map = new OpenLayers.Map("mapdiv");
	map.addLayer(new OpenLayers.Layer.OSM());
	
	epsg4326 =  new OpenLayers.Projection("EPSG:4326"); //WGS 1984 projection
	projectTo = map.getProjectionObject(); //The map projection (Spherical Mercator)
   
	var vectorLayer = new OpenLayers.Layer.Vector("Overlay");
	
			
	propiedades = JSON.parse(list);		
	size = Object.keys(propiedades['Latitud']).length;
	
	var center_lat = -33.81263971;
	var center_lon = -61.87367427;
	var zoom = 10;
	
	for(var i= 0; i < size; i++)
	{

		idx = propiedades['GlobalId'][i];
		lat = propiedades['Latitud'][i];
		lon = propiedades['Longitud'][i];
		marca = propiedades['marca'][i];
		msj = idx + ',' + lat + ',' + lon
		
		var feature = new OpenLayers.Feature.Vector(
			new OpenLayers.Geometry.Point(lon, lat ).transform(epsg4326, projectTo),
			{description: msj} ,
			{externalGraphic: marca, graphicHeight: 25, graphicWidth: 21, graphicXOffset:-12, graphicYOffset:-25  }
		);    
		vectorLayer.addFeatures(feature);
	}   
		
	var lonLat = new OpenLayers.LonLat( center_lon, center_lat ).transform(epsg4326, projectTo);        
	map.setCenter (lonLat, zoom);
	   
	map.addLayer(vectorLayer);
 
	
	//Add a selector control to the vectorLayer with popup functions
	var controls = {
	  selector: new OpenLayers.Control.SelectFeature(vectorLayer, { onSelect: createPopup, onUnselect: destroyPopup })
	};

	function createPopup(feature) {
	  feature.popup = new OpenLayers.Popup.FramedCloud("pop",
		  feature.geometry.getBounds().getCenterLonLat(),
		  null,
		  '<div class="markerContent">'+feature.attributes.description+'</div>',
		  null,
		  true,
		  function() { controls['selector'].unselectAll(); }
	  );
	  //feature.popup.closeOnMove = true;
	  map.addPopup(feature.popup);
	}

	function destroyPopup(feature) {
	  feature.popup.destroy();
	  feature.popup = null;
	}
	
	map.addControl(controls['selector']);
	controls['selector'].activate();
	

}); 

      
