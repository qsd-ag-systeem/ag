import { API_URL, FETCH_HEADERS } from "../constants";

export const enroll = async (inputDir: string) => {
    const data = {
        folder: inputDir
    };

    return await fetch(`${API_URL}/enroll`, {
        ...FETCH_HEADERS(),
        method: "POST",
        body: JSON.stringify(data)
    })
        .then((data) => {
            return data.json();
        })
        .catch((error) => {
            throw error.message;
        });
}
