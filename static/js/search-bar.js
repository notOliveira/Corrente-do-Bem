// Div pai
const listDonations = document.getElementById('list-all-donations');
// Input
const searchBar = document.getElementById('search-bar');
// Items
const donations = document.getElementsByClassName('donations-item');
// Form
// const searchDonationsForm = document.getElementById('search-donations');

searchBar.addEventListener('input', (e) => {
    let filter = e.target.value.toLowerCase();

    Array.from(donations).forEach((donation) => {
        let donationName = donation.getElementsByClassName('donation-user')[0].innerText;
        let donationDate = donation.getElementsByClassName('donation-date')[0].innerText;
        if (donationName.toLowerCase().indexOf(filter) != -1 || donationDate.toLowerCase().indexOf(filter) != -1) {
            donation.style.display = 'block';
        } else {
            donation.style.display = 'none';
        }
    });
});