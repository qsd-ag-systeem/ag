import { useQuery } from "@tanstack/react-query";
import { fetchEnroll } from "../api/enroll";
import { BodyEnroll } from "../../types";

export default function useEnroll(data: BodyEnroll) {
  return useQuery(["enroll", data], () => fetchEnroll(data))
}