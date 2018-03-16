var w = 300,                        //width
h = 300,                            //height
r = 100,                            //radius
color = d3.scaleOrdinal(d3.schemeCategory20c);     //builtin range of color

data = [{"label":"one", "value":20}, 
		{"label":"two", "value":50}, 
		{"label":"three", "value":30}];
console.log(data)

var data_file = "data/plots_total_data.csv"

	var svg1 = d3.select("svg"),
		width = +svg1.attr("width"),
		height = +svg1.attr("height"),
		radius = Math.min(width, height) / 2,
		g = svg1.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

	var color = d3.scaleOrdinal(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

	var pie = d3.pie()
		.sort(null)
		.value(function(d) { return d.value; });

	var path = d3.arc()
		.outerRadius(radius - 10)
		.innerRadius(0);

	var label = d3.arc()
		.outerRadius(radius - 40)
		.innerRadius(radius - 40);

	d3.csv(data_file, function(d) {
	  d.population = +d.population;
	  return d;
	}, function(error, data) {
	  if (error) throw error;
	  console.log(data)

	  var arc = g.selectAll(".arc")
		.data(pie(data))
		.enter().append("g")
		  .attr("class", "arc")
		 	.on("mouseover", function(d,i) {
			arc.append("text")
			.attr("dy", ".5em")
			.style("fill", function(d,i){return "black";})
		  	.text(d.data.label);
		 })
		 .on("mouseout", function(d) {
		 	arc.select("text").remove();
		});

	  arc.append("path")
		  .attr("d", path)
		  .attr("fill", function(d) { return color(d.data.label); });

	  /*arc.append("text")
		  .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
		  .attr("dy", "0.35em")
		  .text(function(d) { return d.data.label; });*/
	});
