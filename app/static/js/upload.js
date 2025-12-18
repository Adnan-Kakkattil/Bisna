document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Select elements
    const courseSelect = document.getElementById('courseSelect');
    const semesterSelect = document.getElementById('semesterSelect');
    const subjectSelect = document.getElementById('subjectSelect');
    const unitSelect = document.getElementById('unitSelect');
    const topicSelect = document.getElementById('topicSelect'); // This is the actual form field name="topic"

    const selects = {
        'course': courseSelect,
        'semester': semesterSelect,
        'subject': subjectSelect,
        'unit': unitSelect,
        'topic': topicSelect
    };

    // Initial load
    fetchData('/api/courses', courseSelect);

    // Event Listeners for changes
    courseSelect.addEventListener('change', () => {
        resetSelects(['semester', 'subject', 'unit', 'topic']);
        if (courseSelect.value) {
            fetchData(`/api/courses/${courseSelect.value}/semesters`, semesterSelect);
        }
    });

    semesterSelect.addEventListener('change', () => {
        resetSelects(['subject', 'unit', 'topic']);
        if (semesterSelect.value) {
            fetchData(`/api/semesters/${semesterSelect.value}/subjects`, subjectSelect);
        }
    });

    subjectSelect.addEventListener('change', () => {
        resetSelects(['unit', 'topic']);
        if (subjectSelect.value) {
            fetchData(`/api/subjects/${subjectSelect.value}/units`, unitSelect);
        }
    });

    unitSelect.addEventListener('change', () => {
        resetSelects(['topic']);
        if (unitSelect.value) {
            fetchData(`/api/units/${unitSelect.value}/topics`, topicSelect);
        }
    });


    // Helper Functions
    function fetchData(url, selectElement) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                selectElement.innerHTML = '<option value="">Select...</option>';
                data.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    option.textContent = item.name;
                    selectElement.appendChild(option);
                });
                selectElement.disabled = false;
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    function resetSelects(keys) {
        keys.forEach(key => {
            const select = selects[key];
            select.innerHTML = '<option value="">Select...</option>';
            select.disabled = true;
        });
    }

    // Modal Form Handling
    handleModalForm('saveCourseBtn', '/api/courses', () => ({ name: document.getElementById('newCourseName').value }));

    handleModalForm('saveSemesterBtn', '/api/semesters', () => ({
        name: document.getElementById('newSemesterName').value,
        course_id: courseSelect.value
    }), () => {
        // Refresh semester list after adding
        fetchData(`/api/courses/${courseSelect.value}/semesters`, semesterSelect);
    });

    handleModalForm('saveSubjectBtn', '/api/subjects', () => ({
        name: document.getElementById('newSubjectName').value,
        semester_id: semesterSelect.value
    }), () => {
        fetchData(`/api/semesters/${semesterSelect.value}/subjects`, subjectSelect);
    });

    handleModalForm('saveUnitBtn', '/api/units', () => ({
        name: document.getElementById('newUnitName').value,
        subject_id: subjectSelect.value
    }), () => {
        fetchData(`/api/subjects/${subjectSelect.value}/units`, unitSelect);
    });

    handleModalForm('saveTopicBtn', '/api/topics', () => ({
        name: document.getElementById('newTopicName').value,
        unit_id: unitSelect.value
    }), () => {
        fetchData(`/api/units/${unitSelect.value}/topics`, topicSelect);
    });


    function handleModalForm(btnId, url, dataCallback, successCallback) {
        document.getElementById(btnId).addEventListener('click', function () {
            const data = dataCallback();

            // Basic client-side check
            for (let key in data) {
                if (!data[key]) {
                    alert('Please select parent items and fill the name.');
                    return;
                }
            }

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(result => {
                    // Close modal (using generic bootstrap logic)
                    const modalEl = document.getElementById(btnId).closest('.modal');
                    const modalInstance = bootstrap.Modal.getInstance(modalEl);
                    modalInstance.hide();

                    // Clear input
                    modalEl.querySelector('input[type="text"]').value = '';

                    // Refresh lists or auto-select
                    if (successCallback) {
                        successCallback();
                    } else if (url === '/api/courses') {
                        // Special case for top level
                        fetchData('/api/courses', courseSelect);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to save item.');
                });
        });
    }
});
