import { useQuery } from "@tanstack/react-query";
import { fetchImport } from "../api/import";
import { BodyImport } from "../../types";

export default function useImport(data: BodyImport) {
  return useQuery(["import", data], () => fetchImport(data))
}