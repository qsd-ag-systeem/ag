export type SuccessResponse<T> = {
  data: T | null;
  errors: string[] | null;
};

export type ErrorResponse<T> = {
  errors: string[];
  data: T | Record<string, any> | null;
};

export type SearchResult = {
  input_file: string;
  id: string;
  dataset: string;
  file_name: string;
  similarity: number;
  left_bound: number[];
  right_bound: number[];
};

export type SearchResponse = SuccessResponse<SearchResult[]>;
