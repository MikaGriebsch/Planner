$(document).ready(function() {
	//select2 für alle sichtbaren select2-Elemente 
	let selection = Array.from(document.querySelectorAll('.django-select2'))
		.filter(sel => sel.offsetParent !== null);
	initSelect2(selection);

	hideDeleteCheckboxes();
	filterEmptyForms();
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

function addForm(templateId, targetId, select2 = false) {
	let prefix = targetId.split('-')[0];
  let formIdx = parseInt(document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`).value, 10);
	let template = document.getElementById(templateId).innerHTML;
	let newForm = template.replace(/__prefix__/g, formIdx);
			
	document.getElementById(targetId).insertAdjacentHTML('beforeend', newForm);

	let newFormContainer = document.getElementById(targetId).lastElementChild; 
	newFormContainer.id = prefix + '-form-' + formIdx;

	// Button event richtig setzten
	let deleteBtn = newFormContainer.querySelector('.delete-btn');
	if (deleteBtn) {
		deleteBtn.setAttribute('onclick', `deleteForm('${prefix}-form-${formIdx}')`);
	}

	console.log("Added new form with ID: " + newFormContainer.id);

	if (select2){
		initSelect2(newFormContainer.querySelector('.django-select2'));
	}
	hideDeleteCheckboxes();

	document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`).value = formIdx + 1;
	return newFormContainer;
}

function addGradeForm(templateId, targetId, select2 = false){
	let container = addForm(templateId, targetId, select2);
	// automatische Nummerierung der Klassenstufe
	const nextNumber = getNextGradeNumber();
	const nameInput = container.querySelector('input[name$="-name"]');
	if (nameInput) {
			nameInput.value = nextNumber;
			
			const heading = container.querySelector('h2');
			heading.textContent = `Klassenstufe ${nextNumber}`;
	}

}
        
function deleteForm(formId) {
		let form = document.getElementById(formId);
		let deleteCheckbox = form.querySelector('input[name$="-DELETE"]');
		deleteCheckbox.checked = true;

		form.style.display = 'none';
		
		console.log("Form " + formId + " marked for deletion. DELETE checkbox checked:", deleteCheckbox.checked);
}

function getNextGradeNumber() {
	const gradeNumbers = [];
	document.querySelectorAll('.grade-form input[name$="-name"]').forEach(input => {
			if (input.value) {
					const num = parseInt(input.value, 10);
					if (!isNaN(num)) {
							gradeNumbers.push(num);
					}
			}
	});
	// return 1 if no grades
	if (gradeNumbers.length === 0) {
			return 1;
	}
	return Math.max(...gradeNumbers) + 1;
}

// Leere Formulare filtern
function filterEmptyForms() {
	document.querySelector('form').addEventListener('submit', function() {
			// Alle Formulartypen durchgehen, die leere Formulare haben könnten
			const formTypes = [
					{selector: '.subject_grade-form', fields: ['subject', 'wochenstunden']},
					{selector: '.class-form', fields: ['name', 'schueleranzahl']},
			];
			
			formTypes.forEach(function(type) {
					document.querySelectorAll(type.selector).forEach(function(form) {
							let isEmpty = true;
							const deleteChecked = form.querySelector('input[name$="-DELETE"]')?.checked;
							
							// Wenn bereits zum Löschen markiert, nicht als leer betrachten
							if (deleteChecked) {
									isEmpty = false;
							} else {
									// Prüfe, ob irgendwelche relevanten Felder einen Wert haben
									type.fields.forEach(function(fieldName) {
											const field = form.querySelector(`[name$="-${fieldName}"]`);
											if (field && field.value) {
													isEmpty = false;
											}
									});
							}
							
							// Wenn das Formular leer ist, deaktiviere alle Felder
							if (isEmpty) {
									form.querySelectorAll('input, select, textarea').forEach(function(input) {
											input.disabled = true;
									});
									console.log('Disabled empty form:', form.id);
							}
					});
			});
	});
}