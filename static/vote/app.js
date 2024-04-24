

// Selecting the navigation links and menu icon elements from the HTML document
const navLinks = document.querySelector(".navLinks");
const menuIcon = document.querySelector(".menu-icon");
const removeNavBar = document.querySelector(".fa-times");

removeNavBar.addEventListener("click", () => {
    navLinks.classList.toggle("showNavLinks");
});
// Adding a click event listener to the menu icon to toggle the visibility of the navigation links
menuIcon.addEventListener("click", () => {
    navLinks.classList.toggle("showNavLinks");
});



// Function to simulate a loading spinner and then display the content after 3 seconds
function loader() {
    // Selecting the content and spinner elements from the HTML document
    const content = document.querySelector(".content");
    const skeletonSpinner = document.querySelector(".spinner");

    // Initially hiding the content and showing the spinner
    content.style.display = "none";
    skeletonSpinner.style.display = "flex";

    // Setting a timeout to hide the spinner and show the content after 3 seconds
    setTimeout(() => {
        skeletonSpinner.style.display = "none";
        content.style.display = "block";
        setTimeout(() => {
            content.style.opacity = "1"; // Fading in the content after it's displayed
        }, 100); // Adding a slight delay to ensure smooth transition
    }, 3000); // Simulating a 3-second loading time
}

// Calling the loader function to start the loading animation when the page loads
loader();


