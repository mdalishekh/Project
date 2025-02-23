// File handling
const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const apiUrl = 'http://127.0.0.1:8000/api/upload/';

fileInput.addEventListener('change', async function (e) {
    const file = e.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.status) {
                localStorage.setItem('source', result.source);
                displayFilePreview(file);
            } else {
                alert(`Upload failed: ${result.message || 'Unknown error'}`);
            }
        } catch (error) {
            alert(`Error uploading file: ${error.message}`);
        }
    }
});

function displayFilePreview(file) {
    const previewContent = document.createElement('div');
    previewContent.className = 'preview-content';
    
    const fileName = document.createElement('h2');
    fileName.textContent = file.name;
    previewContent.appendChild(fileName);
    
    preview.innerHTML = '';

    if (file.type.startsWith('image/')) {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        previewContent.appendChild(img);
    } else if (file.type === 'text/plain') {
        const reader = new FileReader();
        reader.onload = function (e) {
            const pre = document.createElement('pre');
            pre.textContent = e.target.result;
            previewContent.appendChild(pre);
        };
        reader.readAsText(file);
    } else if (file.type === 'application/pdf') {
        const iframe = document.createElement('iframe');
        iframe.src = URL.createObjectURL(file);
        previewContent.appendChild(iframe);
    } else {
        const unsupported = document.createElement('div');
        unsupported.textContent = `Unsupported file type: ${file.type}`;
        previewContent.appendChild(unsupported);
    }
    
    preview.appendChild(previewContent);
}