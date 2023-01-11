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

export type CrossSearchResult = {
  dataset1: string;
  dataset2: string;
  file1: string;
  file2: string;
  similarity: number;
  top_left_1: number[];
  top_left_2: number[];
  bottom_right_1: number[];
  bottom_right_2: number[];
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

export type Dataset = {
    id: string;
    name: string;
    count: number;
}
