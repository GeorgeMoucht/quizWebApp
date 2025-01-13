// Functionallity to open hambuger menu on smaller devices
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    const hamburger = document.querySelector('.hamburger');

    hamburger.classList.toggle('open');
    navLinks.classList.toggle('open');
}