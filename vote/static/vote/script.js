// Selecting the necessary elements
const uploadImage = document.querySelector(".uploadImage");
const imageReceiver = document.querySelector(".image-receiver");

// Adding an event listener to the image input field
uploadImage.addEventListener("change", handleImageUpload);

// Function to handle image upload
function handleImageUpload(event) {
    const selectedImg = event.target.files[0];
    
    if (selectedImg) {
        // Creating a FileReader object
        const reader = new FileReader();
        
        // Callback function when the image is loaded
        reader.onload = function(event) {
            // Creating an image element
            const createImage = document.createElement("img");
            createImage.src = event.target.result;
            
            // Clearing the previous image and displaying the new one
            imageReceiver.innerHTML = "";
            imageReceiver.appendChild(createImage);
        };
        
        // Reading the selected image as a data URL
        reader.readAsDataURL(selectedImg);
    }
}
