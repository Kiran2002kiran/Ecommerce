document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");
    const usernameInput = document.querySelector("#username");
    const passwordInput = document.querySelector("#password");

    
    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); 

        
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        
        if (!username || !password) {
            alert("Please fill in both fields.");
            return;
        }

        
        fetch(loginForm.action, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"), 
            },
            body: JSON.stringify({ username: username, password: password }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    
                    window.location.href = "/"; 
                } else {
                    
                    alert(data.message || "Invalid credentials. Please try again.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Something went wrong. Please try again.");
            });
    });


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


