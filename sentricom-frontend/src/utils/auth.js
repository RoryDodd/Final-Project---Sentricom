export function saveSessionToken(token) {
  localStorage.setItem("sentricom_session_token", token);
}

export function getSessionToken() {
  return localStorage.getItem("sentricom_session_token");
}

export function removeSessionToken() {
  localStorage.removeItem("sentricom_session_token");
}

export function isLoggedIn() {
  return !!getSessionToken();
}

// Get current user role
export function getUserRole() {
  return localStorage.getItem("sentricom_role");
}

// Check if current user is admin
export function isAdmin() {
  return getUserRole() === "admin";
}