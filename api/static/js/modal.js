document.getElementById("priceForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const modal = document.getElementById("modalOverlay");
    const modalContent = document.querySelector(".modalContent");

    // Initial loader
    modalContent.innerHTML = `
        <span id="closeModal">&times;</span>
        <div class="loader"></div>
        <div>Starting to track your product...</div>
    `;
    modal.style.display = "flex";

    // After 2 seconds, show success checkmark
    setTimeout(() => {
        modalContent.innerHTML = `
            <span id="closeModal">&times;</span>
            <div class="checkmark">✔</div>
            <div style="margin-top: 15px;">Product is being tracked successfully!</div>
        `;
        document.querySelector(".checkmark").style.display = "block";
        addCloseListener();
    }, 2000);
});

function addCloseListener() {
    document.getElementById("closeModal").addEventListener("click", function() {
        document.getElementById("modalOverlay").style.display = "none";
    });
}