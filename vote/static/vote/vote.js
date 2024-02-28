
function voteForm() {
    const number_of_vote = document.getElementById("number-of-vote");
    const amountToPayDisplay = document.querySelector(".amount-to-pay-per-vote");

    const amountBePaidForVote = 0.70;

    number_of_vote.addEventListener("input", () => {
        const userName = document.getElementById("user-name").value

        // Calculate the amount to be paid based on the number of votes
        const numberOfVotes = parseFloat(number_of_vote.value);
        const amountToPay = numberOfVotes * amountBePaidForVote;


        // Display the amount to be paid
        amountToPayDisplay.textContent = `Dear ${userName}, you will pay Ghs  ${amountToPay.toFixed(2)} for ${numberOfVotes} votes`;
        amountToPayDisplay.style.display = "flex";

        // Check if the number of vote field is empty, if it is empty, then hide the amountToPayDisplay
        if (number_of_vote.value === "") {
            amountToPayDisplay.style.display = "none";
        }
    });


}

voteForm();
// remove vote form
const removeVotingForm = document.getElementById("removeVotingForm")
// Select the voting form section

const votingFormSection = document.querySelector(".voting-form-section")

removeVotingForm.addEventListener("click", () => {
    votingFormSection.style.display = 'none'
})
// Select all vote buttons
const voteButtons = document.querySelectorAll(".vote-button button")


function handleVoteButtonClick(event) {
    // Get the parent container of the vote button
    const nomineesDetail = event.target.closest(".nominees-detail")

    // Get the nominee image
    const nomineeImageSrc = nomineesDetail.parentElement.querySelector("img").src

    // Get the nominee name
    const nomineeName = nomineesDetail.querySelector("h3").textContent


    // Create elements for nominee image
    const nomineeImage = document.createElement("div")
    nomineeImage.classList.add("nominee-image")
    nomineeImage.innerHTML = `<img src="${nomineeImageSrc}" alt="">`;

    // Create elements for nominee
    const nominee_name = document.createElement("div")
    nominee_name.classList.add("nominee-name")
    nominee_name.innerHTML = nomineeName


    // Append user image and name to user-image-name container
    const nominee_image_name_Container = document.querySelector(".nominee-image-name")
    nominee_image_name_Container.innerHTML = ""
    nominee_image_name_Container.appendChild(nomineeImage)
    nominee_image_name_Container.appendChild(nominee_name)

    // Show the voting form section

    votingFormSection.style.display = "flex"



}
// Add click event listener to each vote button
voteButtons.forEach(button => {
    button.addEventListener("click", handleVoteButtonClick)
})



