

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



// Function to handle the voting form
function voteForm() {
    // Selecting the input field for the number of votes and the display area for the amount to be paid per vote
    const numberOfVote = document.getElementById("number-of-vote");
    const amountToPayDisplay = document.querySelector(".amount-to-pay-per-vote");

    // Constant representing the amount to be paid for each vote
    const amountPerVote = 0.70;

    // Adding an input event listener to the number of votes input field
    numberOfVote.addEventListener("input", () => {
        // Retrieving the user's name from the input field
        const userName = document.getElementById("user-name").value;

        // Parsing the number of votes entered by the user
        const numberOfVotes = parseFloat(numberOfVote.value);

        // Calculating the total amount to be paid based on the number of votes
        const totalAmountToPay = numberOfVotes * amountPerVote;

        // Displaying the calculated amount to be paid
        amountToPayDisplay.textContent = `Dear ${userName}, you will pay Ghs ${totalAmountToPay.toFixed(2)} for ${numberOfVotes} votes`;
        amountToPayDisplay.style.display = "flex"; // Showing the amount to be paid
        if (numberOfVote.value === "") {
            amountToPayDisplay.style.display = "none"; // Hiding the amount display if the input field is empty
        }
    });
}

// Calling the voteForm function to enable vote calculation and display
voteForm();

// Handling the removal of the voting form
const removeVotingForm = document.getElementById("removeVotingForm");
const votingFormSection = document.querySelector(".voting-form-section");

removeVotingForm.addEventListener("click", () => {
    votingFormSection.style.display = 'none'; // Hiding the voting form section when remove button is clicked
});


// Handling vote button clicks.This function handles when when a user click on the vote button, it  takes the nominee image and name
const voteButtons = document.querySelectorAll(".vote-button button");

function handleVoteButtonClick(event) {
    const nomineesDetail = event.target.closest(".nominees-detail");
    const nomineeImageSrc = nomineesDetail.parentElement.querySelector("img").src;
    const nomineeName = nomineesDetail.querySelector("h3").textContent;

    const nomineeImage = document.createElement("div");
    nomineeImage.classList.add("nominee-image");
    nomineeImage.innerHTML = `<img src="${nomineeImageSrc}" alt="">`;

    const nomineeNameElement = document.createElement("div");
    nomineeNameElement.classList.add("nominee-name");
    nomineeNameElement.textContent = nomineeName;

    const nomineeImageNameContainer = document.querySelector(".nominee-image-name");
    nomineeImageNameContainer.innerHTML = "";
    nomineeImageNameContainer.appendChild(nomineeImage);
    nomineeImageNameContainer.appendChild(nomineeNameElement);

    votingFormSection.style.display = "flex"; // Showing the voting form section
}

// Adding click event listeners to each vote button
voteButtons.forEach(button => {
    button.addEventListener("click", handleVoteButtonClick);
});

