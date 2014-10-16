function hexFromRGB(r, g, b) {
    var hex = [
      r.toString( 16 ),
      g.toString( 16 ),
      b.toString( 16 )
    ];
    $.each( hex, function( nr, val ) {
      if ( val.length === 1 ) {
        hex[ nr ] = "0" + val;
      }
    });
    return hex.join( "" ).toUpperCase();
  }
function refreshLabel() {
    var rslider = $( "#rslider" ).slider( "value" ),
      gslider = $( "#gslider" ).slider( "value" ),
      bslider = $( "#blue" ).slider( "value" ),
      hex = hexFromRGB( rslider, gslider, bslider );
    $( "#swatch" ).css( "background-color", "#" + hex );
  }
$(function() {
  $( "#rslider, #gslider, #bslider" ).slider({
    orientation: "horizontal",
    range: "min",
    max: 255,
    value: 127,
    slide: refreshLabel,
    change: refreshLabel
  });
  $( "#rslider" ).slider( "value", 255 );
  $( "#gslider" ).slider( "value", 140 );
  $( "#bslider" ).slider( "value", 60 );
});

$(function() {
    $( "#slider" ).slider({
      value:100,
      min: 0,
      max: 500,
      step: 50,
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.value );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider" ).slider( "value" ) );
});

/* progress bar update*/
$(function() {
  $( "#progressbar" ).progressbar({
    value: false
  });
  progressbar = $( "#progressbar" ),
  progressbar.progressbar( "option", {
  value: Math.floor( Math.random() * 100 )
  });
});
$(document).ready(function(){
  $("#arrow-down").click(function(){
    $("#slipper").toggle("slow");
  });
});

$(document).ready(function(){
  $("#arrow-down-veg").click(function(){
    $("#slipper-veg").toggle("slow");
  });
});

$(document).ready(function(){
  $("#arrow-down-fibre").click(function(){
    $("#slipper-fibre").toggle();
  });
});
$(document).ready(function(){
  $("#arrow-down-salt").click(function(){
    $("#slipper-salt").toggle();
  });
});

$(document).ready(function(){
  $("#arrow-down-fat").click(function(){
    $("#slipper-fat").toggle();
  });
});

$(document).ready(function(){
  $("#arrow-down-bmi").click(function(){
    $("#slipper-bmi").toggle();
  });
});
$(document).ready(function(){
  $("#arrow-down-pa").click(function(){
    $("#slipper-pa").toggle();
  });
});

$(document).ready(function(){
  $("#arrow-down-alcohol").click(function(){
    $("#slipper-alcohol").toggle();
  });
});

$(document).ready(function(){
  $("#arrow-down-smoking").click(function(){
    $("#slipper-smoking").toggle();
  });
});

google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);
function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ['Year', 'Sales', 'Expenses'],
    ['2004',  1000,      400],
    ['2005',  1170,      460],
    ['2006',  660,       1120],
    ['2007',  1030,      540]
  ]);

  var options = {
    title: 'Company Performance',
    hAxis: {title: 'Year',  titleTextStyle: {color: '#333'}},
    vAxis: {minValue: 0}
  };

  var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

$('.accordion').on('show hide', function (n) {
    $(n.target).siblings('.accordion-heading').find('.accordion-toggle i').toggleClass('icon-chevron-up icon-chevron-down');
});

$('#slipper').on('shown.bs.collapse', function () {
   $(".glyphicon").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
});

$('#slipper').on('hidden.bs.collapse', function () {
   $(".glyphicon").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
});

/*
	google map
*/
function MapInitialize()
{
   var mapProp = {
       center:new google.maps.LatLng(51.752854,-1.214993),
       zoom:11,
       mapTypeId:google.maps.MapTypeId.ROADMAP
   };
   var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

google.maps.event.addDomListener(window, 'load', MapInitialize);

function loadScript()
{
   var script = document.createElement("script");
   script.type = "text/javascript";
   script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyBO4EHdS534vJDO-UPAbdMcS7bJfe7oJvc&sensor=false&callback=initialize";
   document.body.appendChild(script);
}

window.onload = loadScript;

$(document).ready(function(){
				  $("#btn-reset").click(function(){
				  			alert('fs'); 
							    });
				  });

