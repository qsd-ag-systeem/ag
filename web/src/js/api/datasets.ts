import { API_URL, FETCH_HEADERS } from "../constants";

export const fetchDatasets = async (query: string = "") => {
    return await fetch(`${API_URL}/datasets?q=${query}`, {
        ...FETCH_HEADERS()
    })
        .then((data) => {
            return data.json();
        })
        .catch((error) => {
            throw error.message;
        });
};