function validateFormPasswordReset(thisForm) {
    with (thisForm) {
        var password = thisForm.password.value;
        var password2 = thisForm.password2.value;
        if (password == "" || password2 == "") {
            alert(("Passwords cannot be empty."));
            return false;
        }
        if (password.valueOf() != password2.valueOf()) {
            alert(("Passwords must match. Password1 = %s, Password2 = %s", password, password2));
            return false;
        }
    }
}
