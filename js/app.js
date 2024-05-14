const submitButton = document.getElementById("submit-button");
const chatContainer = document.getElementById("chatContainer");
const questionInput = document.getElementById("question");
const fileInput = document.getElementById("fileInput");
const loader = document.getElementById("loader");
// added commit
submitButton.addEventListener("click", processQuestion);

document.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    processQuestion();
  }
});

async function processQuestion() {
  const question = questionInput.value.trim();

  if (!question) {
    alert("Please ask a question before submitting.");
    return;
  }

  questionInput.value = "";

  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a PDF file to upload.");
    return;
  }

  if (file.type !== "application/pdf") {
    alert("Only PDF files are supported.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    loader.style.display = "block";

    const uploadResponse = await fetch("https://api.chatpdf.com/v1/sources/add-file", {
      method: "POST",
      headers: {
        "x-api-key": "sec_5Q0hNiqKd2PlimXRbOVwGJ2xkCIZ6qSE",
      },
      body: formData,
    });

    if (!uploadResponse.ok) {
      throw new Error(`Error uploading file: ${uploadResponse.statusText}`);
    }

    const uploadData = await uploadResponse.json();
    const sourceId = uploadData.sourceId;

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
