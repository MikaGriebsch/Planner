$(document).ready(function() {
	//select2 für alle sichtbaren select2-Elemente 
	let selection = Array.from(document.querySelectorAll('.django-select2'))
		.filter(sel => sel.offsetParent !== null);
	initSelect2(selection);

	hideDeleteCheckboxes();
});

function initSelect2(selection) {
	$(selection).select2({
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

function addForm(templateId, formsetId, select2 = true) {
	let prefix = formsetId.startsWith('teacher') ? 'teacher' : 'subject';
  let formIdx = parseInt(document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`).value, 10);
	let template = document.getElementById(templateId).innerHTML;
	let newForm = template.replace(/__prefix__/g, formIdx);
			
	document.getElementById(formsetId).insertAdjacentHTML('beforeend', newForm);

	let newFormContainer = document.getElementById(formsetId).lastElementChild; 
	newFormContainer.id = prefix + '-form-' + formIdx;

	console.log("Added new form with ID: " + newFormContainer.id);

	if (select2){
		initSelect2(newFormContainer.querySelector('.django-select2'));
	}
	hideDeleteCheckboxes();

	document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`).value = formIdx + 1;
}
        
function deleteForm(formId) {
		let form = document.getElementById(formId);
		let deleteCheckbox = form.querySelector('input[name$="-DELETE"]');
		deleteCheckbox.checked = true;

		form.style.display = 'none';
		
		console.log("Form " + formId + " marked for deletion. DELETE checkbox checked:", deleteCheckbox.checked);
}