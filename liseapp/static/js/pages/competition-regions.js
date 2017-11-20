
initMap();


function initMap() {
  var lngs = document.getElementById("map").getAttribute("data-lngs");
  lngs = lngs.substring(1,lngs.length-1).replace(/[\\']/g, "").split(', ');
  var lats = document.getElementById("map").getAttribute("data-lats");
  lats = lats.substring(1,lats.length-1).replace(/[\\']/g, "").split(', ');


  var heatmapData = new Array();

  for (var i = 0; i < lats.length; i++) {
    heatmapData.push(new google.maps.LatLng(parseFloat(lats[i]), parseFloat(lngs[i])))
  };
  
  var teresina = new google.maps.LatLng(
-5.0920108, -42.80375970000001);
  
  map = new google.maps.Map(document.getElementById('map'), {
    center: teresina,
    zoom: 12,
    panControl: false,
    draggable: true,
    zoomControl: false,
    streetViewControl: false,
    scrollwheel: false
  });
  
  
  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData
  });
  heatmap.setMap(map);
  
   var gradient = [
        'rgba(0, 255, 255, 0)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)',
        'rgba(96, 125, 139, 0.8)'
   ]
   heatmap.set('gradient', gradient);
  
   heatmap.set('radius', 15);

}