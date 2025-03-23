$(document).ready(function() {
	//select2 für alle sichtbaren select2-Elemente 
	let selection = Array.from(document.querySelectorAll('.django-select2'))
		.filter(sel => sel.offsetParent !== null);
	initSelect2(selection);

	hideDeleteCheckboxes();
	filterEmptyForms();

	//setupGradeAutoSave();
  setupSubjectAutoSave();
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

// Diese Funktionen müssen ein Promise zurückgeben
function addOrUpdateModel(url, payload) {
  return fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/json" // Wichtig für JSON-Daten
    },
    body: JSON.stringify({payload: payload})
  })
  .then(response => {
    return response.json();
  });
}

function getModelData(url) {
  return fetch(url, {
    method: "GET",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
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
  // Event-Listener für alle bestehenden Subject-Formulare
  setupSubjectFormListeners();
  
  // Wenn neue Subject-Formulare hinzugefügt werden
  const originalAddForm = addForm;
  addForm = function(templateId, targetId, select2 = false) {
    const container = originalAddForm(templateId, targetId, select2);
    if (templateId === 'empty-subject-form') {
      setupSubjectFormListener(container);
    }
    return container;
  };
}

function setupSubjectFormListeners() {
  document.querySelectorAll('.subject-form').forEach((form) => {
    setupSubjectFormListener(form);
  });
}

function setupSubjectFormListener(form) {
  // Relevant für Subjects sind name und abkuerzung
  const nameField = form.querySelector('input[name$="-name"]');
  const abkuerzungField = form.querySelector('input[name$="-abkuerzung"]');
  
  if (!nameField || !abkuerzungField) return;
  
  // Timer für verzögerte Speicherung
  let saveTimer = null;
  
  // Event-Listener für Input-Änderungen
  [nameField, abkuerzungField].forEach(field => {
    field.addEventListener('input', () => {
      // Status-Anzeige hinzufügen
      showSavingStatus(form, "Änderungen werden gespeichert...");
      
      // Lösche vorherigen Timer, um zu häufige API-Anfragen zu vermeiden
      if (saveTimer) clearTimeout(saveTimer);
      
      // Setze neuen Timer für verzögerte Speicherung (nur wenn beide Felder Werte haben)
      saveTimer = setTimeout(() => {
        if (nameField.value && abkuerzungField.value) {
          saveSubject(form);
        }
      }, 1500); // Verzögerung von 1,5 Sekunden
    });
    
    // Beim Verlassen des Feldes sofort speichern
    field.addEventListener('blur', () => {
      // Falls Timer noch läuft, abbrechen
      if (saveTimer) {
        clearTimeout(saveTimer);
        saveTimer = null;
      }
      
      // Nur speichern, wenn beide Felder ausgefüllt sind
      if (nameField.value && abkuerzungField.value) {
        saveSubject(form);
      } else if (nameField.value || abkuerzungField.value) {
        // Falls nur ein Feld ausgefüllt ist, Hinweis anzeigen
        showValidationError(form, "Bitte sowohl Namen als auch Abkürzung angeben.");
      }
    });
  });
}

function saveSubject(form) {
  // Formular-Daten sammeln
  const idField = form.querySelector('input[name$="-id"]');
  const nameField = form.querySelector('input[name$="-name"]');
  const abkuerzungField = form.querySelector('input[name$="-abkuerzung"]');
  
  const subjectData = {
    id: idField ? idField.value : '',
    name: nameField.value,
    abkuerzung: abkuerzungField.value
  };
  
  // Status aktualisieren
  showSavingStatus(form, "Wird gespeichert...");
  
  // Die addOrUpdateModel-Funktion verwenden
  addOrUpdateModel('/schedule/create/save-subject/', subjectData)
    .then(data => {
      if (data.success) {
        // Erfolgreich gespeichert
        if (idField && !idField.value) {
          // Bei neuen Formularen die ID aktualisieren
          idField.value = data.subject_id;
        }
        
        // Feedback anzeigen
        showSavingStatus(form, "✓ Gespeichert", "success");
        
        // Update Select2 Dropdowns mit dem neuen/aktualisierten Subject
        updateSubjectDropdowns();
        
        // Status nach 2 Sekunden entfernen
        setTimeout(() => {
          clearSavingStatus(form);
        }, 2000);
      } else {
        // Fehler anzeigen
        showValidationError(form, data.message || "Fehler beim Speichern");
      }
    })
    .catch(error => {
      console.error("Error saving subject:", error);
      showValidationError(form, "Netzwerkfehler beim Speichern");
    });
}

// Hilfsfunktionen für die Benutzeroberfläche
function showSavingStatus(form, message, type = "info") {
  let statusEl = form.querySelector('.saving-status');
  if (!statusEl) {
    statusEl = document.createElement('div');
    statusEl.className = 'saving-status';
    form.appendChild(statusEl);
  }
  
  statusEl.textContent = message;
  statusEl.className = `saving-status status-${type}`;
}

function clearSavingStatus(form) {
  const statusEl = form.querySelector('.saving-status');
  if (statusEl) {
    statusEl.remove();
  }
}

function showValidationError(form, message) {
  showSavingStatus(form, message, "error");
  
  // Nach 3 Sekunden ausblenden
  setTimeout(() => {
    clearSavingStatus(form);
  }, 3000);
}

// Funktion zum Aktualisieren aller Subject-Dropdowns
// Ersetze die komplette updateSubjectDropdowns-Funktion:

function updateSubjectDropdowns() {
  console.log("Updating subject dropdowns...");
  
  // AJAX-Anfrage, um alle aktualisierten Subjects zu holen
  getModelData('/schedule/create/get-subjects/')
    .then(data => {
      if (!data.success) {
        console.error("Failed to get subjects");
        return;
      }
      
      console.log(`Got ${data.subjects.length} subjects from server`);
      
      // Finde alle relevanten Selects (sowohl normale als auch multiple)
      const selects = document.querySelectorAll(
        'select[name$="-subject"], ' +       // Normale Subjects mit -subject am Ende
        'select[name="subjects"], ' +        // Explizites "subjects" Feld
        'select[multiple][name*="subject"], ' + // Multiple selects mit "subject" im Namen
        '.teacher-form select'               // Alle Selects in Lehrer-Formularen
      );
      
      console.log(`Found ${selects.length} subject-related select elements`);
      
      // Debug: Alle gefundenen Selects anzeigen
      selects.forEach((select, index) => {
        console.log(`Select #${index}:`, {
          element: select,
          name: select.name,
          id: select.id || 'no-id',
          multiple: select.multiple,
          className: select.className,
          optionsCount: select.options.length,
          isTeacherForm: select.closest('.teacher-form') ? true : false,
          isSelect2: window.jQuery && (
            $(select).hasClass('django-select2') || 
            $(select).data('select2')
          ) ? true : false
        });
      });
      
      // Für jedes Select-Element
      selects.forEach(select => {
        // Die aktuelle Auswahl speichern 
        const isMultiple = select.multiple;
        let currentValues = [];
        
        if (isMultiple) {
          // Multiple-Select: Werte als Array speichern
          currentValues = Array.from(select.selectedOptions).map(opt => opt.value);
          console.log(`Multiple select ${select.name}: Current values = [${currentValues.join(', ')}]`);
        } else {
          // Single-Select: Wert als String speichern
          currentValues = [select.value];
          console.log(`Single select ${select.name}: Current value = ${select.value}`);
        }
        
        // Alte Optionen entfernen
        select.innerHTML = '';
        
        // Leere Option für Single-Selects hinzufügen
        if (!isMultiple) {
          const emptyOption = document.createElement('option');
          emptyOption.value = '';
          emptyOption.textContent = '--------';
          select.appendChild(emptyOption);
        }
        
        // Subject-Optionen hinzufügen
        data.subjects.forEach(subject => {
          const option = document.createElement('option');
          option.value = subject.id;
          option.textContent = `${subject.name} (${subject.abkuerzung})`;
          
          // Option als ausgewählt markieren, wenn sie im currentValues-Array ist
          if (currentValues.includes(subject.id.toString())) {
            option.selected = true;
          }
          
          select.appendChild(option);
        });
        
        // Select2 aktualisieren, wenn es eins ist
        if (window.jQuery) {
          if ($(select).hasClass('django-select2') || $(select).data('select2')) {
            console.log(`Triggering change for Select2 ${select.name}`);
            
            // Bei multiple-select manchmal Probleme - erzwinge komplettes Neu-Rendern
            if (isMultiple) {
              // Versuche direkt die Werte mit select2 zu setzen
              try {
                $(select).val(currentValues).trigger('change');
              } catch (e) {
                console.warn('Error setting values via Select2:', e);
                
                // Fallback-Methode
                currentValues.forEach(value => {
                  const option = select.querySelector(`option[value="${value}"]`);
                  if (option) option.selected = true;
                });
                $(select).trigger('change');
              }
            } else {
              // Für single-select reicht meistens ein trigger
              $(select).trigger('change');
            }
          }
        }
      });
      
      console.log("Dropdowns update completed");
    })
    .catch(error => {
      console.error("Error updating dropdowns:", error);
    });
}