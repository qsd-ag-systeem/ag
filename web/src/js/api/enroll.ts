import { API_URL, FETCH_HEADERS } from "../constants";

export const enroll = async (inputDir: string, name: string | null) => {
    if (name?.trim() === "") name = null;
    const data = {
        folder: inputDir,
        name: name,
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
