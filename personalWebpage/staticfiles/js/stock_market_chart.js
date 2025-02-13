document.addEventListener("DOMContentLoaded", function () {
    const mockData = [
        { date: "2024-02-01", value: 150 },
        { date: "2024-02-02", value: 155 },
        { date: "2024-02-03", value: 149 },
        { date: "2024-02-04", value: 160 },
        { date: "2024-02-05", value: 165 }
    ];

    plotGraph(mockData);
});

function plotGraph(data) {
    const width = 250;
    const height = 200;
    const margin = { top: 20, right: 10, bottom: 30, left: 30 };

    const svg = d3.select("#chart-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // **Title**
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", margin.top)
        .attr("text-anchor", "middle")
        .style("font-size", "14px")
        .style("font-weight", "bold")
        .text("Stock Prices Over Time");

    const x = d3.scaleTime()
        .domain(d3.extent(data, d => new Date(d.date)))
        .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
        .domain([d3.min(data, d => d.value) - 5, d3.max(data, d => d.value) + 5])
        .range([height - margin.bottom, margin.top]);

    const xAxis = d3.axisBottom(x).ticks(4).tickFormat(d3.timeFormat("%m-%d"));
    const yAxis = d3.axisLeft(y).ticks(5);

    svg.append("g")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(xAxis)
        .selectAll("text")
        .attr("transform", "rotate(-30)")
        .style("text-anchor", "end");

    svg.append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(yAxis);

    const line = d3.line()
        .x(d => x(new Date(d.date)))
        .y(d => y(d.value));

    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("d", line);

    // **Tooltip**
    const tooltip = d3.select("body") // Append to body for better positioning
        .append("div")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("background", "white")
        .style("border", "1px solid black")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style("font-size", "12px");

    // **Circles for Hovering Effect**
    svg.selectAll(".hover-dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => x(new Date(d.date)))
        .attr("cy", d => y(d.value))
        .attr("r", 5)
        .attr("fill", "transparent") // Initially invisible
        .attr("stroke", "red") // Outline only
        .attr("stroke-width", 2)
        .on("mouseover", function (event, d) {
            d3.select(this).attr("fill", "red"); // Highlight the dot
            tooltip.style("visibility", "visible")
                .text(`Date: ${d.date}, Value: ${d.value}`);
        })
        .on("mousemove", function (event) {
            tooltip.style("top", `${event.pageY - 10}px`)
                .style("left", `${event.pageX + 10}px`);
        })
        .on("mouseout", function () {
            d3.select(this).attr("fill", "transparent"); // Hide again
            tooltip.style("visibility", "hidden");
        });
}
