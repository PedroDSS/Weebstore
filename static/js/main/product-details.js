// For the quantity in product-details pages
if (document.getElementById('select-quantity') != undefined && document.getElementById('select-quantity') != null) {
    let select = document.getElementById('select-quantity');
    let input = document.getElementById('id_quantity');
    // Add event change for select to update quantity value for the form
    select.addEventListener("change", function () {
        input.setAttribute('value', select.value);
    });
}
