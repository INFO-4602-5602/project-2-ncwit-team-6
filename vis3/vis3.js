// Javascript source code for Vis 3, INFO project #2
// 3/16/18

// dimensions of graph
var margin = {top: 40, right: 20, bottom: 30, left: 50};
var width = d3.min([window.innerWidth - 25, 960]);
var height = 500;

var activeData;
var activeScale;

var vis3Data;
d3.csv("filtered-v3-data.csv", function(error, data) {
    if (error) throw error;
    //data.sort(function(a,b) {
    //    return +a[data.columns[0]] - +b[data.columns[0]];
    //});
    vis3Data = data;
    makeDropMenu(data, data.columns[0], data.columns[1]);
    //makePlot(data, data.columns[0], data.columns[1]);
})

// create dropdown with menu options for plot
function makeDropMenu(data, col1, col2) {
    menu = document.getElementById("v3form").elements["inst"];
    console.log(menu);
    //for(var i = 0; i < menu.options.length; i++)

            //.data(d3.map(data, function(d) {return d.col;}).keys())
    d3.select(menu).selectAll(null)
        .data(data)
        .enter()
        .append("option")
        .text(function(d) {return d[col1] + ', ' + d[col2];})
        .attr("value", function(d) {return d[col1] + ',' + d[col2];});
    // read all the institutions in
    // sort the institutions

    // attach event to dropdown menu
    d3.select(menu).on("change", function() {handleMenuClick()});

    // add svg canvas to page
    d3.select("#scatterplot").append("svg")
}

function handleMenuClick() {
    menu = document.getElementById("v3form").elements["inst"];
    value = menu.options[menu.selectedIndex].value
    console.log(value)
    res = value.split(",")
    inst = res[0]
    year = res[1]
    makePlot(vis3Data, inst, year)
}

function setPlotSize(x_in, y1, y2, factor) {
    // linear mapping btw data and pixel space***********
    var abs_margin = 5
    var data_width = (width/factor) - abs_margin - 
                     margin.left - 
                     margin.right;
    var data_height = (height / factor) - abs_margin - 
                     //scaled_margin.top - scaled_margin.bottom;
                      margin.top- 
                      margin.bottom;
    var x = d3.scaleLinear()
    var y = d3.scaleLinear()
    // Scale the dom/range of the data: pull out min/max
    x.domain(d3.extent(x_in, function(d) {return d;}));
    y.domain([0, d3.max(y1.concat(y2), function(d) {return d;})]);
    x.range([0, data_width]);
    y.range([data_height, 0]);
    scale = {x:x, y:y, 
             margin:margin,//margin:scaled_margin,
             width:data_width, 
             height:data_height,
             svg_width:(width/factor) - abs_margin,
             svg_height:(height/factor) - abs_margin};
    return scale
}

function plotGenderData(gender, x, y_data, scale, svg) {
    if(gender == "Female") {
        fill = "red";
    } else {
        fill = "blue";
    }

    // add the line connecting the points
    var line = d3.line()
        .x(function(d) {return scale.x(d);})
        .y(function(d) {return scale.y(y_data[d]);})
    svg.append("path")
        .datum(x)
        .attr("d", line)
        .style("fill", "none")
        .style("stroke", fill)
        .style("stroke-width", "2px");

    // Add the scatterplot points
    svg.selectAll("circle." + gender)
      .data(x) // bind data
      .enter() // enter data so we can use it
      .append("circle")
      .attr("class", gender)
      .attr("r", 7)
      .attr("cx", function(d) {return scale.x(d);})
      .attr("cy", function(d) {return scale.y(y_data[d])})
      .attr("fill", fill)
      .on("mouseover", handleScatterDotMouseoverEvent)
      .on("mouseout", handleScatterDotMouseoutEvent)
}

function makePlot(data, inst, year) {
    // transform the data
    console.log(data)
    m_cols = ["Male Freshmen", "Male Sophomores", "Male Juniors",	"Male Seniors"]
    f_cols = ["Female Freshmen", "Female Sophomores", "Female Juniors", "Female Seniors"]
    m_data = []
    f_data = []
    x = [] // years
    // find the row we want
    for(var i = 0; i < data.length; i++) {
        if ((data[i]["Institution"] == inst) && (data[i]["Class Year Start"] == year)) {
            // found the row
            for(var j = 0; j < m_cols.length; j++) {
                m_data.push(+data[i][m_cols[j]]);
                f_data.push(+data[i][f_cols[j]]);
                x.push(j)
            }
            break;
        }
    }

    scale = setPlotSize(x, m_data, f_data, 1);
    activeData = [x, m_data, f_data];
    activeScale = scale;

    // update the title text
    gradClass = +year + 4;
    title = d3.select("#plotContainer h3");
    title.text("CS-student Retention in Institution " + inst + ", for Graduating Class of " + gradClass);

    // svg tag to document
    canvas = d3.selectAll("#scatterplot svg g").remove();
    var svg = d3.select("#scatterplot svg")
                .attr("width", scale.svg_width)
                .attr("height", scale.svg_height)
                .append("g")
                .attr("transform", "translate(" + 
                    scale.margin.left + "," + 
                    scale.margin.top + ")");
    plotGenderData("Female", x, f_data, scale, svg);
    plotGenderData("Male", x, m_data, scale, svg);

    // Add the X Axis
    svg.append("g")
      .attr("transform", "translate(0, " + scale.height + ")")
      .call(d3.axisBottom(scale.x).ticks(x.length));

    // Add the Y Axis
    svg.append("g")
      .call(d3.axisLeft(scale.y));

    // add the text labels
    svg.append("text")
      .attr("class", "label")
      .text("Year, for freshman start in " + year)
      .attr("x", scale.width - 250)
      .attr("y", scale.height - 10);
    svg.append("text")
      .attr("class", "label")
      .text("Number of Students")
      .attr("y", -10);
}

function handleScatterDotMouseoverEvent(d, i) {
    // change color on mouseover
    d3.select(this).attr("fill", "black");
    gender = d3.select(this).attr("class");
    if(gender == "Male") {
        num = activeData[1][d];
    } else {
        num = activeData[2][d];
    }
    d3.select("body #tooltip")
      .style("opacity", 0.9)
      .style("left", (d3.event.pageX + 5) + "px")
      .style("top", (d3.event.pageY + 5) + "px");
    d3.select("body #tooltip p")
      .text("Gender: " + gender + ", \nYear: " + d + ",\nStudents: " + num);
}

function handleScatterDotMouseoutEvent() {
    // change color back on mouseout
    gender = d3.select(this).attr("class");
    if(gender == "Male") {
        fill = "blue";
    } else {
        fill = "red";
    }
    d3.select(this).attr("fill", fill);
    // bell 1: tooltip disappear
    d3.select("body #tooltip")
      .style("opacity", 0)
      .style("left", "0px")
      .style("top", "0px");
}

