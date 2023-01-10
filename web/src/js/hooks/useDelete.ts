import { useQuery } from "@tanstack/react-query";
import { fetchDelete } from "../api/delete";
import { BodyDelete } from "../../types";

export default function useDelete(data: BodyDelete) {
  return useQuery(
      ["delete", data],
      () => fetchDelete(data)
  )
}