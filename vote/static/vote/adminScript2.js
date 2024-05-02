
    const darkModeButton = document.querySelector(".darkMode-button")
    const main = document.querySelector(".main")
    let isdarkMode = localStorage.getItem("isdarkMode")
    const Settings = document.querySelector(".sett-but")

Settings.addEventListener("click",()=>{
   if( darkModeButton.style.display===""){
    darkModeButton.style.display="block"
   }else{
    darkModeButton.style.display=""
   }
})



    if(isdarkMode){
        if(isdarkMode=== "true")
        main.style.backgroundColor="#333333"
    }

    darkModeButton.addEventListener("click",()=>{
        isdarkMode = !isdarkMode

       if(isdarkMode){
        main.style.backgroundColor="#333333"
       }  
       else{
        main.style.backgroundColor=""
       }
     localStorage.setItem("isdarkMode" , isdarkMode)
    })

