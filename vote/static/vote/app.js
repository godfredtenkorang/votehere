

// // Selecting the navigation links and menu icon elements from the HTML document
// const navLinks = document.querySelector(".navLinks");
// const menuIcon = document.querySelector(".menu-icon");
// const removeNavBar = document.querySelector(".fa-times");

// removeNavBar.addEventListener("click", () => {
//     navLinks.classList.toggle("showNavLinks");
// });
// // Adding a click event listener to the menu icon to toggle the visibility of the navigation links
// menuIcon.addEventListener("click", () => {
//     navLinks.classList.toggle("showNavLinks");
// });



// // Function to simulate a loading spinner and then display the content after 3 seconds
// function loader() {
//     // Selecting the content and spinner elements from the HTML document
//     const content = document.querySelector(".content");
//     const skeletonSpinner = document.querySelector(".spinner");

//     // Initially hiding the content and showing the spinner
//     content.style.display = "none";
//     skeletonSpinner.style.display = "flex";

//     // Setting a timeout to hide the spinner and show the content after 3 seconds
//     setTimeout(() => {
//         skeletonSpinner.style.display = "none";
//         content.style.display = "block";
//         setTimeout(() => {
//             content.style.opacity = "1"; // Fading in the content after it's displayed
//         }, 100); // Adding a slight delay to ensure smooth transition
//     }, 3000); // Simulating a 3-second loading time
// }

// // Calling the loader function to start the loading animation when the page loads
// loader();



// function voteForm() {
//     // Selecting the input field for the number of votes and the display area for the amount to be paid per vote
//     const numberOfVote = document.getElementById("number-of-vote");
//     const amount_top_pay = document.getElementById("amount-top-pay");
//     const total_amount_top_pay = document.getElementById(
//       "total-amount-top-pay"
//     );
//     // Constant representing the amount to be paid for each vote
//     const amountPerVote = 0.7;


//     const totalAmountTopPay = amountPerVote * 100

//     // Adding an input event listener to the number of votes input field
//     numberOfVote.addEventListener("input", () => {
//         // Parsing the number of votes entered by the user
//         const numberOfVotes = parseFloat(numberOfVote.value);
//         // Calculating the total amount to be paid based on the number of votes
//         const userNumberOfVote = parseFloat(
//           (numberOfVotes * amountPerVote).toFixed(2)
//         );

//         const totalAmountToPay = parseFloat(
//           (numberOfVotes * totalAmountTopPay).toFixed(2)
//         );

//         // Displaying the calculated amount to be paid as a number
//         amount_top_pay.value = userNumberOfVote;

//         total_amount_top_pay.value = totalAmountToPay;

//         // Ensure that the value is a number, not a string
//         if (isNaN(amount_top_pay.value)) {
//             amount_top_pay.value = 0; // Set a default value if NaN
//         }
//         if (isNaN(total_amount_top_pay.value)) {
//           total_amount_top_pay.value = 0; // Set a default value if NaN
//         }
//     });
//     // Add a submit event listener to the form
//     document.querySelector(".form-for-voting").addEventListener("submit", () => {
//         // Convert the value of the 'Amount To pay' field to a number before form submission
//         amount_top_pay.value = parseFloat(amount_top_pay.value);
//     });
// }


















// // Calling the voteForm function to enable vote calculation and display
// voteForm();

// // Handling the removal of the voting form
// const removeVotingForm = document.getElementById("removeVotingForm");
// const votingFormSection = document.querySelector(".voting-form-section");

// removeVotingForm.addEventListener("click", () => {
//     votingFormSection.style.display = 'none'; // Hiding the voting form section when remove button is clicked
// });


// // Handling vote button clicks.This function handles when when a user click on the vote button, it  takes the nominee image and name
// const voteButtons = document.querySelectorAll(".vote-button button");

// // Function to handle vote button click event
// function handleVoteButtonClick(event) {
//     // Find the closest parent element with class "nominees-detail"
//     const nomineesDetail = event.target.closest(".nominees-detail");

//     // Get the source of the nominee image
//     const nomineeImageSrc = nomineesDetail.parentElement.querySelector("img").src;

//     // Get the text content of the nominee name
//     const nomineeName = nomineesDetail.querySelector("h3").textContent;

//     // Get the text content of the nominee category
//     const nomineeCategory = nomineesDetail.querySelector("h2").textContent;

//     // Create a div element for the nominee image
//     const nomineeImage = document.createElement("div");
//     nomineeImage.classList.add("nominee-image");
//     nomineeImage.innerHTML = `<img src="${nomineeImageSrc}" alt="">`;

//     // Create a div element for the nominee name
//     const nomineeNameElement = document.createElement("div");
//     nomineeNameElement.classList.add("nominee-name");
//     nomineeNameElement.textContent = nomineeName;

//     // Create a div element for the nominee category
//     const nomineeCategoryContainer = document.createElement("div");
//     nomineeCategoryContainer.textContent = nomineeCategory;

//     // Find the container for nominee image and name
//     const nomineeImageNameContainer = document.querySelector(".nominee-image-name");

//     // Clear any existing content in the container
//     nomineeImageNameContainer.innerHTML = "";

//     // Append the nominee image, name, and category to the container
//     nomineeImageNameContainer.appendChild(nomineeImage);
//     nomineeImageNameContainer.appendChild(nomineeNameElement);
//     nomineeImageNameContainer.appendChild(nomineeCategoryContainer);

//     // Display the voting form section by setting its style display property to "flex"
//     votingFormSection.style.display = "flex"; 
// }


// // Adding click event listeners to each vote button
// voteButtons.forEach(button => {
//     button.addEventListener("click", handleVoteButtonClick);
// });

