// Add event listeners to sidebar options
document.querySelectorAll('.nav-option').forEach(option => {
    option.addEventListener('click', function() {
        // Remove the 'active' class from all buttons
        document.querySelectorAll('.nav-option').forEach(btn => {
            btn.classList.remove('actives');
        });
        // Add the 'active' class to the clicked button
        option.classList.add('actives');

        // Hide all data sections
        document.querySelectorAll('.data').forEach(data => {
            data.style.display = 'none';
        });

        // Get the ID of the corresponding data section
        let targetId = option.dataset.target;
        // Display the corresponding data section
        document.getElementById(targetId).style.display = 'block';

        // Store the ID of the currently displayed data section in local storage
        localStorage.setItem('currentDataSection', targetId);
    });
});

// Check if there's a stored data section ID in local storage
let currentDataSection = localStorage.getItem('currentDataSection');
if (currentDataSection) {
    // Display the corresponding data section
    document.getElementById(currentDataSection).style.display = 'block';
} else {
    // Display the first data section by default
    document.querySelector('.data').style.display = 'block';
}


let menuicn = document.querySelector(".menuicn");
		let nav = document.querySelector(".navcontainer");

		menuicn.addEventListener("click", () => {
			nav.classList.toggle("navclose");
		})


