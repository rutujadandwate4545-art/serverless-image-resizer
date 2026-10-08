const API_URL =
    "https://tnb6qmmsi2.execute-api.ap-south-1.amazonaws.com/upload";

const imageInput = document.getElementById("imageInput");
const uploadBtn = document.getElementById("uploadBtn");
const statusText = document.getElementById("status");

uploadBtn.addEventListener("click", async (event) => {

    event.preventDefault();

    const file = imageInput.files[0];

    if (!file) {
        statusText.textContent = "Please select an image first.";
        return;
    }

    uploadBtn.disabled = true;
    statusText.textContent = "Preparing upload...";

    try {
        const response = await fetch(API_URL, {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error("API request failed: " + response.status);
        }

        const data = await response.json();

        statusText.textContent = "Uploading image...";

        const uploadResponse = await fetch(data.upload_url, {
            method: "PUT",
            headers: {
                "Content-Type": "image/jpeg"
            },
            body: file
        });

        if (!uploadResponse.ok) {
            throw new Error("S3 upload failed: " + uploadResponse.status);
        }

        statusText.textContent =
            "✅ Image uploaded successfully! Resizing...";

    } catch (error) {
        console.error(error);
        statusText.textContent =
            "❌ " + error.message;
    } finally {
        uploadBtn.disabled = false;
    }
});