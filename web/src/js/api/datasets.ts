import { API_URL, FETCH_HEADERS } from "../constants";

export const fetchDatasets = async () => {
    return await fetch(`${API_URL}/datasets`, {
        ...FETCH_HEADERS()
    })
        .then((data) => {
            return data.json();
        })
        .catch((error) => {
            throw error.message;
        });
};