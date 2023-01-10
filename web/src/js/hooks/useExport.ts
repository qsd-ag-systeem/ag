import { useQuery } from "@tanstack/react-query";
import { fetchExport } from "../api/export";

export default function useExport(path: string, dataset: string) {
  return useQuery(["export", path], () => fetchExport({path, dataset}))
}