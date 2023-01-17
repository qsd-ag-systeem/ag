export * from "./response";
export * from "./result";
export * from "./body";

export type Maybe<T> = T | null | undefined;

export type Dataset = {
  id: string;
  name: string;
  count: number;
};