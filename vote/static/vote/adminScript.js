// log out pop up
const logoutpop = document.querySelector(".logout-pop")
    const DontLogout = document.querySelector(".DontLogout")
	const logoutBtn = document.querySelector(".logout-btn")

	logoutBtn.addEventListener("click",()=>{
		logoutpop.style.display="block"

	})
    DontLogout.addEventListener('click',()=>{
        logoutpop.style.display="none"
    })


	// menu 
let menuicn = document.querySelector(".menuicn");
		let nav = document.querySelector(".navcontainer");

		menuicn.addEventListener("click", () => {
			nav.classList.toggle("navclose");
		})


