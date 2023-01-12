import { Maybe } from "../types";

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

export function isEmptyArray(input: Maybe<any[]>) {
  return Array.isArray(input) && !input.length;
}

/**
 * Format errors from backend
 */
export function formatErrors(response: any) {
  if (response?.errors?.stacktrace) {
    delete response.errors.stacktrace;
  }

  let messages: Array<string> = [];

  response.message && messages.push(response.message);

  if (response.errors) {
    for (let key in response.errors) {
      messages.push(response.errors[key]);
    }
  }

  return messages;
}

export async function handleRequestErrors(response: Response) {
  if (!response.ok) {
    let responseClone = response.clone();
    let errors;

    try {
      errors = formatErrors(JSON.parse(await responseClone.text()));
    } catch (err) {
      throw new Error(response.statusText);
    }

    if (!isEmptyArray(errors)) {
      throw new Error(errors[0]);
    }

    throw new Error("An unknown error occurred.");
  }

  return response;
}
