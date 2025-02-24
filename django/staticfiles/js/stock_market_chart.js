document.addEventListener("DOMContentLoaded", function () {
    // URL of your Django REST API endpoint (change if necessary)
    const apiUrl = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/airflow/api/stock_prices/' 
    : 'https://jkirstein.dk/airflow/api/stock_prices/';
    
    // Fetch the data from the API
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Process the data into a format that D3 can use
            const formattedData = data.map(d => ({
                date: d.date, // Ensure the date format is compatible
                value: parseFloat(d.closing_price) // Convert the close price to a number
            }));

            // Pass the formatted data to plotGraph
            plotGraph(formattedData);
        })
        .catch(error => {
            console.error('Error fetching stock prices:', error);
        });
});

function plotGraph(data) {
    const width = 250;
    const height = 250;
    const margin = { top: 30, right: 10, bottom: 30, left: 40 };

    const svg = d3.select("#chart-container")
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
        .text("Stock prices");

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
        .attr("stroke", "#062b55")
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
        .attr("r", 4)
        .attr("fill", "transparent") // Initially invisible
        .attr("stroke", "black") // Outline only
        .attr("stroke-width", 2)
        .on("mouseover", function (event, d) {
            d3.select(this).attr("fill", "black"); // Highlight the dot
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
