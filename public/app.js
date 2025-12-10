const API_URL = window.location.origin;

const showNotification = (message, type = 'success') => {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
};

const navigateToSection = (sectionName) => {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    document.getElementById(`${sectionName}-section`).classList.add('active');
    document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

    if (sectionName === 'detections') {
        loadDetections();
    } else if (sectionName === 'reports') {
        loadReports();
    }
};

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const section = link.dataset.section;
        navigateToSection(section);
    });
});

const loadMissingPersons = async () => {
    try {
        const response = await fetch(`${API_URL}/api/missing-persons`);
        const result = await response.json();

        const select = document.getElementById('select-person');
        select.innerHTML = '<option value="">Select a person...</option>';

        if (result.success && result.data.length > 0) {
            result.data.forEach(person => {
                const option = document.createElement('option');
                option.value = person.id;
                option.textContent = person.name;
                select.appendChild(option);
            });
        } else {
            select.innerHTML = '<option value="">No persons registered yet</option>';
        }
    } catch (error) {
        console.error('Error loading persons:', error);
        showNotification('Failed to load missing persons', 'error');
    }
};

document.getElementById('reference-image').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.querySelector('.file-upload-placeholder').style.display = 'none';
            document.querySelector('.file-preview').style.display = 'block';
            document.getElementById('ref-image-preview').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('video-upload').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const placeholder = e.target.parentElement.querySelector('.file-upload-placeholder');
        const fileName = e.target.parentElement.querySelector('.file-name');

        placeholder.style.display = 'none';
        fileName.style.display = 'block';
        fileName.textContent = file.name;
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.querySelector('span').textContent;

    submitBtn.disabled = true;
    submitBtn.querySelector('span').textContent = 'Registering...';

    try {
        const response = await fetch(`${API_URL}/api/missing-persons`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            showNotification('Person registered successfully!', 'success');
            e.target.reset();
            document.querySelector('.file-upload-placeholder').style.display = 'flex';
            document.querySelector('.file-preview').style.display = 'none';
            loadMissingPersons();
        } else {
            throw new Error(result.message || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to register person', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.querySelector('span').textContent = originalText;
    }
});

document.getElementById('detect-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const progressContainer = document.getElementById('detection-progress');
    const progressFill = progressContainer.querySelector('.progress-fill');
    const resultSection = document.getElementById('result-section');

    submitBtn.disabled = true;
    progressContainer.style.display = 'block';
    resultSection.style.display = 'none';

    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 5;
        if (progress > 90) progress = 90;
        progressFill.style.width = progress + '%';
    }, 500);

    try {
        const response = await fetch(`${API_URL}/api/detect/video`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        clearInterval(progressInterval);
        progressFill.style.width = '100%';

        setTimeout(() => {
            progressContainer.style.display = 'none';
            resultSection.style.display = 'block';

            const resultContent = document.getElementById('result-content');

            if (result.detected) {
                resultContent.innerHTML = `
                    <div class="result-item">
                        <div>
                            <img src="${API_URL}/${result.data.frame_url}" alt="Detected Frame">
                        </div>
                        <div class="result-details">
                            <h4>Person Detected!</h4>
                            <p><strong>Confidence:</strong> ${(result.data.confidence * 100).toFixed(2)}%</p>
                            <p><strong>Detection ID:</strong> ${result.data.detection_id}</p>
                            <a href="${API_URL}/${result.data.video_url}" class="btn btn-primary" download>
                                <span>Download Processed Video</span>
                            </a>
                        </div>
                    </div>
                `;
                showNotification('Person detected in video!', 'success');
            } else {
                resultContent.innerHTML = `
                    <div style="text-align: center; padding: 48px;">
                        <h3 style="color: var(--warning); margin-bottom: 16px;">Person Not Found</h3>
                        <p style="color: var(--text-secondary);">The person was not detected in the uploaded video.</p>
                    </div>
                `;
                showNotification('Person not found in video', 'warning');
            }

            progressFill.style.width = '0%';
        }, 500);
    } catch (error) {
        clearInterval(progressInterval);
        console.error('Error:', error);
        showNotification('Detection failed', 'error');
        progressContainer.style.display = 'none';
    } finally {
        submitBtn.disabled = false;
    }
});

const loadDetections = async () => {
    const container = document.getElementById('detections-list');
    container.innerHTML = '<div class="loading">Loading detections...</div>';

    try {
        const response = await fetch(`${API_URL}/api/missing-persons`);
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            let allDetections = [];

            for (const person of result.data) {
                const detectionsResponse = await fetch(`${API_URL}/api/detections/${person.id}`);
                const detectionsResult = await detectionsResponse.json();

                if (detectionsResult.success && detectionsResult.data.length > 0) {
                    allDetections = allDetections.concat(
                        detectionsResult.data.map(d => ({ ...d, person_name: person.name }))
                    );
                }
            }

            if (allDetections.length > 0) {
                container.innerHTML = allDetections.map(detection => `
                    <div class="detection-card">
                        <img src="${API_URL}/${detection.frame_url}" alt="Detection">
                        <div class="detection-card-content">
                            <h4>${detection.person_name}</h4>
                            <p><strong>Type:</strong> ${detection.detection_type}</p>
                            <p><strong>Detected:</strong> ${new Date(detection.detected_at).toLocaleString()}</p>
                            <span class="confidence-badge">${(detection.confidence_score * 100).toFixed(1)}% Match</span>
                        </div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<div class="loading">No detections found</div>';
            }
        } else {
            container.innerHTML = '<div class="loading">No detections found</div>';
        }
    } catch (error) {
        console.error('Error loading detections:', error);
        container.innerHTML = '<div class="loading">Failed to load detections</div>';
    }
};

const loadReports = async () => {
    const container = document.getElementById('reports-list');
    container.innerHTML = '<div class="loading">Reports feature coming soon...</div>';
};

loadMissingPersons();
