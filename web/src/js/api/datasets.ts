import { BodyDeleteDataset } from "../../types";
import { API_URL, FETCH_HEADERS } from "../constants";
import { handleRequestErrors } from "../tools";

export const fetchDatasets = async (query: string = "") => {
    return await fetch(`${API_URL}/datasets?q=${query}`, {
        ...FETCH_HEADERS()
    })
        .then((data) => {
            return data.json();
        })
        .then((data) => {
            return data.data;
        })
        .catch((error) => {
            throw error.message;
        });
};


export const deleteDataset = async (values: BodyDeleteDataset) => {
    return await fetch(`${API_URL}/delete`, {
        ...FETCH_HEADERS(),
        method: 'POST',
        body: JSON.stringify(values),
    })
        .then((data) => handleRequestErrors(data))
        .then((data) => {
            return data.json();
        })
        .catch((error) => {
            throw error.message;
        });
}
