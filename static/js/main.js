const navbarToggle =() =>{
    let menu = document.getElementById("navbarBasicExample")
    if (menu.classList.contains('is-active')){
        menu.classList.remove("is-active")
    }
    else{
        menu.classList.add("is-active")
    }
}

