document.addEventListener("DOMContentLoaded", function() {
    const enterButton = document.querySelector(".enter-button");
    const clearButton = document.querySelector(".clear-table");
    const exportButton = document.querySelector(".export-to-excel");

    // After button press search for item using the scrapper
    enterButton.addEventListener("click", function() {
        const productId = document.getElementById("product-id").value;
        fetch(`/search/${productId}`)
            .then(response => response.json())
            .then(data => {
                updateTable(data);
            })
            .catch(error => console.error('Error:', error));
    });

    // Clear the table of all the data
    clearButton.addEventListener("click", function() {
        clearTable();
    });

    // Generate excel with all the data that is in the table
    exportButton.addEventListener("click", function() {
        const table = document.getElementById("product-table");
        const wb = XLSX.utils.table_to_book(table, {sheet: "Sheet 1"});
        XLSX.writeFile(wb, "product_details.xlsx");
    });

    const updateTable = (data) => {
        // Update table with new data
        const tableBody = document.getElementById("table-body");
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>${data.denumire}</td>
            <td>${data.pret}</td>
            <td>${data.disponibilitate}</td>
            <td>${data.producator}</td>
        `;
        tableBody.appendChild(newRow);
    }

    const clearTable = () => {
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = ''; // Clear all rows from table body
    }
});
