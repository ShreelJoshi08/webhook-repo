// This function fetches the latest events from the backend
// and updates the UI accordingly.
function fetchEvents() {

    // Send GET request to the /events endpoint
    fetch("/events")
        .then(response => response.json())
        .then(data => {

            // Select the container where events will be displayed
            const container = document.getElementById("events");

            // Clear previous events before rendering updated list
            container.innerHTML = "";

            // Loop through each event received from backend
            data.forEach(event => {

                let message = "";

                // Format message for Push event
                if (event.action === "push") {
                    message = `${event.author} pushed to ${event.to_branch} on ${event.timestamp}`;
                }

                // Format message for Pull Request event
                else if (event.action === "pull_request") {
                    message = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
                }

                // Format message for Merge event
                else if (event.action === "merge") {
                    message = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
                }

                // Create paragraph element for each event
                const p = document.createElement("p");

                // Set formatted message as text
                p.innerText = message;

                // Append event to UI container
                container.appendChild(p);
            });
        })
        .catch(err => {
            // Log any fetch errors (optional safety)
            console.error("Fetch error:", err);
        });
}

// Initial call to load events when page loads
fetchEvents();

// Poll backend every 10 sec to fetch latest updates
setInterval(fetchEvents, 10000);