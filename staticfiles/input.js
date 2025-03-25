$(document).ready(function() {
	//select2 für alle sichtbaren select2-Elemente 
	let selection = Array.from(document.querySelectorAll('.django-select2'))
		.filter(sel => sel.offsetParent !== null);

	initSelect2(selection);
	hideDeleteCheckboxes();
	filterEmptyForms();
  setupSubjectAutoSave();
	setupGradeAutoSave();
	showErrorsInForms();
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
    if (templateId === 'empty-subject-form') {
      deleteBtn.setAttribute('onclick', `deleteSubjectForm('${prefix}-form-${formIdx}')`);
    }
    else if (templateId === 'empty-grade-form') {
      deleteBtn.setAttribute('onclick', `deleteGradeForm('${prefix}-form-${formIdx}')`);
    }
    else {
      deleteBtn.setAttribute('onclick', `deleteForm('${prefix}-form-${formIdx}')`);
    }
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
	setupGradeFormListener(container);
	saveGrade(container);
	return container;
}

function addSubjectForm(templateId, targetId, select2 = false){
	container = addForm(templateId, targetId, select2);
	setupSubjectFormListener(container);
}
        
function deleteForm(formId) {
	let form = document.getElementById(formId);
	
	let isEmpty = true;
	const inputs = form.querySelectorAll('input:not([type="hidden"]):not([name$="-DELETE"]), select, textarea');
	inputs.forEach(input => {
		if (input.value && input.value.trim() !== '') {
			isEmpty = false;
		}
	});
	
	// nur wenn nicht empty
	if (!isEmpty && !confirm('Möchten Sie dieses Fach wirklich löschen?')) {
		return;
	}
	
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
//getCookie aus Django-Dokumentation
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

//Funktionen für AJAX-Requests
function addOrUpdateModel(url, payload) {
  return fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json"
    },
    body: JSON.stringify({payload: payload})
  })
	.then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  });
}

//function to get/write data from/to server
function getModelData(url) {
  return fetch(url, {
    method: "GET",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
			"Content-Type": "application/json"
    },
  })
  .then(response => { 
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  });
}
function setupSubjectAutoSave() {
  document.querySelectorAll('.subject-form').forEach((form) => {
    setupSubjectFormListener(form);
  });
}

function setupSubjectFormListener(form) {
  const nameField = form.querySelector('input[name$="-name"]');
  const abkuerzungField = form.querySelector('input[name$="-abkuerzung"]');
  
  if (!nameField || !abkuerzungField) return;
  
  // Event-Listener für Input-Änderungen
  [nameField, abkuerzungField].forEach(field => {
    field.addEventListener('blur', () => {
      
      if (nameField.value && abkuerzungField.value) {
        saveSubject(form);
      }
    });
  });
}

function saveSubject(form) {
  const idField = form.querySelector('input[name$="-id"]');
  const nameField = form.querySelector('input[name$="-name"]');
  const abkuerzungField = form.querySelector('input[name$="-abkuerzung"]');
  
  const subjectData = {
    id: idField ? idField.value : '',
    name: nameField.value,
    abkuerzung: abkuerzungField.value
  };
  
  addOrUpdateModel('/schedule/create/save-subject/', subjectData)
    .then(data => {
      if (data.success) {
        if (idField && !idField.value) {
          idField.value = data.subject_id;
        }
        console.log(`${idField.value} saved successfully`)
        showSavingStatus(form, "✓ Gespeichert", "success");
        updateSubjectDropdowns();

      } else {
        console.log(data.message || "Fehler beim Speichern");
				showSavingStatus(form, data.message || "Fehler beim Speichern", "error");
      }
    })
    .catch(error => {
      console.error("Error saving model:", error);
    });
}

function setupGradeAutoSave() {
  document.querySelectorAll('.grade-form').forEach((form) => {
    setupGradeFormListener(form);
  });
}

function setupGradeFormListener(form) {
  const nameField = form.querySelector('input[name$="-name"]');
  
  if (!nameField) return;
  
  // Event-Listener für Input-Änderungen
  nameField.addEventListener('blur', () => {
    if (nameField.value) {
      saveGrade(form);
    }
  });
}

