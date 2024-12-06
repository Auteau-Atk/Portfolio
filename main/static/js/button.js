// scripts.js
document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const addProjectBtn = document.getElementById('add-project-btn');
    const projectList = document.getElementById('project-list');

    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            fetch('/logout', { method: 'POST' })
                .then(() => {
                    alert('Logged out successfully!');
                    window.location.reload();
                });
        });
    }

    if (addProjectBtn) {
        addProjectBtn.addEventListener('click', () => {
            const projectName = prompt('Enter the project name:');
            const projectDetails = prompt('Enter the project details:');
            if (projectName && projectDetails) {
                fetch('/add_project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: projectName, details: projectDetails })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    window.location.reload();
                });
            }
        });
    }

    document.querySelectorAll('.remove-project-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const projectName = e.target.dataset.name;
            fetch('/remove_project', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: projectName })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.reload();
            });
        });
    });
});
