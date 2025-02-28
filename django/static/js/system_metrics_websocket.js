const socket = new WebSocket("ws://localhost:8000/ws/metrics/");

socket.onopen = function(event) {
    console.log("WebSocket connection opened!");
    socket.send(JSON.stringify({ message: "Hello from client!" }));
};

socket.onmessage = function(event) {
    const message = JSON.parse(event.data);

    if (message.type === "history") {
        console.log("Historical Data:", message.data);
        plotHistoricalData(message.data); // Function to plot existing data
    } else if (message.type === "realtime") {
        console.log("New Data:", message.data);
        updateLiveChart(message.data); // Function to update chart in real-time
    }
};

socket.onclose = function(event) {
    console.log("WebSocket closed", event);
};

function plotHistoricalData(data) {
    // Plot historical data (CPU and RAM usage)
    const width = 600;
    const height = 300;
    const margin = { top: 30, right: 10, bottom: 30, left: 40 };

    const svg = d3.select("#metrics-chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // Title
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", margin.top - 20)
        .attr("text-anchor", "middle")
        .style("font-size", "14px")
        .style("font-weight", "bold")
        .text("System Metrics (CPU & RAM)");

    const x = d3.scaleTime()
        .domain(d3.extent(data, d => new Date(d.timestamp)))
        .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
        .domain([0, 100])  // Assuming metrics are percentage values
        .range([height - margin.bottom, margin.top]);

    const xAxis = d3.axisBottom(x).ticks(4).tickFormat(d3.timeFormat("%H:%M"));
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

    // CPU Line
    const cpuLine = d3.line()
        .x(d => x(new Date(d.timestamp)))
        .y(d => y(d.cpu_usage));

    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr("d", cpuLine);

    // RAM Line
    const ramLine = d3.line()
        .x(d => x(new Date(d.timestamp)))
        .y(d => y(d.ram_usage));

    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "green")
        .attr("stroke-width", 2)
        .attr("d", ramLine);

    // Tooltip
    const tooltip = d3.select("body")
        .append("div")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("background", "white")
        .style("border", "1px solid black")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style("font-size", "12px");

    // Circles for Hovering Effect (CPU and RAM)
    svg.selectAll(".hover-dot-cpu")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => x(new Date(d.timestamp)))
        .attr("cy", d => y(d.cpu_usage))
        .attr("r", 4)
        .attr("fill", "transparent")
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .on("mouseover", function (event, d) {
            d3.select(this).attr("fill", "blue");
            tooltip.style("visibility", "visible")
                .text(`Time: ${d.timestamp}, CPU: ${d.cpu_usage}%`);
        })
        .on("mousemove", function (event) {
            tooltip.style("top", `${event.pageY - 10}px`)
                .style("left", `${event.pageX + 10}px`);
        })
        .on("mouseout", function () {
            d3.select(this).attr("fill", "transparent");
            tooltip.style("visibility", "hidden");
        });

    svg.selectAll(".hover-dot-ram")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => x(new Date(d.timestamp)))
        .attr("cy", d => y(d.ram_usage))
        .attr("r", 4)
        .attr("fill", "transparent")
        .attr("stroke", "green")
        .attr("stroke-width", 2)
        .on("mouseover", function (event, d) {
            d3.select(this).attr("fill", "green");
            tooltip.style("visibility", "visible")
                .text(`Time: ${d.timestamp}, RAM: ${d.ram_usage}%`);
        })
        .on("mousemove", function (event) {
            tooltip.style("top", `${event.pageY - 10}px`)
                .style("left", `${event.pageX + 10}px`);
        })
        .on("mouseout", function () {
            d3.select(this).attr("fill", "transparent");
            tooltip.style("visibility", "hidden");
        });
}

// Function to update live chart with real-time data
function updateLiveChart(data) {
    const svg = d3.select("#metrics-chart").select("svg");

    // Update the existing lines for CPU and RAM
    const x = d3.scaleTime()
        .domain([d3.min(data, d => new Date(d.timestamp)), d3.max(data, d => new Date(d.timestamp))])
        .range([40, 600]);

    const y = d3.scaleLinear()
        .domain([0, 100])  // Assuming metrics are percentage values
        .range([300, 30]);

    const cpuLine = d3.line()
        .x(d => x(new Date(d.timestamp)))
        .y(d => y(d.cpu_usage));

    const ramLine = d3.line()
        .x(d => x(new Date(d.timestamp)))
        .y(d => y(d.ram_usage));

    // Rebind the data to the lines
    svg.selectAll("path").data([data]);

    // Update CPU line
    svg.selectAll("path")
        .data([data])
        .transition()
        .duration(500)
        .attr("d", cpuLine)
        .attr("stroke", "blue");

    // Update RAM line
    svg.selectAll("path")
        .data([data])
        .transition()
        .duration(500)
        .attr("d", ramLine)
        .attr("stroke", "green");
}
