import { API_URL, FETCH_HEADERS } from "../constants";
import { BodySearch, SearchResponse } from "../../types";

export const fetchSearch = async (data: BodySearch): Promise<SearchResponse> => {
  return await fetch(`${API_URL}/search`, {
    method: "POST",
    body: JSON.stringify(data),
    ...FETCH_HEADERS(),
  })
    .then(data => {
      return data.json();
    })
    .catch(error => {
      throw error.message;
    });
};
