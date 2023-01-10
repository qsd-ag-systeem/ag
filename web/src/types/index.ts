export type BodySearch = {
    folder: string;
    cuda?: boolean;
    dataset?: string;
}

export type BodyExport = {
    path: string;
    dataset?: string;
}

export type BodyEnroll = {
    folder: string;
    cuda?: boolean;
}

export type BodyDelete = {
    dataset: string;
    file: string;
    remove_file: boolean;
}

export type BodyImport = {
    path: string;
}