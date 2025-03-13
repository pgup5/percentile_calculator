document.addEventListener("DOMContentLoaded", function () {
    let birthdayInput = document.getElementById("birthday");

    // 預設日期
    birthdayInput.value = "2020-01-01";

    // 確保日期範圍在 2004-2030 之間
    birthdayInput.addEventListener("change", function () {
        let selectedDate = new Date(birthdayInput.value);
        let minDate = new Date("2004-01-01");
        let maxDate = new Date("2030-12-31");

        if (selectedDate < minDate || selectedDate > maxDate) {
            alert("請選擇 2004 至 2030 年之間的日期。");
            birthdayInput.value = "2010-01-01"; 
        }
    });
});

function calculateGrowth() {
    let gender = document.querySelector('input[name="gender"]:checked').value;
    let birthday = document.getElementById("birthday").value;
    let height = document.getElementById("height").value;
    let weight = document.getElementById("weight").value;

    if (!birthday) {
        alert("請選擇有效的出生日期。");
        return;
    }
    if (!height || height <= 0) {
        alert("請輸入正確的身高。");
        return;
    }
    if (!weight || weight <= 0) {
        alert("請輸入正確的體重。");
        return;
    }

    let requestData = {
        gender: gender,
        birthday: birthday,
        height: height,
        weight: weight
    };

    fetch("/calculate", {
        method: "POST",
        body: JSON.stringify(requestData),
        headers: { "Content-Type": "application/json" },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = `
            <p><strong>年齡：</strong> ${data.age}</p>
            <p><strong>身高百分位：</strong> ${data.height_percentile}</p>
            <p><strong>體重百分位：</strong> ${data.weight_percentile}</p>
            <p><strong>BMI：</strong> ${data.bmi}</p>
            <p><strong>BMI 評估：</strong> ${data.bmi_interpretation}</p>
        `;
    })
    .catch(error => console.error("錯誤：", error));
}
