function validateFormPasswordReset(thisForm) {
    with (thisForm) {
        var password = thisForm.password.value;
        var password2 = thisForm.password2.value;
        if (password.valueOf() == "" || password2.valueOf() == "") {
            alert(("Passwords cannot be empty."));
            return false;
        }
        else if (password.valueOf() !== password2.valueOf()) {
            alert("Passwords must match.");
            console.log(password.valueOf());
            console.log(password2.valueOf());
            return false;
        }
        else {
            return true;
        }
    }
}
