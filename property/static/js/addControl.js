let formControls = document.querySelectorAll("input, select, textarea");
formControls.forEach(formControl => {
    if(!formControl.classList.contains("form-control")) {
        formControl.classList.add('form-control');
        formControl.classList.add('form-control-sm');
    }
});