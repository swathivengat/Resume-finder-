function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const role = document.querySelector('input[name="role"]:checked').value;
    const msg = document.getElementById("login-msg");

    msg.innerText = "";
    msg.style.color = "red";

    if (!username || !password) {
        msg.innerText = "Please enter username and password.";
        return;
    }

    if (role === "user" && username === "candidate" && password === "candidate@1") {
        msg.style.color = "green";
        msg.innerText = "Login successful!";
        setTimeout(() => {
            window.location.href = "/user";
        }, 700);
        return;
    }

    if (role === "hr" && username === "admin" && password === "admin@1") {
        msg.style.color = "green";
        msg.innerText = "Login successful!";
        setTimeout(() => {
            window.location.href = "/hr";
        }, 700);
        return;
    }

    msg.innerText = "Invalid username or password.";
}