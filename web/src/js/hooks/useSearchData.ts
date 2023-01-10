import { useQuery } from "@tanstack/react-query";
import { fetchSearch } from "../api/search";

export default function useSearchData(folder: string, dataset: string, cuda: boolean = false) {
  return useQuery(
      ["search", folder, dataset, cuda],
      () => fetchSearch({folder, dataset, cuda}),
    )
}