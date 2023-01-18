import { useQuery } from "@tanstack/react-query";
import { fetchSearch } from "../api/search";
import { BodySearch, SearchResult } from "../../types";

export default function useSearchData({ folder, datasets, cuda }: BodySearch) {
  return useQuery<SearchResult[]>(
    ["results", folder, cuda, datasets],
    () => fetchSearch({ folder, cuda, datasets }),
    {
      keepPreviousData: true,
      placeholderData: Array.from({ length: 10 })
        .fill(0)
        .map((_, i) => ({
          id: "loading-" + i,
          dataset: "",
          file_name: "",
          similarity: 0,
          input_file: "",
          top_left: [],
          bottom_right: [],
          input: {
            id: "loading-" + i,
            dataset: "",
            file_name: "",
            similarity: 0,
            input_file: "",
            top_left: [],
            bottom_right: [],
          },
        })),
    }
  );
}
