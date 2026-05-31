const toggle = document.getElementById("darkModeToggle");
const Settings = document.querySelector(".sett-but");

// restore saved preference
const savedMode = localStorage.getItem("isdarkMode");
if (savedMode === "true") {
  document.body.classList.add("dark-mode");
  toggle.checked = true;
}

// toggle on change
toggle.addEventListener("change", () => {
  const isDark = toggle.checked;
  document.body.classList.toggle("dark-mode", isDark);
  localStorage.setItem("isdarkMode", isDark);
});

// if you still want settings button to show/hide the toggle wrapper
Settings.addEventListener("click", () => {
  const wrapper = document.querySelector(".dark-toggle");
  wrapper.style.display = wrapper.style.display === "none" ? "flex" : "none";
});