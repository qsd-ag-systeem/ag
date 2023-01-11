import { API_URL, FETCH_HEADERS } from "../constants";
import { BodyDelete } from "../../types";

export const fetchDelete = async (data: BodyDelete) => {
    return await fetch(`${API_URL}/delete`, {
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