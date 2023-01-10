import { API_URL, FETCH_HEADERS } from "../constants";
import { BodyEnroll } from "../../types";

export const fetchEnroll = async (data: BodyEnroll) => {
    return await fetch(`${API_URL}/enroll`, {
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