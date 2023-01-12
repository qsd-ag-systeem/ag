import { useQuery } from "@tanstack/react-query";
import { fetchSearch } from "../api/search";
import { BodySearch } from "../../types";

export default function useSearchData({ folder, dataset, cuda }: BodySearch) {
  return useQuery(
    ["results", folder, cuda, dataset],
    () => fetchSearch({ folder, cuda, dataset }),
    {
      keepPreviousData: true,
      placeholderData: {
        data: Array.from({ length: 10 })
          .fill(0)
          .map((_, i) => ({
            id: "loading-" + i,
            dataset: "",
            file_name: "",
            similarity: 0,
            input_file: "",
            left_bound: [0],
            right_bound: [0],
          })),
        errors: [],
      },
    }
  );
}
