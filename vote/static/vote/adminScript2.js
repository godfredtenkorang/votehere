
           
// Constants
const categoryInterfaceContainer = document.querySelector(".category-interface-container");
const navOptions = document.querySelectorAll(".nav-option");
const awardsContainers = document.querySelectorAll(".awards-container");
const nomineeInterfaceContainer = document.querySelector(".nominee-interface-container");
const categoriesContainers = document.querySelectorAll(".categories-container");
const ongoingAwardsContainer = document.querySelector(".awards-ongoing");
const registeredCategoryContainer = document.querySelector(".registered-category-container");
const registeredAwardsContainers = document.querySelectorAll(".registered-awards");
const registration = document.getElementById("Registration");
const registeredCategory = document.querySelectorAll(".registered-category");
const listOfRegisteredNominee = document.querySelector(".list-of-registered-nominee");
const awardsTransactionCcontainer = document.querySelectorAll(".awards-transaction-container")
const transationDetailsContainer = document.querySelector(".transation-details-container")
const transaction_interface_container = document.querySelector(".transaction-interface-container")

// Initial setup
nomineeInterfaceContainer.style.display = "none";
categoryInterfaceContainer.style.display = "none";
registeredCategoryContainer.style.display = "none";
listOfRegisteredNominee.style.display = "none";

transationDetailsContainer.style.display="none"


// Event listeners
awardsContainers.forEach((awards) => {
    awards.addEventListener("click", () => {
        categoryInterfaceContainer.style.display = "block";
        ongoingAwardsContainer.style.display = "none";
    });
});

navOptions.forEach((navOption) => {
    navOption.addEventListener("click", () => {
        categoryInterfaceContainer.style.display = "none";
        nomineeInterfaceContainer.style.display = "none";
        listOfRegisteredNominee.style.display = "none";
        transationDetailsContainer.style.display="none"
    });
});

categoriesContainers.forEach((category) => {
    category.addEventListener("click", () => {
        nomineeInterfaceContainer.style.display = "block";
        categoryInterfaceContainer.style.display = "none";
    });
});

registeredAwardsContainers.forEach((awardsRegistered) => {
    awardsRegistered.addEventListener("click", () => {
        registeredCategoryContainer.style.display = "block";
        registration.style.display = "none";
    });
});

registeredCategory.forEach((categoryRegistered) => {
    categoryRegistered.addEventListener("click", () => {
        listOfRegisteredNominee.style.display = "block";
        registeredCategoryContainer.style.display = "none";
    });
});

awardsTransactionCcontainer.forEach((awardTransac)=>{
    awardTransac.addEventListener("click",()=>{
        transationDetailsContainer.style.display="block"
        transaction_interface_container.style.display="none"
    })
})


