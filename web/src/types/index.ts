import { SuccessResponse } from "./response";

export type BodySearch = {
  folder: string;
  cuda?: boolean;
  dataset?: string;
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

export type BodyExport = {
  path: string;
  dataset?: string;
};

export type BodyEnroll = {
  folder: string;
  cuda?: boolean;
};

export type BodyDelete = {
  dataset: string;
  file: string;
  remove_file: boolean;
};

export type BodyImport = {
  path: string;
};
