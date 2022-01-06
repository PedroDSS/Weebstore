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