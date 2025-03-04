// Graph setup without data

const container = document.getElementById("metrics-chart");
const width = container.clientWidth;
const height = container.clientHeight;

const margin = { top: 30, right: 10, bottom: 30, left: 40 };

// Select the container and append an SVG once
const svg = d3.select("#metrics-chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// **Title**
svg.append("text")
    .attr("x", width / 2)
    .attr("y", margin.top - 20)
    .attr("text-anchor", "middle")
    .style("font-size", "14px")
    .style("font-weight", "bold")
    .text("Hardware Metrics Chart");

// y-label
svg.append("text")
    .attr("x", -10)
    .attr("y", 125)
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")  // Rotate to vertical
    .style("font-size", "12px")
    .text("%");

// Define scales (but leave the domain empty for now)
const y = d3.scaleLinear().domain([0, 100]).range([height - margin.bottom, margin.top]);
const x = d3.scaleTime().range([margin.left, width - margin.right]);

// Update the X-axis domain dynamically
function updateXAxis() {
    const now = new Date();
    const oneHourAgo = new Date(now - 60 * 60 * 1000);  // One hour ago

    x.domain([oneHourAgo, now]);  // Set domain from 60 minutes ago to now
}


// Append axes (will be updated dynamically)
const xAxisGroup = svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`);

const yAxisGroup = svg.append("g")
    .attr("transform", `translate(${margin.left},0)`);



// Define line generators
const cpuLine = d3.line().x(d => x(new Date(d.timestamp))).y(d => y(d.cpu_usage));
const ramLine = d3.line().x(d => x(new Date(d.timestamp))).y(d => y(d.ram_usage));

// Append empty paths for CPU and RAM lines
const cpuPath = svg.append("path")
    .attr("class", "cpu-line")
    .attr("fill", "none")
    .attr("stroke", "blue")
    .attr("stroke-width", 2);

const ramPath = svg.append("path")
    .attr("class", "ram-line")
    .attr("fill", "none")
    .attr("stroke", "green")
    .attr("stroke-width", 2);

// **Legend** for CPU and RAM
const legend = svg.append("g")
    .attr("transform", `translate(${width - margin.right - 10}, ${margin.top})`);

legend.append("rect")
    .attr("width", 10)
    .attr("height", 10)
    .attr("fill", "blue");

legend.append("text")
    .attr("x", 15)
    .attr("y", 10)
    .style("font-size", "12px")
    .text("CPU");

legend.append("rect")
    .attr("y", 20)
    .attr("width", 10)
    .attr("height", 10)
    .attr("fill", "green");

legend.append("text")
    .attr("x", 15)
    .attr("y", 30)
    .style("font-size", "12px")
    .text("RAM");

// Websocket setup

// Determine if we're in production or development
const isProduction = window.location.hostname !== "localhost";

// Use the correct WebSocket URL based on the environment
const websocketUrl = isProduction
    ? "wss://" + window.location.hostname + "/ws/metrics/"
    : "ws://localhost:8000/ws/metrics/";

const socket = new WebSocket(websocketUrl);

socket.onopen = function(event) {
    console.log("WebSocket connection opened!");
};

socket.onmessage = function(event) {
    const message = JSON.parse(event.data); // Parse the received message
    console.log("Received Message:", message); // Debugging
    plotData(message)
};

socket.onclose = function(event) {
    console.log("WebSocket closed", event);
};

let liveData = [];  // Store live data for real-time updates

function plotData(data) {
    console.log("Plotting data:", data); // Debugging

    if (Array.isArray(data.data)) {
        liveData = data.data;
    } else {
        liveData.push(data);
    }

    updateChart();
}

function updateChart() {
    if (liveData.length === 0) return;  // Do nothing if no data

    console.log("Live Data:", liveData);  // Debugging step

    // Update the X-axis domain to always show the last hour of data
    updateXAxis();

    // Update the Y axis domain (fixed from 0 to 100)
    y.domain([0, 100]);

    // Update the axes
    xAxisGroup.call(d3.axisBottom(x).ticks(5));  // Update X axis
    yAxisGroup.call(d3.axisLeft(y));  // Update Y axis

    // Update the CPU line path
    cpuPath.datum(liveData)
        .attr("d", cpuLine)  // Create a line for CPU usage
        .attr("fill", "none")
        .attr("stroke", "blue")
        .attr("stroke-width", 2);

    // Update the RAM line path
    ramPath.datum(liveData)
        .attr("d", ramLine)  // Create a line for RAM usage
        .attr("fill", "none")
        .attr("stroke", "green")
        .attr("stroke-width", 2);
}
