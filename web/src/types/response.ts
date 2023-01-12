import {CrossSearchResult, SearchResult} from "./index";

export type SuccessResponse<T> = {
  data: T | null;
  errors: string[] | null;
};

export type ErrorResponse<T> = {
  errors: string[];
  data: T | Record<string, any> | null;
};

export type SearchResponse = SuccessResponse<SearchResult[]>;
export type CrossSearchResponse = SuccessResponse<CrossSearchResult[]>;

