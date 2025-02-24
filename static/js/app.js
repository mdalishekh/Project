// Clearing all my local storage when loading page
window.onload = function () {
    localStorage.clear();
};

// File handling
const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const apiUrl = 'api/upload/';
const chatApiUrl = 'api/get-answer/';

let isFileUploaded = false; // Track file upload status

 // Chat elements
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const chatMessages = document.getElementById('chat-messages');
const sendButton = document.getElementById('send-button');


// Enable send button only when input has text
messageInput.addEventListener('input', function () {
    sendButton.disabled = messageInput.value.trim() === '';
});


// Function to add message to chat panel
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);

    // Auto-scroll to the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
// File upload logic
fileInput.addEventListener('change', async function (e) {
    const file = e.target.files[0];
    if (!file) return;

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            console.log("Trying to upload file...");
            localStorage.clear();
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.status) {
                isFileUploaded = true;
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


// Function to display file preview
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
    } else if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        const docxInfo = document.createElement('div');
        docxInfo.innerHTML = `
            <p>DOCX preview not available</p>
            <a href="${URL.createObjectURL(file)}" download="${file.name}">
                Download DOCX file
            </a>
        `;
        previewContent.appendChild(docxInfo);
    } else {
        const unsupported = document.createElement('div');
        unsupported.textContent = `Unsupported file type: ${file.type}`;
        previewContent.appendChild(unsupported);
    }

    preview.appendChild(previewContent);
}

// Handle chat form submission
chatForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!isFileUploaded) {
        alert("Please upload a file before chatting.");
        return;
    }
    const userMessage = messageInput.value.trim();
    if (userMessage === '') return;

    if (chatMessages.textContent.trim() === "No messages yet") {
        chatMessages.innerHTML = '';
    }

    // Display user message
    addMessage(userMessage, 'user');

    // Prepare request data
    const requestData = {
        question: userMessage,
        source: localStorage.getItem('source') || '' // Get source from localStorage
    };

    try {
        // Send user message to the REST API
        const response = await fetch(chatApiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        });

        const result = await response.json();

        // Display AI response
        if (response.ok && result.status) {
            addMessage(result.answer, 'ai');
        } else {
            addMessage("Failed to get an answer. Try again.", 'ai');
        }
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'ai');
    }

    // Clear input field
    messageInput.value = '';
    sendButton.disabled = true;
});


