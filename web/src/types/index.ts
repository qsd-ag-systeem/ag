import { SuccessResponse } from "./response";

export * from "./response";
export * from "./result";
export * from "./body";

export type Maybe<T> = T | null | undefined;

export type BodySearch = {
  folder: string;
  cuda?: boolean;
  datasets?: string[];
};

export type BodyCrossSearch = {
  dataset1: string;
  dataset2: string;
};

export type BodyExport = {
  path: string;
  dataset?: string;
};

export type BodyEnroll = {
  folder: string;
  name?: string;
  cuda?: boolean;
};

export type BodyDeleteDataset = {
  dataset: string;
  files: string[];
  remove_file: boolean;
};

export type BodyImport = {
  path: string;
};

export type SearchResponse = SuccessResponse<SearchResult[]>;
export type CrossSearchResponse = SuccessResponse<CrossSearchResult[]>;

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
  score: number;
  top_left_1: number[];
  top_left_2: number[];
  bottom_right_1: number[];
  bottom_right_2: number[];
  width1: number;
  height1: number;
  width2: number;
  height2: number;
};

export type Dataset = {
  id: string;
  name: string;
  count: number;
};
