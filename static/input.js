$(document).ready(function() {
	initSelect2();
	hideDeleteCheckboxes();
});

function initSelect2() {
	$('.django-select2').not('#empty-teacher-form .django-select2').select2({
		placeholder: "Wähle Fächer aus...",
		allowClear: true, 
		tokenSeparators: [','],
		width: 200,
	});
}
function hideDeleteCheckboxes() {
	document.querySelectorAll('input[name$="-DELETE"]').forEach(function(checkbox) {
			checkbox.style.display = 'none';
	});
}

function addTeacher() {
    let formIdx = parseInt(document.getElementById("id_form-TOTAL_FORMS").value, 10);
    let template = document.getElementById("empty-teacher-form").innerHTML;
    let newForm = template.replace(/__prefix__/g, formIdx);
            
    document.getElementById("teacher-forms").insertAdjacentHTML('beforeend', newForm);
    
    // WICHTIG: ID des neuen Formulars explizit setzen
    let newFormContainer = document.getElementById("teacher-forms").lastElementChild;
    newFormContainer.id = 'form-' + formIdx;
    console.log("Added new form with ID:", 'form-' + formIdx);
    
    document.getElementById("id_form-TOTAL_FORMS").value = formIdx + 1;
		$(newFormContainer.querySelector('.django-select2')).select2({
			placeholder: "Wähle Fächer aus...",
			allowClear: true, 
			tokenSeparators: [','],
			width: 200,
		});
		hideDeleteCheckboxes();
}
        
function deleteForm(formId) {
		let form = document.getElementById(formId);
		let deleteCheckbox = form.querySelector('input[name$="-DELETE"]');
		deleteCheckbox.checked = true;
		

		form.style.display = 'none';
		
		console.log("Form " + formId + " marked for deletion. DELETE checkbox checked:", deleteCheckbox.checked);
}