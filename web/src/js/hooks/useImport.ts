import { useQuery } from "@tanstack/react-query";
import { fetchImport } from "../api/import";

export default function useImport(path: string) {
  return useQuery(["import", path], () => fetchImport({path}))
}