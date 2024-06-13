document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const parentContainer = document.querySelector('.parent-container');
    const sidebarToggleLeft = document.getElementById('sidebar-toggle-left');
    const sidebarToggleRight = document.getElementById('sidebar-toggle-right');
    const logo = document.querySelector('.logo');
    const logoSmol = document.querySelector('.logo-smol');
    
    // Toggle classes
    const toggleClasses = () => {
        sidebar.classList.toggle('sidebar-minimized');
        parentContainer.classList.toggle('sidebar-minimized');
        logo.classList.toggle('d-none');
        logoSmol.classList.toggle('d-none');
    }

    // Manage sidebar toggle state
    const manageSidebarToggleState = () => {
        if (sidebar.classList.contains('sidebar-minimized')) {
            sidebarToggleLeft.classList.add('d-none');
            sidebarToggleRight.classList.remove('d-none');
            localStorage.setItem('sidebar-minimized', 'true');
        } else {
            sidebarToggleLeft.classList.remove('d-none');
            sidebarToggleRight.classList.add('d-none');
            localStorage.removeItem('sidebar-minimized');
        }
    }

    // Set minimized state
    const setMinimizedState = () => {
        sidebar.classList.add('sidebar-minimized');
        parentContainer.classList.add('sidebar-minimized');
        sidebarToggleLeft.classList.add('d-none');
        sidebarToggleRight.classList.remove('d-none');
        logo.classList.add('d-none');
        logoSmol.classList.remove('d-none');
    }

    sidebarToggle.addEventListener('click', () => {
        toggleClasses();
        manageSidebarToggleState();
    });

    if (localStorage.getItem('sidebar-minimized') === 'true') setMinimizedState();
});

// getCookie function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}