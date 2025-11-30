// Auto-detect API base URL - works for both local and Vercel deployment
const getApiBase = () => {
    // Check if we're on Vercel (production)
    if (window.location.hostname.includes('vercel.app') || window.location.hostname.includes('vercel.com')) {
        return `${window.location.origin}/api/auth`;
    }
    // Local development
    return `${window.location.origin}/auth`;
};

const API_BASE = getApiBase();

// Toast Notification System
class ToastManager {
    constructor() {
        this.container = this.createContainer();
        this.toasts = new Map();
    }

    createContainer() {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 5000) {
        const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const toast = this.createToast(message, type, toastId);
        
        this.container.appendChild(toast);
        this.toasts.set(toastId, toast);

        // Auto remove
        if (duration > 0) {
            setTimeout(() => {
                this.remove(toastId);
            }, duration);
        }

        return toastId;
    }

    createToast(message, type, id) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.id = id;

        const icons = {
            success: '✓',
            error: '✕',
            info: 'ℹ',
            warning: '⚠'
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <div class="toast-content">
                <div class="toast-message">${escapeHtml(message)}</div>
            </div>
            <button class="toast-close" onclick="toastManager.remove('${id}')" aria-label="Close">×</button>
        `;

        return toast;
    }

    remove(toastId) {
        const toast = this.toasts.get(toastId);
        if (toast) {
            toast.classList.add('hiding');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
                this.toasts.delete(toastId);
            }, 300);
        }
    }

    success(message, duration = 4000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 6000) {
        return this.show(message, 'error', duration);
    }

    info(message, duration = 4000) {
        return this.show(message, 'info', duration);
    }

    warning(message, duration = 5000) {
        return this.show(message, 'warning', duration);
    }
}

// Initialize toast manager
const toastManager = new ToastManager();

// Utility functions - now using toast notifications
function showError(message) {
    toastManager.error(message);
    console.error('Error:', message);
}

function showSuccess(message) {
    toastManager.success(message);
}

function showInfo(message) {
    toastManager.info(message);
}

function showWarning(message) {
    toastManager.warning(message);
}

function hideError() {
    // Legacy support - toasts auto-dismiss
}

// Check authentication
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE}/feed`, {
            credentials: 'include'
        });
        return response.ok;
    } catch (error) {
        return false;
    }
}

// Login
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = '/feed-page';
            } else {
                showError(data.detail || 'Login failed');
            }
        } catch (error) {
            showError('Network error. Please try again.');
        }
    });
}

// Register
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;

        try {
            const response = await fetch(`${API_BASE}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, email, password, role })
            });

            const data = await response.json();

            if (response.ok) {
                showSuccess('Registration successful! Redirecting to login...');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 1500);
            } else {
                const errorMsg = Array.isArray(data.detail) 
                    ? data.detail.map(d => d.msg || d).join(', ')
                    : (data.detail || 'Registration failed');
                showError(errorMsg);
            }
        } catch (error) {
            console.error('Registration error:', error);
            showError('Network error. Please make sure the server is running.');
        }
    });
}

// Logout
if (document.getElementById('logoutBtn')) {
    document.getElementById('logoutBtn').addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_BASE}/logout`, {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                window.location.href = '/';
            }
        } catch (error) {
            showError('Logout failed');
        }
    });
}

