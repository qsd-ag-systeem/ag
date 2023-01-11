export type SuccessResponse<T> = {
  data: T | null;
  errors: string[] | null;
};

export type ErrorResponse<T> = {
  errors: string[];
  data: T | Record<string, any> | null;
};


