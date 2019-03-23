/*
This file uses d3 version 3. There is no time to rewrite to version 4.
Since this project uses version 4 for the bubble graph, the library heatmap/d3.v3.js has been changed to d3v3 variable.

Inspired from:
http://bl.ocks.org/tjdecke/5558084
http://bl.ocks.org/ianyfchang/8119685
https://bl.ocks.org/Bl3f/cdb5ad854b376765fa99
*/
function v3heatmap(rawData, selector) {
    var itemSize = 22, cellSize = itemSize - 1
    var width = 940, height = 300;

    var margin = {top: 50, right: 0, bottom: 0, left: 110},
        colors = ["#ffffd9", "#edf8b1", "#c7e9b4", "#7fcdbb", "#41b6c4", "#1d91c0", "#225ea8", "#253494", "#081d58"] // alternatively colorbrewer.YlGnBu[9]

        var data = rawData.map(function (item) {
            return {
                folder: item.x,
                extension: item.y,
                value: item.value
            };
        });

        var x_elements = d3v3.set(data.map(function (item) {
                return item.extension;
            })).values(),
            y_elements = d3v3.set(data.map(function (item) {
                return item.folder;
            })).values();

        var xScale = d3v3.scale.ordinal()
            .domain(x_elements)
            .rangeBands([0, x_elements.length * itemSize]);

        var xAxis = d3v3.svg.axis()
            .scale(xScale)
            .tickFormat(function (d) {
                return d;
            })
            .orient("top");

        var yScale = d3v3.scale.ordinal()
            .domain(y_elements)
            .rangeBands([0, y_elements.length * itemSize]);

        var yAxis = d3v3.svg.axis()
            .scale(yScale)
            .tickFormat(function (d) {
                return d;
            })
            .orient("left");

        var colorScale = d3v3.scale.quantile()
            .domain([0, 9, d3v3.max(data, function (d) {
                return d.value;
            })])
            .range(colors);

        var svg = d3v3.select(selector)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var cells = svg.selectAll('rect')
            .data(data)
            .enter().append('g').append('rect')
            .attr('class', 'cell')
            .attr('width', cellSize)
            .attr('height', cellSize)
            .attr('y', function (d) {
                return yScale(d.folder);
            })
            .attr('x', function (d) {
                return xScale(d.extension);
            })
            .attr('fill', function (d) {
                return colorScale(d.value);
            })
            .on("mouseover", function (d) {
                //highlight text
                d3v3.select(this).classed("cell-hover", true);
                d3v3.selectAll(".rowLabel").classed("text-highlight", function (r, ri) {
                    return ri == (d.row - 1);
                });
                d3v3.selectAll(".colLabel").classed("text-highlight", function (c, ci) {
                    return ci == (d.col - 1);
                });

                //Update the tooltip position and value
                d3v3.select("#tooltip")
                    .style("left", (d3v3.event.pageX + 10) + "px")
                    .style("top", (d3v3.event.pageY - 10) + "px")
                    .select("#value")
                    .text("Folder:" + d.folder + "\nExtension:" + d.extension + "\nCount:" + d.value)
                //Show the tooltip
                d3v3.select("#tooltip").classed("hidden", false);
            })
            .on("mouseout", function () {
                d3v3.select(this).classed("cell-hover", false);
                d3v3.selectAll(".rowLabel").classed("text-highlight", false);
                d3v3.selectAll(".colLabel").classed("text-highlight", false);
                d3v3.select("#tooltip").classed("hidden", true);
            });

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .selectAll('text')
            .style("text-anchor", "end")
            //.attr("transform", "translate(-6," + cellSize / 1.5 + ")")
            .attr("class", function (d, i) {
                return "rowLabel mono r" + i;
            })
            .on("mouseover", function (d) {
                d3v3.select(this).classed("text-hover", true);
            })
            .on("mouseout", function (d) {
                d3v3.select(this).classed("text-hover", false);
            })
        ;

        svg.append("g")
            .attr("class", "x axis")
            .call(xAxis)
            .selectAll('text')
            .attr('font-weight', 'normal')
            .style("text-anchor", "start")
            .attr("dx", ".8em")
            .attr("dy", ".5em")
            .attr("transform", function (d) {
                return "rotate(-65)";
            })
            .style("text-anchor", "left")
            //.attr("transform", "translate("+cellSize/2 + ",-6) rotate (-90)")
            .attr("class", function (d, i) {
                return "colLabel mono c" + i;
            })
            .on("mouseover", function (d) {
                d3v3.select(this).classed("text-hover", true);
            })
            .on("mouseout", function (d) {
                d3v3.select(this).classed("text-hover", false);
            });


}//v3heatmap