document.addEventListener("DOMContentLoaded", function () {
    let birthdayInput = document.getElementById("birthday");

    // Set default date to prevent invalid input
    birthdayInput.value = "2010-01-01";

    // Ensure the date is within the allowed range (2004-2030)
    birthdayInput.addEventListener("change", function () {
        let selectedDate = new Date(birthdayInput.value);
        let minDate = new Date("2004-01-01");
        let maxDate = new Date("2030-12-31");

        if (selectedDate < minDate || selectedDate > maxDate) {
            alert("Please select a date between 2004 and 2030.");
            birthdayInput.value = "2010-01-01"; // Reset to a default valid date
        }
    });
});

function calculateGrowth() {
    let gender = document.querySelector('input[name="gender"]:checked').value;
    let birthday = document.getElementById("birthday").value;
    let height = document.getElementById("height").value;
    let weight = document.getElementById("weight").value;

    // Input validation
    if (!birthday) {
        alert("Please select a valid birthday.");
        return;
    }
    if (!height || height <= 0) {
        alert("Please enter a valid height.");
        return;
    }
    if (!weight || weight <= 0) {
        alert("Please enter a valid weight.");
        return;
    }

    // Prepare data to send
    let requestData = {
        gender: gender,
        birthday: birthday,
        height: height,
        weight: weight
    };

    // Send POST request to Flask server
    fetch("/calculate", {
        method: "POST",
        body: JSON.stringify(requestData),
        headers: { "Content-Type": "application/json" },
    })
    .then(response => response.json())
    .then(data => {
        // Display the results in the result div
        document.getElementById("result").innerHTML = `
            <p><strong>Age:</strong> ${data.age}</p>
            <p><strong>Height Percentile:</strong> ${data.height_percentile}</p>
            <p><strong>Weight Percentile:</strong> ${data.weight_percentile}</p>
            <p><strong>BMI:</strong> ${data.bmi}</p>
            <p><strong>BMI Interpretation:</strong> ${data.bmi_interpretation}</p>
        `;
    })
    .catch(error => console.error("Error:", error));
}
