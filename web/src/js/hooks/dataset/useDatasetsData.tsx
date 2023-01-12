import { useQuery } from "@tanstack/react-query";
import { Dataset } from "../../../types";
import { fetchDatasets } from "../../api/datasets";

export default function useDatasetsData() {
  return useQuery<Dataset[]>(["datasets"], () => fetchDatasets());
}
