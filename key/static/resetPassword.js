function validateFormPasswordReset(thisForm) {
    with (thisForm) {
        var password_str = thisForm.password.value;
        var password2_str = thisForm.password2.value;
        if (password_str == "" || password2_str == "") {
            alert(("Passwords cannot be empty."));
            return false;
        }
        else if (password_str !== password2_str) {
            alert("Passwords must match.");
            return false;
        }
        else {
            return true;
        }
    }
}
}