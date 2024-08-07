const listDonations = document.getElementById('list-all-donations');
const searchBar = document.getElementById('search-bar');
const searchDonationsForm = document.getElementById('search-donations');

searchDonationsForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Search button clicked');
    // request to API localhost:8000/api/v1/donations with params
    // organization_id, email
});