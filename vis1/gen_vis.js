var container, canvas, context;
var camera, scene, raycaster, renderer;

var sphere_dict = {};
var object_dict = {};
var color_dict = {
    'gy': [new THREE.Color("rgb(10%, 100%, 10%)"), new THREE.Color("rgb(100%, 100%, 10%)")],
    'rb': [new THREE.Color("rgb(100%, 10%, 10%)"), new THREE.Color("rgb(10%, 10%, 100%)")]
};

var f_fnames = {
  't1': 'data/female_2012_2013.json',
  't2': 'data/female_2013_2014.json',
  't3': 'data/female_2014_2015.json',
  't4': 'data/female_2015_2016.json',
  't5': 'data/female_2016_2017.json'
};
var m_fnames = {
  't1': 'data/male_2012_2013.json',
  't2': 'data/male_2013_2014.json',
  't3': 'data/male_2014_2015.json',
  't4': 'data/male_2015_2016.json',
  't5': 'data/male_2016_2017.json'
};

var cur_id, cur_dtype, cur_time_slice;
var cur_color = 'rb';
var cur_scale = 0.001;
var cur_f_file = 'data/female.json';
var cur_m_file = 'data/male.json';

var select = document.getElementById("select");
var title = document.getElementById("title");
var ratio = document.getElementById("ratio");
var info = document.getElementById("info");
var select_time = document.getElementById("select_time");
var select_time_title = document.getElementById("select_time_title");

var mouse = new THREE.Vector2(), INTERSECTED;
var radius = 600, theta = 0;
var frustumSize = 1000;

init();
animate();

$(document).ready(function () {
  $('#select_color').change(function() {
      color_spheres();
  });
});

$(document).ready(function () {
  $('#select_ctype').change(function() {
      color_spheres();
  });
});

$(document).ready(function () {
  $('#select_data').change(function() {
    update_data();
  });
});

$(document).ready(function () {
  $('#select_time').change(function() {
    update_data();
  });
});

// Function that will update the data behind the scene according to the select boxes and update the scene
function update_data() {
  cur_dtype = $("#select_data option:selected").val();
  cur_time_slice = $("#select_time option:selected").val();
  if(cur_dtype == 'time'){
    select_time.style.display = 'inline';
    select_time_title.style.display = 'inline';
    cur_f_file = f_fnames[cur_time_slice];
    cur_m_file = m_fnames[cur_time_slice];
    cur_scale = 0.01;
  }
  else if (cur_dtype == 'all'){
    select_time.style.display = 'none';
    select_time_title.style.display = 'none';
    cur_f_file = 'data/female.json';
    cur_m_file = 'data/male.json';
    cur_scale = 0.001;
  }
  update_scene();
}

// Function that is called to format the coloring of the spheres
function color_spheres() {
  cur_color = $("#select_color option:selected").val();
  cur_ctype = $("#select_ctype option:selected").val();
  for( var key in object_dict ){
    var selectedObject = object_dict[key][0];
    if( cur_ctype == 'split'){
      if (object_dict[key][1] == 'm'){
        var material = new THREE.MeshLambertMaterial( {color: color_dict[cur_color][0]} );
      }
      else{
        var material = new THREE.MeshLambertMaterial( {color: color_dict[cur_color][1]} );
      }
    }
    else if ( cur_ctype == 'solid'){
      if(cur_color == 'rb'){
        var color = new THREE.Color("rgb(" + Math.round(object_dict[key][2]*100).toString() + "%, 10%, " + Math.round(object_dict[key][3]*100).toString() + "%)");
      }
      else if(cur_color == 'gy'){
        var color = new THREE.Color("rgb(" + (Math.round(object_dict[key][3]/2)*100).toString() + "%, " + Math.round((object_dict[key][2]/2 + object_dict[key][3]/2)*100).toString() + "%, 10%)");
      }
      var material = new THREE.MeshLambertMaterial( {color: color} );
    }
    else if ( cur_ctype == 'normal' ) {
      var tempr = Object.values( object_dict ).map(function ( k ) { return parseFloat( k[2] ); });
      var tempb = Object.values( object_dict ).map(function ( k ) { return parseFloat( k[3] ); });
      tempr = Object.values( tempr );
      tempb = Object.values( tempb );
      var arrr = filter_array( tempr );
      var arrb = filter_array( tempb );
      var minr = Math.min.apply(null, arrr);
      var maxr = Math.max.apply(null, arrr);
      var minb = Math.min.apply(null, arrb);
      var maxb = Math.max.apply(null, arrb);
      if(cur_color == 'rb'){
        var color = new THREE.Color("rgb(" + Math.round((object_dict[key][2]-minr)/(maxr-minr)*100).toString() + "%, 10%, " + Math.round((object_dict[key][3]-minb)/(maxb-minb)*100).toString() + "%)");
      }
      else if (cur_color == 'gy'){
        var color = new THREE.Color("rgb(" + (Math.round((object_dict[key][3]-minb)/(maxb-minb)*100)).toString() + "%, " + (Math.round(((object_dict[key][2]-minr)/(maxr-minr)/2 + (object_dict[key][3]-minb)/(maxb-minb)/2)*100)).toString() + "%, 10%)");
      }
      var material = new THREE.MeshLambertMaterial( {color: color} );
    }
    selectedObject.material = material;
  }
}

