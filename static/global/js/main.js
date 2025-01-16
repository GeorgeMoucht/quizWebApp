// Functionallity to open hambuger menu on smaller devices
function toggleMenu() {
    // const navLinks = document.querySelector('.nav-links');
    // const hamburger = document.querySelector('.hamburger');

    // hamburger.classList.toggle('open');
    // navLinks.classList.toggle('open');
    const listContainer = document.querySelector('.list-container');
    const hambuger = document.querySelector('.hamburger');

    listContainer.classList.toggle('open');
    hambuger.classList.toggle('open');
}

function toggleDropdown() {
    const profileMenu = document.querySelector('.profile-menu');
    profileMenu.classList.toggle('open');
}