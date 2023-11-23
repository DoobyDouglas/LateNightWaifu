document.addEventListener('DOMContentLoaded', function () {
    function submitForm() {
        let queryValue = document.getElementById('search').value
        window.location.href = '/search/' + encodeURIComponent(queryValue)
        return false
    }
    const searchForm = document.getElementById('search_form');
    searchForm.onsubmit = submitForm
})