// Function used to remove NaNs from array
function filter_array(test_array) {
    var index = -1,
        arr_length = test_array ? test_array.length : 0,
        resIndex = -1,
        result = [];

    while (++index < arr_length) {
        var value = test_array[index];

        if (value) {
            result[++resIndex] = value;
        }
    }
    return result;
}

// Function used to load in the female json data
function loadJSONf(callback) {
   var xobj = new XMLHttpRequest();
       xobj.overrideMimeType("application/json");
   xobj.open('GET', cur_f_file, true);
   xobj.onreadystatechange = function () {
         if (xobj.readyState == 4 && xobj.status == "200") {
           // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
           callback(xobj.responseText);
         }
   };
   xobj.send(null);
}

// Function used to load in the male json data
function loadJSONm(callback) {
   var xobj = new XMLHttpRequest();
       xobj.overrideMimeType("application/json");
   xobj.open('GET', cur_m_file, true);
   xobj.onreadystatechange = function () {
         if (xobj.readyState == 4 && xobj.status == "200") {
           // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
           callback(xobj.responseText);
         }
   };

   xobj.send(null);
}

// Function used to generate a new scene to be added to the renderer
function update_scene() {
  object_dict = {}
  sphere_dict = {}
  scene = new THREE.Scene();
  scene.background = new THREE.Color( 0xf0f0f0 );

  var light = new THREE.DirectionalLight( 0xffffff, 1 );
  var light1 = new THREE.DirectionalLight( 0xffffff, 1 );
  light.position.set( 1, 1, 1 ).normalize();
  light1.position.set( -1, -1, -1 ).normalize();
  scene.add( light );
  scene.add( light1 );

  loadJSONf(function(response) {
      var female = JSON.parse(response);
      loadJSONm(function(response1) {
        var male = JSON.parse(response1);
        // Cycle through the keys in the loaded data and generate spheres for each
        var i = 1 / Object.keys(female).length;
        for (var key in female) {

          // Color is determined by ratio of male to female (male=red, female=blue)
          var red = parseInt(male[key]) / (parseInt(male[key])+parseInt(female[key]));
          var blue = parseInt(female[key]) / (parseInt(male[key])+parseInt(female[key]));

          // Size is determined by number of students, colored slice size is number of males and females
          var geometryr = new THREE.SphereGeometry( parseInt(female[key]) + parseInt(male[key]), 32, 32, phiStart=0, phiLength=2*Math.PI*red );
          var geometryb = new THREE.SphereGeometry( parseInt(female[key]) + parseInt(male[key]), 32, 32, 2*Math.PI*red, 2*Math.PI*blue );

          // Store a string to be displayed when this particular object is selected
          sphere_dict[geometryr.id] = "School Index: " + key.toString() + "<br />Number of Students: " + (parseInt(male[key])+parseInt(female[key])).toString() + "<br />Ratio (M/F): " + Math.round(parseInt(male[key]) / (parseInt(male[key])+parseInt(female[key])) * 100).toString() + "% / " + Math.round(parseInt(female[key]) / (parseInt(male[key])+parseInt(female[key])) * 100).toString() +"%";
          sphere_dict[geometryb.id] = "School Index: " + key.toString() + "<br />Number of Students: " + (parseInt(male[key])+parseInt(female[key])).toString() + "<br />Ratio (M/F): " + Math.round(parseInt(male[key]) / (parseInt(male[key])+parseInt(female[key])) * 100).toString() + "% / " + Math.round(parseInt(female[key]) / (parseInt(male[key])+parseInt(female[key])) * 100).toString() +"%";

          // Set the color of each of the proportioned slices
          var r_color = color_dict[cur_color][0];
          var b_color = color_dict[cur_color][1];

          // Create the object from the material and geometry
          var materialr = new THREE.MeshLambertMaterial( {color: r_color} );
          var materialb = new THREE.MeshLambertMaterial( {color: b_color} );
          var objectr = new THREE.Mesh( geometryr, materialr );
          var objectb = new THREE.Mesh( geometryb, materialb );

          // Randomly place the object and scale it down, use i to disperse semi equally
          objectr.position.x = i * 800 - 400;
          objectr.position.y = Math.random() * 800 - 400;
          objectr.position.z = Math.random() * 800 - 400;
          i += 1 / Object.keys(female).length;

          objectr.rotation.x = Math.random() * 2*Math.PI;
          objectr.rotation.y = Math.random() * 2*Math.PI;
          objectr.rotation.z = Math.random() * 2*Math.PI;

          objectr.scale.x = cur_scale;
          objectr.scale.y = cur_scale;
          objectr.scale.z = cur_scale;

          // Blue object the same as red object
          objectb.position.x = objectr.position.x;
          objectb.position.y = objectr.position.y;
          objectb.position.z = objectr.position.z;

          objectb.rotation.x = objectr.rotation.x;
          objectb.rotation.y = objectr.rotation.y;
          objectb.rotation.z = objectr.rotation.z;

          objectb.scale.x = objectr.scale.x;
          objectb.scale.y = objectr.scale.y;
          objectb.scale.z = objectr.scale.z;

          // Store into a dict so you can use position and scale again
          object_dict[objectr.id] = [objectr, 'm', red, blue];
          object_dict[objectb.id] = [objectb, 'f', red, blue];

          scene.add( objectr );
          scene.add( objectb );
        }
      });
  });
}

