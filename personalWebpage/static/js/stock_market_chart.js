document.addEventListener("DOMContentLoaded", function () {
    // Mock data: array of objects with date and stock_price
    const data = [
        { date: "2024-02-01", stock_price: 150 },
        { date: "2024-02-02", stock_price: 155 },
        { date: "2024-02-03", stock_price: 149 },
        { date: "2024-02-04", stock_price: 160 },
        { date: "2024-02-05", stock_price: 162 },
        { date: "2024-02-06", stock_price: 158 }
    ];

    // Set up dimensions
    const margin = { top: 20, right: 30, bottom: 30, left: 50 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Parse date format
    const parseDate = d3.timeParse("%Y-%m-%d");
    data.forEach(d => d.date = parseDate(d.date));

    // Create scales
    const x = d3.scaleTime()
        .domain(d3.extent(data, d => d.date))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([d3.min(data, d => d.stock_price) - 5, d3.max(data, d => d.stock_price) + 5])
        .range([height, 0]);

    // Create SVG container
    const svg = d3.select("#chart-container")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Create X and Y axes
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .call(d3.axisLeft(y));

    // Create line generator
    const line = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.stock_price))
        .curve(d3.curveMonotoneX); // Smooth curve

    // Draw line
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("d", line);

    // Add data points
    svg.selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => x(d.date))
        .attr("cy", d => y(d.stock_price))
        .attr("r", 4)
        .attr("fill", "steelblue");
});