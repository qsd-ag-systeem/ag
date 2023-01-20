export type SearchResult = {
  input_file: string;
  id: string;
  dataset: string;
  file_name: string;
  similarity: number;
  top_left: number[];
  bottom_right: number[];
  input: Omit<SearchResult, "input">;
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
