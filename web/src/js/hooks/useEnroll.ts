import { useQuery } from "@tanstack/react-query";
import { fetchEnroll } from "../api/enroll";
import { BodyDelete } from "../../types";

export default function useEnroll(data: BodyDelete) {
  return useQuery(["enroll", data], () => fetchEnroll(data))
}