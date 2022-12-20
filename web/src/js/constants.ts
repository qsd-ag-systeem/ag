import {env, getAuthToken} from "./tools";

/**
 * The application name
 * Used for setting the title
 */
export const APP_NAME = env("APP_NAME", "AG-Systeem");

/**
 * The API url
 */
export const API_URL = env("API_URL");

/**
 * Debounce timeout
 * See https://mantine.dev/hooks/use-debounced-value
 */
export const DEBOUNCE_TIMEOUT = 300;

/**
 * Get the default fetch headers
 */
export const FETCH_HEADERS = () => {
    return {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAuthToken()}`,
        },
    };
};
