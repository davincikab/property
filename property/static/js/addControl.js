let formControls = document.querySelectorAll("input, select, textarea");
formControls.forEach(formControl => {
    if(!formControl.classList.contains("form-control") && formControl.type != "checkbox") {
        formControl.classList.add('form-control');
        formControl.classList.add('form-control-sm');
    }
    
    if(formControl.type == "checkbox" || formControl.type == "radio") {
        formControl.classList.add("form-check-input")
    }
});