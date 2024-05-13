const submitButton = document.getElementById('submit-button');
const historyContainer = document.querySelector('.chat-container');
const questionInput = document.getElementById('question');
const fileInput = document.getElementById('fileInput');  // Reference the file input

// Function to process the answer and display response
function processAnswer() {
  const question = questionInput.value.trim(); // Trim leading/trailing whitespace

  // Check if input field is empty before processing
  if (!question) {
    alert("Please ask a question before submitting.");
    return; // Exit function if empty
  }

  questionInput.value = ""; // Clear input field

  // Handle file upload and API call before processing question
  handleFileUpload(question);
}

// Function to handle file upload and API call
async function handleFileUpload(question) {
  const file = fileInput.files[0];

  // Check if a file is selected
  if (!file) {
    alert('Please select a PDF file to upload.');
    return;
  }

  // Validate file type (optional)
  if (file.type !== 'application/pdf') {
    alert('Only PDF files are supported.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('https://api.chatpdf.com/v1/sources/add-file', {
      method: 'POST',
      headers: {
        'x-api-key': 'sec_5Q0hNiqKd2PlimXRbOVwGJ2xkCIZ6qSE', 
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Error uploading file: ${response.statusText}`);
    }

    const data = await response.json();
    const sourceId = data.sourceId;  

    
    const answerText = await processQuestionUsingSourceId(sourceId, question);

    
    const userParagraph = document.createElement('p');
    userParagraph.classList.add('user'); 
    userParagraph.textContent = `YOU : ${question}`;

    const responseParagraph = document.createElement('p');
    responseParagraph.classList.add('ai'); 
    responseParagraph.textContent = answerText;

    
    historyContainer.appendChild(userParagraph);
    historyContainer.appendChild(responseParagraph);
    historyContainer.scrollTop = historyContainer.scrollHeight; 
  } catch (error) {
    console.error('Error:', error);
    alert('Error uploading file or processing question.');
  }
}


async function processQuestionUsingSourceId(sourceId, question) {
  const data = {
    'sourceId': sourceId,
    'messages': [
      {
        'role': 'user',
        'content': question,
      }
    ]
  };

  const response = await fetch('https://api.chatpdf.com/v1/chats/message', {
    method: 'POST',
    headers: {
      'x-api-key': 'sec_5Q0hNiqKd2PlimXRbOVwGJ2xkCIZ6qSE', 
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Error processing question: ${response.statusText}`);
  }

  const responseJson = await response.json();
  const content = responseJson.content; 
  
  const answer = `AI : ${content} `;
  return answer;
}

// Event listener for submit button click
submitButton.addEventListener('click', processAnswer);

// Event listener for Enter key press (optional)
document.addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault();
    submitButton.click();
  }
});
