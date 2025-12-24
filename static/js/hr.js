async function matchResume() {
    const jobDescValue = document.getElementById("jobDesc").value;
    const resultList = document.getElementById("result-list");

    if (!jobDescValue.trim()) {
        alert("Please enter a job description first.");
        return;
    }

    resultList.innerHTML = "<li>Analyzing resumes...</li>";

    try {
        const response = await fetch("/match_resume", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ description: jobDescValue })
        });

        const data = await response.json();
        resultList.innerHTML = "";

        if (data.matches && data.matches.length > 0) {
            data.matches.forEach(item => {
                const li = document.createElement("li");
                li.className = "result-card";

                li.innerHTML = `
                    <h4>${item.resume_name}</h4>
                    <div class="score">${item.match_score}% Match</div>

                    <div class="skills">
                        <p><strong>Matched Skills:</strong>
                        ${item.matched_skills && item.matched_skills.length
                            ? item.matched_skills.join(", ")
                            : "None"}
                        </p>

                        <p><strong>Missing Skills:</strong>
                        ${item.missing_skills && item.missing_skills.length
                            ? item.missing_skills.join(", ")
                            : "None"}
                        </p>
                    </div>
                `;
                resultList.appendChild(li);
            });
        } else {
            resultList.innerHTML = `<li>No matching resumes found.</li>`;
        }

    } catch (err) {
        console.error(err);
        resultList.innerHTML = "<li>Error connecting to server.</li>";
    }
}
