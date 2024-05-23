const submitButton = document.getElementById("submit-button");
const chatContainer = document.getElementById("chatContainer");
const questionInput = document.getElementById("question");
const fileInput = document.getElementById("fileInput");
const loader = document.getElementById("loader");
const blob = document.querySelector('.blob');
const fileNameDisplay = document.getElementById('fileName');

let isFileUploadInProgress = false; // Flag to track whether file upload is in progress
let sourceId = null; // Variable to store the sourceId

async function fileUpload() {
  // If file upload is already in progress, return
  if (isFileUploadInProgress) {
    console.log("File upload already in progress");
    return;
  }

  console.log("Started");
  const file = fileInput.files[0];

  if (!file) {
    console.log("No file selected");
    return;
  }

  console.log("File Found");
  
  if (file.type !== "application/pdf") {
    alert("Only PDF files are supported.");
    return;
  }

  fileNameDisplay.textContent = `${file.name}`;

  const formData = new FormData();
  formData.append("file", file);

  try {
    console.log("Trying to send file in API");
    
    isFileUploadInProgress = true; // Set flag to true indicating file upload is in progress
    blob.style.display = 'block';

    const uploadResponse = await fetch("https://api.chatpdf.com/v1/sources/add-file", {
      method: "POST",
      headers: {
        "x-api-key": "sec_5Q0hNiqKd2PlimXRbOVwGJ2xkCIZ6qSE",
      },
      body: formData,
    });

    blob.style.display = 'none';
    
    console.log("File uploaded");

    if (!uploadResponse.ok) {
      throw new Error(`Error uploading file: ${uploadResponse.statusText}`);
    }

    const uploadData = await uploadResponse.json();
    sourceId = uploadData.sourceId; // Set the sourceId
    console.log("Source Id ==>", sourceId);

    return sourceId; // Return the sourceId

  } catch (error) {
    console.error("Error:", error);
    alert("Error uploading file.");
  } finally {
    blob.style.display = "none";
    isFileUploadInProgress = false; // Reset the flag to false after file upload completes
  }
}

fileInput.addEventListener('change', async () => {
  sourceId = await fileUpload();
});

async function processQuestion() {
  const question = questionInput.value.trim();

  if (!question) {
    alert("Please ask a question before submitting.");
    return;
  }

  questionInput.value = "";

  if (!sourceId) {
    const file = fileInput.files[0];
    if (!file) {
      alert("Please select a PDF file to upload.");
      return;
    }

    if (file.type !== "application/pdf") {
      alert("Only PDF files are supported.");
      return;
    }

    fileNameDisplay.textContent = `${file.name}`;
    sourceId = await fileUpload(); // Upload the file and get the sourceId
  }

  if (!sourceId) {
    alert("Error obtaining source ID.");
    return;
  }

  loader.style.display = "block";

  try {
    const questionParagraph = document.createElement("p");
    questionParagraph.classList.add("user");
    questionParagraph.textContent = `YOU: ${question}`;
    chatContainer.appendChild(questionParagraph);

    const answer = await getAnswer(sourceId, question);

    const answerParagraph = document.createElement("p");
    answerParagraph.classList.add("ai");
    answerParagraph.textContent = `AI: ${answer}`;
    chatContainer.appendChild(answerParagraph);

    chatContainer.scrollTop = chatContainer.scrollHeight;
  } catch (error) {
    console.error("Error:", error);
    alert("Error uploading file or processing question.");
  } finally {
    loader.style.display = "none";
    // Ensure the blob animation is hidden in case of error
    blob.style.display = "none";
  }
}

async function getAnswer(sourceId, question) {
  const requestData = {
    sourceId: sourceId,
    messages: [
      {
        role: "user",
        content: question,
      },
    ],
  };

  const response = await fetch("https://api.chatpdf.com/v1/chats/message", {
    method: "POST",
    headers: {
      "x-api-key": "sec_5Q0hNiqKd2PlimXRbOVwGJ2xkCIZ6qSE",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  });

  if (!response.ok) {
    throw new Error(`Error processing question: ${response.statusText}`);
  }

  const responseData = await response.json();
  return responseData.content;
}

submitButton.addEventListener("click", processQuestion);

document.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    processQuestion();
  }
});
