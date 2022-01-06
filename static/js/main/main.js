function toast_message(message, level) {
    if (level == 10 || level == 20) {
        // Display an info toast with no title
        toastr.info(message);
    } else if (level == 25) {
        // Display a success toast, with a title
        toastr.success(message);
    } else if (level == 30) {
        // Display a warning toast, with no title
        toastr.warning(message);
    } else if (level == 40) {
        // Display an error toast, with a title
        toastr.error(message);
    }
}

function changeQuantity() {
    select = document.getElementById('select-quantity')
    input = document.getElementById('id_quantity')
    // Change the quantity value for the form depending on the real product quantity
    input.setAttribute('value', select.value);
}

function search_from_text(obj) {
    // Get All blocks items like Manga, Figurine...
    elements = document.querySelectorAll('.searchable');
    if (elements != undefined) {
        for (let i = 0; i < elements.length; i++) {
            // If data-name attribute of the element match show it, else hide it
            if (elements[i].getAttribute('data-name').toLowerCase().includes(obj.value.toLowerCase())) {
                elements[i].classList.remove('hide');
            } else {
                elements[i].classList.add('hide');
            }
        }
    }
}