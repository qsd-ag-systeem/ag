import { useQuery } from "@tanstack/react-query";
import { fetchDirectories } from "../api/directories";

export default function useDirectoriesData(currentDir: string = "") {
  return useQuery(
      ["directories", currentDir],
      () => fetchDirectories(currentDir),
      {
          keepPreviousData: true,
      }
    )
}