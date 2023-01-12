import { useQuery } from "@tanstack/react-query";
import { fetchCrossSearch } from "../api/cross-search";
import { BodyCrossSearch } from "../../types";

export default function useCrossSearchData(data?: BodyCrossSearch) {
  return useQuery({
      queryKey: ["cross-search", data],
      queryFn: () => fetchCrossSearch(data as BodyCrossSearch),
      enabled: !!data,
  })
}