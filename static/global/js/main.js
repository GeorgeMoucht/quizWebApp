// Functionality to toggle the hamburger menu on smaller devices
function toggleMenu() {
    const listContainer = document.querySelector('.list-container');
    const hamburger = document.querySelector('.hamburger');
    const profileMenu = document.querySelector('.profile-menu');

    // Close the profile dropdown if it's open
    if (profileMenu.classList.contains('open')) {
        profileMenu.classList.remove('open');
    }

    // Toggle the navigation menu
    listContainer.classList.toggle('open');
    hamburger.classList.toggle('open');
}

// Functionality to toggle the profile dropdown menu
function toggleDropdown() {
    const profileMenu = document.querySelector('.profile-menu');
    const listContainer = document.querySelector('.list-container');
    const hamburger = document.querySelector('.hamburger');

    // Close the navigation menu if it's open
    if (listContainer.classList.contains('open')) {
        listContainer.classList.remove('open');
        hamburger.classList.remove('open');
    }

    // Toggle the profile dropdown menu
    profileMenu.classList.toggle('open');
}

// Close menus when clicking outside
document.addEventListener('click', function (event) {
    const listContainer = document.querySelector('.list-container');
    const hamburger = document.querySelector('.hamburger');
    const profileMenu = document.querySelector('.profile-menu');

    // Check if the click is outside the navigation menu
    if (
        !listContainer.contains(event.target) &&
        !hamburger.contains(event.target) &&
        listContainer.classList.contains('open')
    ) {
        listContainer.classList.remove('open');
        hamburger.classList.remove('open');
    }

    // Check if the click is outside the profile dropdown menu
    if (
        !profileMenu.contains(event.target) &&
        profileMenu.classList.contains('open')
    ) {
        profileMenu.classList.remove('open');
    }
});
