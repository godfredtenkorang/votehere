const darkModeButton = document.querySelector(".darkMode-button")
const main = document.querySelector(".main")
let isdarkMode = localStorage.getItem("isdarkMode")
const Settings = document.querySelector(".sett-but")

// NEW
darkModeButton.style.display = "none"

Settings.addEventListener("click",()=>{
   if(darkModeButton.style.display === "none"){
    darkModeButton.style.display = "block"
   }else{
    darkModeButton.style.display = "none"
   }
})

    if(isdarkMode){
        if(isdarkMode === "true")
        document.body.classList.add("dark-mode") // UPDATED
    }

    darkModeButton.addEventListener("click",()=>{
        isdarkMode = !isdarkMode

       if(isdarkMode){
        document.body.classList.add("dark-mode")    // UPDATED
       }  
       else{
        document.body.classList.remove("dark-mode") // UPDATED
       }
     localStorage.setItem("isdarkMode" , isdarkMode)
    })