import { API_URL, FETCH_HEADERS } from "../constants";

type BodySearch = {
    folder: string;
    cuda?: boolean;
    dataset?: string;
}

export const fetchSearch = async (data: BodySearch) => {
    return await fetch(`${API_URL}/search`, {
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