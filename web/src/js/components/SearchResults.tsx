import { createStyles, Flex, LoadingOverlay } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { BodySearch, SearchResult } from "../../types";
import { fetchSearch } from "../api/search";
import { API_URL } from "../constants";
import Match from "./Match";

const useStyles = createStyles((theme) => ({
  results: {
    padding: `${theme.spacing.sm}px ${theme.spacing.md}px`,
    border: `1px solid ${
      theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[3]
    }`,
    borderRadius: theme.radius.md,
    gap: theme.spacing.sm,
    overflowX: "scroll",
    gridArea: "results",
    position: "relative",
    scrollSnapType: "x proximity",
  },
}));

type SearchResultsProps = BodySearch;

export default function SearchResults({ folder, cuda, datasets }: SearchResultsProps) {
  const { classes } = useStyles();

  const {
    isSuccess,
    data: results,
    isFetching,
  } = useQuery<SearchResult[]>(
    ["results", folder, cuda, datasets],
    () => fetchSearch({ folder, cuda, datasets }),
    {
      keepPreviousData: true,
      placeholderData: Array.from({ length: 10 })
        .fill(0)
        .map((_, i) => ({
          id: "loading-" + i,
          dataset: "",
          file_name: "",
          similarity: 0,
          input_file: "",
          left_bound: [0],
          right_bound: [0],
        })),
    }
  );

  return (
    <Flex className={classes.results} sx={{ overflowX: isFetching ? "hidden" : "auto" }}>
      <LoadingOverlay visible={isFetching} overlayBlur={2} />
      {results?.map((match, i) => (
        <Match
          image={`${API_URL}/image/${match.dataset}/${match.file_name}`}
          percentage={match.similarity}
          fileName={match.file_name}
          dataset={match.dataset}
          inputFile={match.input_file}
          key={match.id + "-" + i}
        />
      ))}
    </Flex>
  );
}
