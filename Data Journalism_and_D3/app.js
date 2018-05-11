// Define SVG area dimensions
var svgWidth = 960;
var svgHeight = 500;

// Define the chart's margins as an object
var margin = {
  top: 60,
  right: 60,
  bottom: 60,
  left: 60 
};

// Define dimensions of the chart area
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Select body, append SVG area to it, and set its dimensions
var svg = d3.select("body")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append a group area, then set its margins
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

  // Append a div to the body to create tooltips, assign it a class
d3.select(".chart").append("div").attr("class", "tooltip").style("opacity", 0);

// Retrieve data from CSV file and execute everything below
d3.csv("data/data.csv", function(error, gradData) {
    if(error) throw error;
    gradData.forEach(function(data) {
      data.excellentHealth = +data.excellentHealth;
      data.bachDeg = +data.bachDeg;
  });

// Create scale functions
var yLinearScale = d3.scaleLinear()
  .domain([0, d3.max(gradData, d => d.bachDeg+5)])
  .range([height, 0]);

var xLinearScale = d3.scaleLinear()
  .domain([12, d3.max(gradData, d => d.excellentHealth+2)])
  .range([12, width]);

// Create axis functions
var bottomAxis = d3.axisBottom(xLinearScale);
var leftAxis = d3.axisLeft(yLinearScale);

// append circles to data points
var circles = chartGroup.selectAll("circle")
.data(gradData)
.enter()
.append("circle")
.attr("cx", (d, i) => xLinearScale(d.excellentHealth))
.attr("cy", d => yLinearScale(d.bachDeg))
.attr("r", "12")
.attr("fill", "skyblue")
.attr("opacity","0.9")

// append labels to circles
chartGroup.selectAll("text") 
  .data(gradData)
  .enter()
  .append("text")
    .style("text-anchor", "middle")
    .attr("font_family", "sans-serif")  // Font type
    .attr("font-size", "11px")  // Font size
    .attr("fill", "white")  // Font color
  .attr("x", (d, i) => xLinearScale(d.excellentHealth))
  .attr("y", d => yLinearScale(d.bachDeg))
  .text(function(d) {
    return d.stateAbb;
  });

// Append Axes to the chart
chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

chartGroup.append("g")
    .call(leftAxis);

// Initialize tool tip
var toolTip = d3.tip()
  .attr("class", "tooltip")
  .offset([80, -60])
  .html(d =>
    `${d.State}<br>Bachelor Degree: ${d.bachDeg}<br>Reported Excellent Health: ${d.excellentHealth}`
  );
// Create event listeners to display and hide the tooltip
circles.on("mouseover", function (data) {
   toolTip.show(data);
  })
  // onmouseout event
  .on("mouseout", function (data, index) {
    toolTip.hide(data);
  });

  // Create tooltip in the chart
chartGroup.call(toolTip);

  // Create axes labels
  // Y axis
  chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 40)
    .attr("x", 0 - (height / 2))
    .attr("class", "axisText")
    .text("Graduated with Bachelor Degree (%)");
  // X axis
  chartGroup.append("text")
    .attr(
      "transform",
      "translate(" + width / 2 + " ," + (height + margin.top + 30) + ")")
    .attr("class", "axisText")
    .text("Reported Excellent Health (%)");
});

// need to have x axis label to render
// need to get tooltip to stop strobbing
