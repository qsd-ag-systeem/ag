import { API_URL, FETCH_HEADERS } from "../constants";

type BodyExport = {
    path: string;
    dataset?: string;
}

export const fetchExport = async (data: BodyExport) => {
    return await fetch(`${API_URL}/export`, {
        method: 'POST',
        body: JSON.stringify(data),
        ...FETCH_HEADERS()
    })
        .then((data) => {
            return data.json();
        })
        .catch((error) => {
            throw error.message;
        });
};