// Load and display posts
async function loadPosts() {
    const container = document.getElementById('postsContainer');
    if (!container) return;

    container.innerHTML = '<div class="loading">Loading posts...</div>';

    try {
        const response = await fetch(`${API_BASE}/feed`, {
            credentials: 'include'
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            throw new Error('Failed to load posts');
        }

        const posts = await response.json();

        if (posts.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>No posts yet</h3>
                    <p>Be the first to share something!</p>
                </div>
            `;
            return;
        }

        // Get current user's posts to show delete button
        let userPosts = [];
        try {
            const userPostsResponse = await fetch(`${API_BASE}/get-post`, {
                credentials: 'include'
            });
            if (userPostsResponse.ok) {
                userPosts = await userPostsResponse.json();
                userPosts = userPosts.map(p => p.id);
            }
        } catch (error) {
            console.error('Failed to get user posts');
        }

        container.innerHTML = posts.map(post => {
            const canDelete = userPosts.includes(post.id);
            return `
            <div class="post-card" data-post-id="${post.id}">
                <div class="post-header">
                    <span class="post-author">@${post.author}</span>
                    ${canDelete ? `
                    <div class="post-actions">
                        <button class="btn btn-danger btn-small delete-post" data-id="${post.id}">Delete</button>
                    </div>
                    ` : ''}
                </div>
                <h3 class="post-title">${escapeHtml(post.title)}</h3>
                <p class="post-content">${escapeHtml(post.content)}</p>
            </div>
        `;
        }).join('');

        // Add delete event listeners
        document.querySelectorAll('.delete-post').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const postId = e.target.getAttribute('data-id');
                if (confirm('Are you sure you want to delete this post?')) {
                    await deletePost(postId);
                }
            });
        });

    } catch (error) {
        container.innerHTML = `
            <div class="error-message show">
                Failed to load posts. Please refresh the page.
            </div>
        `;
    }
}

// Create post
if (document.getElementById('postForm')) {
    document.getElementById('postForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();

        const title = document.getElementById('postTitle').value;
        const content = document.getElementById('postContent').value;

        try {
            const response = await fetch(`${API_BASE}/post_upload`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ title, content })
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById('postForm').reset();
                loadPosts();
            } else {
                if (response.status === 401) {
                    window.location.href = '/login';
                } else {
                    showError(data.detail || 'Failed to create post');
                }
            }
        } catch (error) {
            showError('Network error. Please try again.');
        }
    });
}

// Delete post
async function deletePost(postId) {
    try {
        const response = await fetch(`${API_BASE}/post/${postId}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            showSuccess('Post deleted successfully!');
            loadPosts();
        } else {
            if (response.status === 401) {
                showError('Please login to delete posts');
                setTimeout(() => window.location.href = '/login', 1500);
            } else {
                showError('Failed to delete post');
            }
        }
    } catch (error) {
        showError('Network error. Please try again.');
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load posts on feed page
if (document.getElementById('postsContainer')) {
    // Test connection on page load
    console.log('API Base URL:', API_BASE);
    loadPosts();
    // Refresh posts every 30 seconds
    setInterval(loadPosts, 30000);
}

// Admin Panel Functionality
if (document.getElementById('usersTableBody')) {
    // Load users on page load
    loadUsers();
    
    // Admin sidebar navigation
    document.querySelectorAll('.admin-menu-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.getAttribute('data-section');
            
            // Update active state
            document.querySelectorAll('.admin-menu-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Show/hide sections
            document.querySelectorAll('.admin-section').forEach(s => s.style.display = 'none');
            if (section === 'users') {
                document.getElementById('usersSection').style.display = 'block';
            } else if (section === 'update') {
                document.getElementById('updateSection').style.display = 'block';
            }
        });
    });
    
    // Refresh users button
    if (document.getElementById('refreshUsersBtn')) {
        document.getElementById('refreshUsersBtn').addEventListener('click', loadUsers);
    }
    
    // Search user
    if (document.getElementById('searchUserBtn')) {
        document.getElementById('searchUserBtn').addEventListener('click', searchUser);
    }
    
    // Update user form
    if (document.getElementById('updateUserForm')) {
        document.getElementById('updateUserForm').addEventListener('submit', updateUser);
    }
    
    // Clear form
    if (document.getElementById('clearFormBtn')) {
        document.getElementById('clearFormBtn').addEventListener('click', () => {
            document.getElementById('updateUserForm').reset();
            document.getElementById('userInfoCard').style.display = 'none';
            document.getElementById('searchUsername').value = '';
        });
    }
}

// Load all users
async function loadUsers() {
    const tbody = document.getElementById('usersTableBody');
    const statsContainer = document.getElementById('usersStats');
    
    if (!tbody) return;
    
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem;"><div class="loading-spinner"></div><p style="margin-top: 1rem;">Loading users...</p></td></tr>';
    
    try {
        const response = await fetch(`${API_BASE}/admin/users`, {
            credentials: 'include'
        });
        
        if (response.status === 401 || response.status === 403) {
            window.location.href = '/login';
            return;
        }
        
        if (!response.ok) {
            throw new Error('Failed to load users');
        }
        
        const users = await response.json();
        
        // Update stats
        const totalUsers = users.length;
        const adminCount = users.filter(u => u.role === 'admin').length;
        const userCount = users.filter(u => u.role === 'user').length;
        
        statsContainer.innerHTML = `
            <div class="stat-card">
                <div class="stat-value">${totalUsers}</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${adminCount}</div>
                <div class="stat-label">Admins</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${userCount}</div>
                <div class="stat-label">Regular Users</div>
            </div>
        `;
        
        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem;">No users found</td></tr>';
            return;
        }
        
        // Desktop table
        tbody.innerHTML = users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td><strong>${escapeHtml(user.username)}</strong></td>
                <td>${escapeHtml(user.email)}</td>
                <td><span class="badge ${user.role === 'admin' ? 'badge-danger' : 'badge-primary'}">${user.role}</span></td>
                <td>
                    <button class="btn btn-sm btn-secondary" onclick="fillUpdateForm('${escapeHtml(user.username)}')">Edit</button>
                </td>
            </tr>
        `).join('');
        
        // Mobile cards
        updateMobileCards(users, tableContainer);
        
    } catch (error) {
        console.error('Error loading users:', error);
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem; color: var(--danger);">Failed to load users</td></tr>';
    }
}

// Search user
async function searchUser() {
    const username = document.getElementById('searchUsername').value.trim();
    if (!username) {
        showError('Please enter a username');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/admin/user/${encodeURIComponent(username)}`, {
            credentials: 'include'
        });
        
        if (response.status === 401 || response.status === 403) {
            window.location.href = '/login';
            return;
        }
        
        if (response.status === 404) {
            showError('User not found');
            document.getElementById('userInfoCard').style.display = 'none';
            return;
        }
        
        if (!response.ok) {
            throw new Error('Failed to fetch user');
        }
        
        const user = await response.json();
        
        // Display user info
        document.getElementById('currentUserInfo').innerHTML = `
            <p><strong>ID:</strong> ${user.id}</p>
            <p><strong>Username:</strong> ${escapeHtml(user.username)}</p>
            <p><strong>Email:</strong> ${escapeHtml(user.email)}</p>
            <p><strong>Role:</strong> <span class="badge ${user.role === 'admin' ? 'badge-danger' : 'badge-primary'}">${user.role}</span></p>
        `;
        
        // Fill form
        document.getElementById('updateUsername').value = user.username;
        document.getElementById('updateEmail').value = user.email;
        document.getElementById('updateRole').value = user.role;
        document.getElementById('updatePassword').value = '';
        
        document.getElementById('userInfoCard').style.display = 'block';
        hideError();
        
    } catch (error) {
        console.error('Error searching user:', error);
        showError('Failed to search user');
    }
}

