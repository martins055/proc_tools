<html>
  <head>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <script src="js/jquery.min.js"></script>
    <script src="js/socket.io.js"></script>
    <script src="js/plotly-latest.min.js"></script>
  </head>
  <body>

<div class="container-fluid" style="width: 99%;margin:0px">

    <div class="row">
        <div class="col-lg-4 col-md-6" id="divemg0" style="height: 32vh"></div>
        <div class="col-lg-4 col-md-6" id="divemg1" style="height: 32vh"></div>
        <div class="col-lg-4 col-md-6" id="divemg2" style="height: 32vh"></div>
    </div>
    <div class="row">
        <div class="col-lg-4 col-md-6" id="divemg3" style="height: 32vh"></div>
        <div class="col-lg-4 col-md-6" id="divemg4" style="height: 32vh"></div>
        <div class="col-lg-4 col-md-6" id="divemg5" style="height: 32vh"></div>
    </div>
    <div class="row">
        <div class="col-lg-6 col-md-6" id="divemg6" style="height: 32vh"></div>
        <div class="col-lg-6 col-md-6" id="divemg7" style="height: 32vh"></div>
    </div>

</div>


<script>

//************************************************
// Create the EMG graphs
//************************************************

// The graphs will be updated later
 var emg_window_size_total = 3240 // Size of the table that contains the EMG data
 var emg_window_size_newdata = 270 // Part of the table that will be updated with new EMG data (from the python script)

  // Fill X axis
  var xaxis = [];
  for (var i = 1; i <= emg_window_size_total; i++) { xaxis.push(i) }
  
  // Create Y axis for each EMG
  var arrayLength = emg_window_size_total
  var newArray_emg0 = []
  var newArray_emg1 = []
  var newArray_emg2 = []
  var newArray_emg3 = []
  var newArray_emg4 = []
  var newArray_emg5 = []
  var newArray_emg6 = []
  var newArray_emg7 = []

  // Fill all the the Y with 0 values
  for(var i = 0; i < arrayLength; i++) {
    var y = 0
    newArray_emg0[i] = y
    newArray_emg1[i] = y
    newArray_emg2[i] = y
    newArray_emg3[i] = y
    newArray_emg4[i] = y
    newArray_emg5[i] = y
    newArray_emg6[i] = y
    newArray_emg7[i] = y
  }

// define the layout that will be used for the graphs
var custom_layout_emg_global = { title: 'EMG waiting', font: {size: 18}, yaxis: {range: [-0.0005, 0.0005]} };

Plotly.plot('divemg0', [{ y: newArray_emg0, mode: 'lines', line: {color: '#80CAF6'} }], custom_layout_emg_global, {staticPlot: true} );
Plotly.plot('divemg1', [{ y: newArray_emg1, mode: 'lines', line: {color: '#80CAF6'} }], custom_layout_emg_global, {staticPlot: true} );
Plotly.plot('divemg2', [{ y: newArray_emg2, mode: 'lines', line: {width: 5, color: 'pink'} }], custom_layout_emg_global, {staticPlot: true} );
Plotly.plot('divemg3', [{ y: newArray_emg3, mode: 'lines', line: {color: '#80CAF6'} }], custom_layout_emg_global, {staticPlot: true} );
Plotly.plot('divemg4', [{ y: newArray_emg4, mode: 'lines', line: {color: '#80CAF6'} }], custom_layout_emg_global, {staticPlot: true} );
Plotly.plot('divemg5', [{ y: newArray_emg5, mode: 'lines', line: {color: '#80CAF6'} }], custom_layout_emg_global, {staticPlot: true} );
Plotly.plot('divemg6', [{ y: newArray_emg6, mode: 'lines', line: {color: '#80CAF6'} }], custom_layout_emg_global, {staticPlot: true} );
Plotly.plot('divemg7', [{ y: newArray_emg7, mode: 'lines', line: {color: '#80CAF6'} }], custom_layout_emg_global, {staticPlot: true} );

//************************************************
// Socket to get data from the server
//************************************************

  var socket1 = io('http://169.254.1.1:7766/emg');

  socket1.on('connect', function(){console.log('connect!')});
  socket1.on('confirmation_connection', function(msg){console.log('Connected on:', msg)});
  socket1.on('disconnect', function(){console.log('disconnect!')});
  socket1.on('reply', function(msg){console.log('reply!', msg)});
  

  // Every time the server sends a "message", update all the EMG graphs
  socket1.on("message", function(data) {

    console.log(data, " for ", socket1.id);

    var y_emg0 = data[0]; // get the first row of the table
    newArray_emg0 = newArray_emg0.concat(y_emg0) // add it (270 values) to our main array 
    newArray_emg0.splice(0, emg_window_size_newdata) // remove as many cells (270) from the beginning of the array
  	var data_update_emg0 = { y: [newArray_emg0] }; // format the data to update the plot
  	Plotly.update('divemg0', data_update_emg0) // update the plot

    var y_emg1 = data[1];
    newArray_emg1 = newArray_emg1.concat(y_emg1)
    newArray_emg1.splice(0, emg_window_size_newdata)
  	var data_update_emg1 = { y: [newArray_emg1] };
  	Plotly.update('divemg1', data_update_emg1)

    var y_emg2 = data[2];
    newArray_emg2 = newArray_emg2.concat(y_emg2)
    newArray_emg2.splice(0, emg_window_size_newdata)
  	var data_update_emg2 = { y: [newArray_emg2] };
  	Plotly.update('divemg2', data_update_emg2)

    var y_emg3 = data[3];
    newArray_emg3 = newArray_emg3.concat(y_emg3)
    newArray_emg3.splice(0, emg_window_size_newdata)
  	var data_update_emg3 = { y: [newArray_emg3] };
  	Plotly.update('divemg3', data_update_emg3)

    var y_emg4 = data[4];
    newArray_emg4 = newArray_emg4.concat(y_emg4)
    newArray_emg4.splice(0, emg_window_size_newdata)
  	var data_update_emg4 = { y: [newArray_emg4] };
  	Plotly.update('divemg4', data_update_emg4)
  		
    var y_emg5 = data[5];
    newArray_emg5 = newArray_emg5.concat(y_emg5)
    newArray_emg5.splice(0, emg_window_size_newdata)
  	var data_update_emg5 = { y: [newArray_emg5] };
  	Plotly.update('divemg5', data_update_emg5)

    var y_emg6 = data[6];
    newArray_emg6 = newArray_emg6.concat(y_emg6)
    newArray_emg6.splice(0, emg_window_size_newdata)
  	var data_update_emg6 = { y: [newArray_emg6] };
  	Plotly.update('divemg6', data_update_emg6)

    var y_emg7 = data[7];
    newArray_emg7 = newArray_emg7.concat(y_emg7)
    newArray_emg7.splice(0, emg_window_size_newdata)
  	var data_update_emg7 = { y: [newArray_emg7] };
  	Plotly.update('divemg7', data_update_emg7)
	
  });

</script>

  </body>
</html>
