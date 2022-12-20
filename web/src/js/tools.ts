/**
 * Get a environment variable.
 */
export function env(name: string, defaultValue: string = "") {
    return import.meta.env[`VITE_${name}`] || defaultValue;
}

/**
 * Test if localstorage has a token.
 */
export function hasAuthToken() {
    return Boolean(getAuthToken());
}

/**
 * Test if localstorage has a token.
 */
export function getAuthToken() {
    return localStorage.getItem("token");
}

/**
 * Set the authentication token in the local storage.
 */
export function setAuthToken(token: string) {
    localStorage.setItem("token", token);
}

/**
 * Remove authorization token from the local storage.
 */
export function removeAuthToken(): void {
    localStorage.removeItem('token');
}