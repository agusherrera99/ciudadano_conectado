document.addEventListener("DOMContentLoaded", function () {
    const resultBarPercentages = document.querySelectorAll(".result-bar-percentage");
    resultBarPercentages.forEach((bar => {
        const percentage = bar.getAttribute("data-percentage");
        bar.style.width = `${percentage}%`;
    }));
});