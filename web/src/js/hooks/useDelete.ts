import { useQuery } from "@tanstack/react-query";
import { fetchDelete } from "../api/delete";

export default function useDelete(dataset: string, file: string, remove_file: boolean = false) {
  return useQuery(
      ["delete", dataset, file, remove_file],
      () => fetchDelete({dataset, file, remove_file})
  )
}