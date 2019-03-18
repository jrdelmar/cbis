//https://vallandingham.me/bubble_charts_in_js.html
/* bubbleChart creation function. Returns a function that will
 * instantiate a new bubble chart given a DOM element to display
 * it in and a dataset to visualize.
 *
 * Organization and style inspired by:
 * https://bost.ocks.org/mike/chart/
 *
 */
//update by joanna to use in this code
function bubbleChart() {
  // Constants for sizing
  var width = 940;
  var height = 600;

  // tooltip for mouseover functionality
  var tooltip = floatingTooltip('gates_tooltip', 240);

  // Locations to move bubbles towards, depending
  // on which view mode is selected.
  var center = { x: width / 2, y: height / 2 };

  //var yearCenters = {
  var categoryCenters = {
    gun: { x: width / 3, y: height / 2 },
    not_gun: { x: width / 2, y: height / 2 }
  };

  // X locations of the year titles.
  var categoryTitleX = {
    gun: 160,
    not_gun: width / 2//,
    //2010: width - 160
  };

  // @v4 strength to apply to the position forces
  var forceStrength = 0.03;

  // These will be set in create_nodes and create_vis
  var svg = null;
  var bubbles = null;
  var nodes = [];

  // Charge function that is called for each node.
  // As part of the ManyBody force.
  // This is what creates the repulsion between nodes.
  //
  // Charge is proportional to the diameter of the
  // circle (which is stored in the radius attribute
  // of the circle's associated data.
  //
  // This is done to allow for accurate collision
  // detection with nodes of different sizes.
  //
  // Charge is negative because we want nodes to repel.
  // @v4 Before the charge was a stand-alone attribute
  //  of the force layout. Now we can use it as a separate force!
  function charge(d) {
    return -Math.pow(d.radius, 2.0) * forceStrength;
  }

  // Here we create a force layout and
  // @v4 We create a force simulation now and
  //  add forces to it.
  var simulation = d3.forceSimulation()
    .velocityDecay(0.2)
    .force('x', d3.forceX().strength(forceStrength).x(center.x))
    .force('y', d3.forceY().strength(forceStrength).y(center.y))
    .force('charge', d3.forceManyBody().strength(charge))
    .on('tick', ticked);

  // @v4 Force starts up automatically,
  //  which we don't want as there aren't any nodes yet.
  simulation.stop();

  // Nice looking colors - no reason to buck the trend
  // @v4 scales now have a flattened naming scheme
  var fillColor = d3.scaleOrdinal()
    //.domain(['low', 'medium', 'high'])
    .domain(['gun', 'not_gun', ''])
    .range(['#d84b2a', '#beccae', '#7aa25c']);

  /*
   * This data manipulation function takes the raw data from
   * the CSV file and converts it into an array of node objects.
   * Each node will store data and visualization values to visualize
   * a bubble.
   *
   * rawData is expected to be an array of data objects, read in from
   * one of d3's loading functions like d3.csv.
   *
   * This function returns the new node array, with a node in that
   * array for each element in the rawData input.
   */
  function createNodes(rawData) {
    // Use the max total_amount in the data as the max in the scale's domain
    // note we have to ensure the total_amount is a number.
    var maxAmount = d3.max(rawData, function (d) { return +d.value; });
    //edited: joanna 03052019
    // Sizes bubbles based on area.
    // @v4: new flattened scale names.
    /*var radiusScale = d3.scalePow()
      .exponent(0.5)
      .range([2, 85])
      .domain([0, maxAmount]);*/
    //manually adjust first
    //TODO: Adjust from the front end
    console.log("maxAmount=",maxAmount)
    var adj
    if (maxAmount < 100 ){
      adj = 2
    }else if (maxAmount > 100 && maxAmount <= 200 ){
      adj = 4
    } else if (maxAmount > 200 && maxAmount <= 300 ){
      adj = 5
    } else if (maxAmount > 300 && maxAmount <= 400 ){
      adj = 10
    } else if (maxAmount > 400 && maxAmount <= 500 ){
      adj = 20
    } else {
      adj = 50
    }

    var d_min = (maxAmount+10)*(-1)
    var d_max = (maxAmount+10)
    var r_min = d_min/adj
    var r_max = d_max/adj

    //var radiusScale = d3.scalePow().domain([-100,100]).range([-50,50]);
    //var radiusScale = d3.scalePow().exponent(0.4).domain([0,30]).range([1,30]);
    //var radiusScale = d3.scalePow().exponent(0.10).domain([0,maxAmount]).range([1,maxAmount+10]);
    //var radiusScale = d3.scalePow().domain([-400,400]).range([-100,100]);
    var radiusScale = d3.scalePow().domain([d_min,d_max]).range([r_min,r_max]);

    //adjust again for each results in index.html page
    if (maxAmount < 50){
      radiusScale = d3.scalePow().domain([-80,80]).range([-50,50]);
    }

    // Use map() to convert raw data into node data.
    // Checkout http://learnjsdata.com/ for more on
    // working with data.
    var myNodes = rawData.map(function (d) {
      return {
        //id: d.id,
        radius: radiusScale(+d.value),
        value: +d.value,
        name: d.label,
        label: d.label,
        category: d.category,
        x: Math.random() * 900,
        y: Math.random() * 800
      };
    });

    // sort them to prevent occlusion of smaller nodes.
    myNodes.sort(function (a, b) { return b.value - a.value; });

    return myNodes;
  }

  /*
   * Main entry point to the bubble chart. This function is returned
   * by the parent closure. It prepares the rawData for visualization
   * and adds an svg element to the provided selector and starts the
   * visualization creation process.
   *
   * selector is expected to be a DOM element or CSS selector that
   * points to the parent element of the bubble chart. Inside this
   * element, the code will add the SVG container for the visualization.
   *
   * rawData is expected to be an array of data objects as provided by
   * a d3 loading function like d3.csv.
   */
  var chart = function chart(selector, rawData) {
    // convert raw data into nodes data
    nodes = createNodes(rawData);

    // Create a SVG element inside the provided selector
    // with desired size.
    svg = d3.select(selector)
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    // Bind nodes data to what will become DOM elements to represent them.
    bubbles = svg.selectAll('.bubble')
      .data(nodes, function (d) { return d.label; });

    // Create new circle elements each with class `bubble`.
    // There will be one circle.bubble for each object in the nodes array.
    // Initially, their radius (r attribute) will be 0.
    // @v4 Selections are immutable, so lets capture the
    //  enter selection to apply our transtition to below.
    var bubblesE = bubbles.enter().append('circle')
      .classed('bubble', true)
      .attr('r', 0)
      .attr('fill', function (d) { return fillColor(d.category); })
      .attr('stroke', function (d) { return d3.rgb(fillColor(d.category)).darker(); })
      .attr('stroke-width', 2)
      .on('mouseover', showDetail)
      .on('mouseout', hideDetail);

    // @v4 Merge the original empty selection and the enter selection
    bubbles = bubbles.merge(bubblesE);

    // Fancy transition to make bubbles appear, ending with the
    // correct radius
    bubbles.transition()
      .duration(2000)
      .attr('r', function (d) { return d.radius; });

    // Set the simulation's nodes to our newly created nodes array.
    // @v4 Once we set the nodes, the simulation will start running automatically!
    simulation.nodes(nodes);

    // Set initial layout to single group.
    groupBubbles();
  };

  /*
   * Callback function that is called after every tick of the
   * force simulation.
   * Here we do the acutal repositioning of the SVG circles
   * based on the current x and y values of their bound node data.
   * These x and y values are modified by the force simulation.
   */
  function ticked() {
    bubbles
      .attr('cx', function (d) { return d.x; })
      .attr('cy', function (d) { return d.y; });
  }

  /*
   * Provides a x value for each node to be used with the split by year
   * x force.
   */
  function nodeCategoryPos(d) {
    return categoryCenters[d.category].x;
  }


  /*
   * Sets visualization in "single group mode".
   * The year labels are hidden and the force layout
   * tick function is set to move all nodes to the
   * center of the visualization.
   */
  function groupBubbles() {
    hideCategoryTitles();

    // @v4 Reset the 'x' force to draw the bubbles to the center.
    simulation.force('x', d3.forceX().strength(forceStrength).x(center.x));

    // @v4 We can reset the alpha value and restart the simulation
    simulation.alpha(1).restart();
  }


  /*
   * Sets visualization in "split by year mode".
   * The year labels are shown and the force layout
   * tick function is set to move nodes to the
   * yearCenter of their data's year.
   */
  function splitBubbles() {
    showCategoryTitles();

    // @v4 Reset the 'x' force to draw the bubbles to their year centers
    simulation.force('x', d3.forceX().strength(forceStrength).x(nodeCategoryPos));

    // @v4 We can reset the alpha value and restart the simulation
    simulation.alpha(1).restart();
  }

  /*
   * Hides Year title displays.
   */
  function hideCategoryTitles() {
    svg.selectAll('.category').remove();
  }

  /*
   * Shows Year title displays.
   */
  function showCategoryTitles() {
    // Another way to do this would be to create
    // the year texts once and then just hide them.
    var categoryData = d3.keys(categoryTitleX);
    var category = svg.selectAll('.category')
      .data(categoryData);

    category.enter().append('text')
      .attr('class', 'category')
      .attr('x', function (d) { return categoryTitleX[d]; })
      .attr('y', 40)
      .attr('text-anchor', 'middle')
      .text(function (d) { return d; });
  }


  /*
   * Function called on mouseover to display the
   * details of a bubble in the tooltip.
   */
  function showDetail(d) {
    // change outline to indicate hover state.
    d3.select(this).attr('stroke', 'black');

    var content = '<span class="name">Label: </span><span class="value">' +
                  d.label +
                  '</span><br/>' +
                  '<span class="name">Count: </span><span class="value">' +
                  addCommas(d.value) +
                  '</span>';

    tooltip.showTooltip(content, d3.event);
  }

  /*
   * Hides tooltip
   */
  function hideDetail(d) {
    // reset outline
    d3.select(this)
      .attr('stroke', d3.rgb(fillColor(d.category)).darker());

    tooltip.hideTooltip();
  }

  /*
   * Externally accessible function (this is attached to the
   * returned chart function). Allows the visualization to toggle
   * between "single group" and "split by year" modes.
   *
   * displayName is expected to be a string and either 'year' or 'all'.
   */
  chart.toggleDisplay = function (displayName) {
    if (displayName === 'category') {
      splitBubbles();
    } else {
      groupBubbles();
    }
  };

  var params = "";
  chart.params = function(value) {
    if (!arguments.length) { return params; }
    params = value;

    return chart;
  }

  var dataset = undefined;
  chart.dataset = function(value) {
    if (!arguments.length) { return dataset; }
    dataset = value;

    return chart;
  }


  // return the chart function from closure.
  return chart;

} //--end of bubble chart function

/*
 * Below is the initialization code as well as some helper functions
 * to create a new bubble chart instance, load the data, and display it.
 */

//var myBubbleChart = bubbleChart();

/*
 * Function called once data is loaded from CSV.
 * Calls bubble chart function to display inside #vis div.
 */
/*function display(error, data) {
  if (error) {
    console.log(error);
  }

  myBubbleChart('#vis', data);
}*/


/*
 * Helper function to convert a number into a string
 * and add commas to it to improve presentation.
 */
function addCommas(nStr) {
  nStr += '';
  var x = nStr.split('.');
  var x1 = x[0];
  var x2 = x.length > 1 ? '.' + x[1] : '';
  var rgx = /(\d+)(\d{3})/;
  while (rgx.test(x1)) {
    x1 = x1.replace(rgx, '$1' + ',' + '$2');
  }

  return x1 + x2;
}
