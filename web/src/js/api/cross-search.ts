import { API_URL, FETCH_HEADERS } from "../constants";
import { BodyCrossSearch, CrossSearchResponse } from "../../types";

export const fetchCrossSearch = async (data: BodyCrossSearch): Promise<CrossSearchResponse> => {
  return await fetch(`${API_URL}/cross-search`, {
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
