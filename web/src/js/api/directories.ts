import { API_URL, FETCH_HEADERS } from "../constants";

export const fetchDirectories = async (query: string = "") => {
    return await fetch(`${API_URL}/directories/${query}`, {
        ...FETCH_HEADERS()
    })
        .then((data) => {
            return data.json();
        })
        .catch((error) => {
            throw error.message;
        });
};
