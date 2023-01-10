import { useQuery } from "@tanstack/react-query";
import { fetchSearch } from "../api/search";
import { BodySearch } from "../../types";

export default function useSearchData(data: BodySearch) {
  return useQuery(
      ["search", data],
      () => fetchSearch(data),
    )
}