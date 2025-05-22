function openNav() {
    document.getElementsByClassName("sidenav")[0].classList.add("active");
    document.getElementsByClassName("content")[0].classList.remove("active");
}

function closeNav() {
    document.getElementsByClassName("sidenav")[0].classList.remove("active");
    document.getElementsByClassName("content")[0].classList.add("active");
}