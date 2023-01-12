import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Dataset } from "../../../types";

export default function useMutateSectionData(
  mutationFn: (...args: any) => Promise<unknown>,
  onSuccess?: (values: Dataset) => void,
  onError?: (error: string) => void
) {
  const queryClient = useQueryClient();

  return useMutation(mutationFn, {
    onSuccess: (data) => {
      // Invalidate datasets query cache to update the UI
      queryClient.invalidateQueries(["datasets"]);

      onSuccess?.(data as any);
    },
    onError: (data) => onError?.(data as any),
  });
}
