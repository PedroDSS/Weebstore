// Used for Searchbar only for product-gallery-pages

if (document.getElementById('searchbar') != undefined && document.getElementById('searchbar') != null) {
    // Get searchbar
    let searchbar = document.getElementById('searchbar');

    // Get All blocks items like Manga, Figurine...
    let elements = document.querySelectorAll('.searchable');
    if (elements != undefined && elements != null) {
        searchbar.addEventListener('input', function () {
            for (let i = 0; i < elements.length; i++) {
                // If data-name attribute of the element match show it, else hide it
                if (elements[i].getAttribute('data-name').toLowerCase().includes(searchbar.value.toLowerCase())) {
                    elements[i].classList.remove('hide');
                } else {
                    elements[i].classList.add('hide');
                }
            }
        });
    }
}
