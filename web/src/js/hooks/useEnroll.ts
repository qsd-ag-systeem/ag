import { useQuery } from "@tanstack/react-query";
import { fetchEnroll } from "../api/enroll";

export default function useEnroll(folder: string, cuda: boolean = false) {
  return useQuery(["enroll", folder, cuda], () => fetchEnroll({folder, cuda}))
}