function saveGrade(form) {
  const idField = form.querySelector('input[name$="-id"]');
  const nameField = form.querySelector('input[name$="-name"]');
  
  const gradeData = {
    id: idField ? idField.value : '',
    name: nameField.value
  };
  
  addOrUpdateModel('/schedule/create/save-grade/', gradeData)
    .then(data => {
      if (data.success) {
        if (idField && !idField.value) {
          idField.value = data.grade_id;
					setupNewGradeContainers(form, data.grade_id);
        }

        const heading = form.querySelector('h2');
        if (heading) {
          heading.textContent = `Klassenstufe ${nameField.value}`;
        }
        
        console.log(`Grade ${idField.value} saved successfully`);
        showSavingStatus(form, "✓ Gespeichert", "success");
      } else {
        console.log(data.message || "Fehler beim Speichern");
        showSavingStatus(form, data.message || "Fehler beim Speichern", "error");
      }
    })
    .catch(error => {
      console.error("Error saving grade:", error);
    });
}

// Hilfsfunktionen für die Benutzeroberfläche (akutell nur success benutzt)
function showSavingStatus(form, message, type = "info", duration = 2000) {
	console.log("Form:", form, "Message:", message, "Type:", type);
  let statusEl = form.querySelector('.saving-status');
  if (!statusEl) {
    statusEl = document.createElement('div');
    statusEl.className = 'saving-status';
    form.appendChild(statusEl);
  }
  
  statusEl.textContent = message;
  statusEl.className = `saving-status status-${type}`;

	setTimeout(() => {
		statusEl.remove();
	}, duration);
}

// Funktion zum Aktualisieren aller Subject-Dropdowns (cleanup dringend nötig)
function updateSubjectDropdowns() {
	console.log("Updating subject dropdowns...");
	getModelData('/schedule/create/get-subjects/')
		.then(data => {
			if (!data.success) {
				console.error("Failed to get subjects");
				return;
			}
			const selects = document.querySelectorAll('.django-select2:not([disabled])');
			
			selects.forEach(select => {
				const isMultiple = select.multiple
				const currentValues = isMultiple ? Array.from(select.selectedOptions).map(opt => opt.value) : [select.value];
				
				select.innerHTML = '';
				
				data.subjects.forEach(subject => {
					const option = document.createElement('option');
					option.value = subject.id;
					option.textContent = `${subject.name} (${subject.abkuerzung})`;
					
					if (currentValues.includes(String(subject.id))) {
						option.selected = true;
					}
					select.appendChild(option);
				});
				
				// Select2 aktualisieren, wenn verfügbar
				if ($(select).data('select2')) {
					$(select).val(currentValues).trigger('change');
				}
				console.log("Dropdown updated:", select);
			});
		})
		.catch(error => {
			console.error("Error updating dropdowns:", error);
		});
}

