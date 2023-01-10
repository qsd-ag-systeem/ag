import { createStyles, Flex, LoadingOverlay, Overlay, Image, Button } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { BodySearch } from "../../types";
import { fetchSearch } from "../api/search";
import { ContextModalProps } from "@mantine/modals";

import Match from "./Match";

const useStyles = createStyles(theme => ({
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

export default function SearchResults({ folder, cuda, dataset }: SearchResultsProps) {
  const { classes } = useStyles();

  const {
    isSuccess,
    data: result,
    isLoading,
    isFetching,
  } = useQuery(["results", folder, cuda, dataset], () => fetchSearch({ folder, cuda, dataset }), {
    keepPreviousData: true,
    placeholderData: {
      data: Array.from({ length: 10 })
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
      errors: [],
    },
  });

  return (
    <Flex className={classes.results} sx={{ overflowX: isFetching ? "hidden" : "auto" }}>
      <LoadingOverlay visible={isFetching} overlayBlur={2} />
      {isSuccess &&
        result?.data?.map((match, i) => (
          <Match
            image={`${match.dataset}/${match.file_name}`}
            percentage={match.similarity}
            fileName={match.file_name}
            key={match.id + "-" + i}
          />
        ))}
    </Flex>
  );
}
