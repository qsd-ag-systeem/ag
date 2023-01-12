export type BodyExport = {
  path: string;
  dataset?: string;
};

export type BodyEnroll = {
  folder: string;
  cuda?: boolean;
};

export type BodyImport = {
  path: string;
};

export type BodySearch = {
  folder: string;
  cuda?: boolean;
  dataset?: string;
};

export type BodyCrossSearch = {
  dataset1: string;
  dataset2: string;
};

export type BodyDeleteDataset = {
  dataset: string;
  files: string[];
  remove_file: boolean;
};