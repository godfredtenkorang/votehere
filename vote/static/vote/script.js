const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const image_note = document.querySelector(".image-upload-note")
const imageExample = document.querySelector(".imageExmple")

if (inputFile && imageView) {
    inputFile.addEventListener("change", uploadImage);
}

function uploadImage() {
    if (inputFile.files.length > 0) {
        const imgLink = URL.createObjectURL(inputFile.files[0]);
        imageView.querySelector("img").src = imgLink;
        image_note.textContent = "Nominee image selected"
        imageExample.style.displya = "none"
    } else {
        console.error("No file selected.");
    }
}