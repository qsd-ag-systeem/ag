import { API_URL, FETCH_HEADERS } from "../constants";
import { BodyImport } from "../../types";

export const fetchImport = async (data: BodyImport) => {
    return await fetch(`${API_URL}/import`, {
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