// Called to initialize an instance of the visualization
function init() {

  container = document.getElementById("container");

  // Bind 'm' to enter full screen mode
  THREEx.FullScreen.bindKey({ charCode : 'm'.charCodeAt(0) });

  var aspect = window.innerWidth / window.innerHeight;
  camera = new THREE.OrthographicCamera( frustumSize * aspect / - 2, frustumSize * aspect / 2, frustumSize / 2, frustumSize / - 2, 0, 1200 );

  update_scene();

  // Create a raycaster to identify intersected objects
  raycaster = new THREE.Raycaster();

  // Create renderer which generates a new canvas object and inserts into div container
  renderer = new THREE.WebGLRenderer();
  renderer.setPixelRatio( window.devicePixelRatio );
  renderer.setSize( window.innerWidth, window.innerHeight );
  canvas = container.appendChild(renderer.domElement);


  // Event listeners for highlighting a sphere and displaying info for a sphere
  document.addEventListener( 'mousemove', onDocumentMouseMove, false );
  document.addEventListener( 'mousedown', onDocumentMouseDown, false );
  window.addEventListener( 'resize', onWindowResize, false );

}

// This function adds a listener for the keyboard and does appropriate functions
document.addEventListener('keydown', (event) => {
  const keyName = event.key;
  if (keyName == 'm') {
    onWindowResize();
    console.log('hi');
  }
});

// This function reorients the generated visualization on window resize
function onWindowResize() {
  var aspect = window.innerWidth / window.innerHeight;
  camera.left   = - frustumSize * aspect / 2;
  camera.right  =   frustumSize * aspect / 2;
  camera.top    =   frustumSize / 2;
  camera.bottom = - frustumSize / 2;
  camera.updateProjectionMatrix();
  renderer.setPixelRatio( window.devicePixelRatio );
  renderer.setSize( window.innerWidth, window.innerHeight );
}

// This event highlights spheres when the mouse hovers over them
function onDocumentMouseMove( event ) {
  event.preventDefault();
  mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
  mouse.y = - ( event.clientY / (window.innerHeight+title.style.top) ) * 2 + 1;

}

// This event handler is for displaying the current sphere information in the ratio div
function onDocumentMouseDown( event ) {
  ratio.innerHTML = sphere_dict[cur_id];
}

// Function to animate the scene
function animate() {
  requestAnimationFrame( animate );
  render();
}

// Function that renders the scene, adjust ortho camera to spin about data
function render() {

  theta += 0.1;

  camera.position.x = radius * Math.sin( THREE.Math.degToRad( theta ) );
  camera.position.y = radius * Math.sin( THREE.Math.degToRad( theta ) );
  camera.position.z = radius * Math.cos( THREE.Math.degToRad( theta ) );
  camera.position.y = 0;
  camera.lookAt( scene.position );

  camera.updateMatrixWorld();

  // find intersections and set the geometry id of the selected object
  raycaster.setFromCamera( mouse, camera );1
  var intersects = raycaster.intersectObjects( scene.children );

  if ( intersects.length > 0 ) {
    if ( INTERSECTED != intersects[ 0 ].object ) {
      if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
      INTERSECTED = intersects[ 0 ].object;
      INTERSECTED.currentHex = INTERSECTED.material.emissive.getHex();
      INTERSECTED.material.emissive.setHex( 0xff0000 );
      if( INTERSECTED.geometry ){
        cur_id = INTERSECTED.geometry.id;
      }
    }
  } else {

    if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
    // remove previous intersection object reference
    //     by setting current intersection object to "nothing"
    INTERSECTED = null;
  }
  renderer.render( scene, camera );
}
