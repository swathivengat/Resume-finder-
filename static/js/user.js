
async function uploadResume() {
    const fileInput = document.getElementById("resumeFile");
    const msg = document.getElementById("msg");

    if (!fileInput.files[0]) {
        msg.innerText = "Please select a PDF file first.";
        msg.style.color = "red";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    msg.innerText = "Processing resume...";
    msg.style.color = "blue";

    try {
        const response = await fetch("/upload_resume", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            msg.innerText = "Success: " + data.message;
            msg.style.color = "green";
            fileInput.value = ""; 
        } else {
            msg.innerText = "Error: " + (data.error || "Upload failed");
            msg.style.color = "red";
        }
    } catch (err) {
        console.error("Connection error:", err);
        msg.innerText = "Connection error. Is the server running?";
        msg.style.color = "red";
    }
}