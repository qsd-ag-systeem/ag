import { useQuery } from "@tanstack/react-query";
import { fetchExport } from "../api/export";
import { BodyExport } from "../../types";

export default function useExport(data: BodyExport) {
  return useQuery(["export", data], () => fetchExport(data))
}