// Fill update form from table
window.fillUpdateForm = function(username) {
    document.getElementById('searchUsername').value = username;
    searchUser();
    // Switch to update section
    document.querySelectorAll('.admin-menu-link').forEach(l => l.classList.remove('active'));
    document.querySelector('[data-section="update"]').classList.add('active');
    document.querySelectorAll('.admin-section').forEach(s => s.style.display = 'none');
    document.getElementById('updateSection').style.display = 'block';
};

// Update user
async function updateUser(e) {
    e.preventDefault();
    hideError();
    
    const username = document.getElementById('searchUsername').value.trim();
    if (!username) {
        showError('Please search for a user first');
        return;
    }
    
    const updateData = {
        username: document.getElementById('updateUsername').value.trim() || null,
        email: document.getElementById('updateEmail').value.trim() || null,
        password: document.getElementById('updatePassword').value.trim() || null,
        role: document.getElementById('updateRole').value || null
    };
    
    // Remove null values
    Object.keys(updateData).forEach(key => {
        if (updateData[key] === null || updateData[key] === '') {
            delete updateData[key];
        }
    });
    
    if (Object.keys(updateData).length === 0) {
        showError('Please fill at least one field to update');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/admin/update/${encodeURIComponent(username)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(updateData)
        });
        
        if (response.status === 401 || response.status === 403) {
            window.location.href = '/login';
            return;
        }
        
        const data = await response.json();
        
        if (response.ok) {
            showSuccess('User updated successfully!');
            // Refresh users list
            loadUsers();
            // Refresh current user info
            setTimeout(() => searchUser(), 1000);
        } else {
            showError(data.detail || 'Failed to update user');
        }
    } catch (error) {
        console.error('Error updating user:', error);
        showError('Network error. Please try again.');
    }
}

// Update mobile cards for responsive display
function updateMobileCards(users, tableContainer) {
    if (!tableContainer) return;
    
    const isMobile = window.innerWidth <= 768;
    const existingMobileCards = tableContainer.querySelectorAll('.table-mobile-card');
    
    if (isMobile) {
        // Remove existing mobile cards
        existingMobileCards.forEach(card => card.remove());
        
        // Create mobile cards
        const mobileCards = users.map(user => `
            <div class="table-mobile-card">
                <div class="table-mobile-card-header">
                    <div class="table-mobile-card-title">${escapeHtml(user.username)}</div>
                    <span class="badge ${user.role === 'admin' ? 'badge-danger' : 'badge-primary'}">${user.role}</span>
                </div>
                <div class="table-mobile-card-body">
                    <div class="table-mobile-card-row">
                        <div class="table-mobile-card-label">ID:</div>
                        <div class="table-mobile-card-value">${user.id}</div>
                    </div>
                    <div class="table-mobile-card-row">
                        <div class="table-mobile-card-label">Email:</div>
                        <div class="table-mobile-card-value">${escapeHtml(user.email)}</div>
                    </div>
                    <div class="table-mobile-card-row">
                        <div class="table-mobile-card-label">Role:</div>
                        <div class="table-mobile-card-value"><span class="badge ${user.role === 'admin' ? 'badge-danger' : 'badge-primary'}">${user.role}</span></div>
                    </div>
                    <div style="margin-top: 1rem;">
                        <button class="btn btn-sm btn-primary btn-block" onclick="fillUpdateForm('${escapeHtml(user.username)}')">Edit User</button>
                    </div>
                </div>
            </div>
        `).join('');
        
        // Insert mobile cards
        if (mobileCards) {
            tableContainer.insertAdjacentHTML('afterbegin', mobileCards);
        }
    } else {
        // Remove mobile cards on desktop
        existingMobileCards.forEach(card => card.remove());
    }
}

// Handle window resize for mobile cards
if (document.getElementById('usersTableBody')) {
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const tableContainer = document.querySelector('.table-container');
            if (tableContainer) {
                // Reload users to update mobile cards
                loadUsers();
            }
        }, 250);
    });
}

// Log API connection info
console.log('Frontend connected to backend at:', API_BASE);

