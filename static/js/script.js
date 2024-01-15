document.addEventListener("DOMContentLoaded", function () {
    //  cafe data (!TODO! replace this with real data from database)
    const cafes = [
        { name: "Cool Beans Cafe", location: "123 Main St", wifi: true, power: true },
        { name: "Brew Haven", location: "456 Oak St", wifi: true, power: false },
    ];

    const cafeListContainer = document.getElementById("cafe-list");

    cafes.forEach(cafe => {
        const cafeCard = document.createElement("div");
        cafeCard.classList.add("cafe-card");

        cafeCard.innerHTML = `
            <h2>${cafe.name}</h2>
            <p><strong>Location:</strong> ${cafe.location}</p>
            <p><strong>Wifi:</strong> ${cafe.wifi ? 'Yes' : 'No'}</p>
            <p><strong>Power:</strong> ${cafe.power ? 'Yes' : 'No'}</p>
            <a href="#">Details</a>
        `;

        cafeListContainer.appendChild(cafeCard);
    });
});
