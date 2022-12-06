CREATE TABLE public.faces
(
    id SERIAL PRIMARY KEY,
    dataset character varying(100) NOT NULL,
    file_name character varying(100) NOT NULL,
    width smallint NOT NULL,
    height smallint NOT NULL,
    x point NOT NULL,
    y point NOT NULL,
    face_embedding double precision[] NOT NULL
);
