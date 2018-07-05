function validateFormPasswordReset(thisForm) {
    with (thisForm) {
        var password = thisForm.password.value;
        var password2 = thisForm.password2.value;
        if (password == "" || password2 == "") {
            alert(("Passwords cannot be empty."));
            return false;
        }
        if (password.valueOf().trim() != password2.valueOf().trim()) {
            alert(("Passwords must match."));
            return false;
        }
    }
}
