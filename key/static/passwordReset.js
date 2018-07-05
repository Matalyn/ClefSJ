function validateFormPasswordReset(thisForm) {
    with (thisForm) {
        var password = thisForm.password.value;
        var password2 = thisForm.password2.value;
        if (password == "" || password2 == "") {
            alert(("Passwords cannot be empty."));
            return false;
        }
        if (password !== password2) {
            alert("Passwords must match.");
            console.log(password.type());
            console.log(password.valueOf());
            console.log(password2.type());
            console.log(password2.valueOf());
            return false;
        }
    }
}
