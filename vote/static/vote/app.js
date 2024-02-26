// to show menu links
const navLinks = document.querySelector(".navLinks")
const menuicon = document.querySelector(".menu-icon")
function showNavlinks(){
    menuicon.addEventListener("click", ()=>{
        navLinks.classList.toggle("showNavLinks")
    })
}
showNavlinks()

// on for 5 seconds to show the content the page
function loader() {
    const content = document.querySelector(".content")
    const skeleton_spinner = document.querySelector(".spinner")

    content.style.display="none"
    document.addEventListener("DOMContentLoaded", ()=>{
        skeleton_spinner.style.display="flex"

        setTimeout(() => {
            skeleton_spinner.style.display="none"
            content.style.display="block"
        }, 5000);

    })
}

loader()