function showErrorsInForms() {
  const errorForms = document.querySelectorAll('.field-error');
  
  if (errorForms.length === 0) return;
  
  // Für jedes fehlerhafte Formular das übergeordnete details-Element öffnen
  errorForms.forEach(form => {
    const parentDetails = form.closest('details');
    if (parentDetails) {
      parentDetails.setAttribute('open', '');
    }
  });
  // Zur ersten Fehlermeldung scrollen
  const firstError = errorForms[0];
  if (firstError) {
    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

deleteSubjectForm = function(formId) {
  const formElement = document.getElementById(formId);
  const idInput = formElement.querySelector('input[name$="-id"]');
    
  if (idInput && idInput.value) {
    if (!confirm('Möchten Sie dieses Fach wirklich löschen?')) {
      return;
    }
    const payload = {
			id: idInput.value,
			delete: 'delete'
		};

    console.log("Sending delete request with payload:", payload);
    
    addOrUpdateModel('/schedule/create/save-subject/', payload)
    .then(data => {
      if (data.success) {
				console.log(data.message || "Fach erfolgreich gelöscht");
        
        formElement.remove();
        
        const totalForms = document.querySelector('input[name="subject-TOTAL_FORMS"]');
        if (totalForms) {
          totalForms.value = parseInt(totalForms.value) - 1;
        }
        
        updateSubjectDropdowns();
			} else {
				console.log(data.message || "Fehler beim Speichern");
				showSavingStatus(formElement, data.message, "error", 5000);
			}
    })
    .catch(error => {
      console.error("Error deleting subject:", error);
			showSavingStatus(formElement, error, "error", 5000);
    });
	//neue/leere Forms normal löschen
  } else {
    deleteForm(formId);
  }
};

deleteGradeForm = function(formId) {
  const formElement = document.getElementById(formId);
  const idInput = formElement.querySelector('input[name$="-id"]');
    
  if (idInput && idInput.value) {
    if (!confirm('Möchten Sie diese Klassenstufe wirklich löschen?')) {
      return;
    }
    const payload = {
      id: idInput.value,
      delete: 'delete'
    };

    console.log("Sending delete request with payload:", payload);
    
    addOrUpdateModel('/schedule/create/save-grade/', payload)
    .then(data => {
      if (data.success) {
        console.log(data.message || "Klassenstufe erfolgreich gelöscht");
        
        formElement.remove();
        
        const totalForms = document.querySelector('input[name="grade-TOTAL_FORMS"]');
        if (totalForms) {
          totalForms.value = parseInt(totalForms.value) - 1;
        }
      } else {
        console.log(data.message || "Fehler beim Löschen");
        showSavingStatus(formElement, data.message, "error", 5000);
      }
    })
    .catch(error => {
      console.error("Error deleting grade:", error);
			showSavingStatus(formElement, error, "error", 5000);
    });
  } else {
    deleteForm(formId);
  }
};

function setupNewGradeContainers(gradeForm, gradeId) {
  const subjectGradeContainer = document.createElement('div');
  subjectGradeContainer.id = `subject_grade${gradeId}-forms`;
  subjectGradeContainer.innerHTML = `
    <h3>Unterrichtete Fächer</h3>
    <input type="hidden" name="subject_grade${gradeId}-TOTAL_FORMS" value="0" id="id_subject_grade${gradeId}-TOTAL_FORMS">
    <input type="hidden" name="subject_grade${gradeId}-INITIAL_FORMS" value="0" id="id_subject_grade${gradeId}-INITIAL_FORMS">
    <input type="hidden" name="subject_grade${gradeId}-MIN_NUM_FORMS" value="0" id="id_subject_grade${gradeId}-MIN_NUM_FORMS">
    <input type="hidden" name="subject_grade${gradeId}-MAX_NUM_FORMS" value="1000" id="id_subject_grade${gradeId}-MAX_NUM_FORMS">
  `;
  gradeForm.appendChild(subjectGradeContainer);

  const addSubjectGradeButton = document.createElement('button');
  addSubjectGradeButton.type = 'button';
  addSubjectGradeButton.innerHTML = '<i class="fa-solid fa-plus"></i>';
  addSubjectGradeButton.setAttribute('onclick', `addForm('empty-subject_grade-form', 'subject_grade${gradeId}-forms', ${gradeId}, true)`);
  gradeForm.appendChild(addSubjectGradeButton);
  
  const classContainer = document.createElement('div');
  classContainer.id = `class${gradeId}-forms`;
  classContainer.innerHTML = `
    <h3>Klassen</h3>
    <input type="hidden" name="class${gradeId}-TOTAL_FORMS" value="0" id="id_class${gradeId}-TOTAL_FORMS">
    <input type="hidden" name="class${gradeId}-INITIAL_FORMS" value="0" id="id_class${gradeId}-INITIAL_FORMS">
    <input type="hidden" name="class${gradeId}-MIN_NUM_FORMS" value="0" id="id_class${gradeId}-MIN_NUM_FORMS">
    <input type="hidden" name="class${gradeId}-MAX_NUM_FORMS" value="1000" id="id_class${gradeId}-MAX_NUM_FORMS">
  `;
  gradeForm.appendChild(classContainer);
  
  const addClassButton = document.createElement('button');
  addClassButton.type = 'button';
  addClassButton.innerHTML = '<i class="fa-solid fa-plus"></i>';
  addClassButton.setAttribute('onclick', `addForm('empty-class-form', 'class${gradeId}-forms', ${gradeId})`);
  gradeForm.appendChild(addClassButton);

  addForm('empty-class-form', classContainer.id);
  addForm('empty-subject_grade-form', subjectGradeContainer.id, true);
}