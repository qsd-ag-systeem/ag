import { useQuery } from "@tanstack/react-query";
import { fetchDatasets } from "../api/datasets";

export default function useDatasetsData() {
  return useQuery(["datasets"], () => fetchDatasets())
}