import { createStyles, Flex, LoadingOverlay } from "@mantine/core";
import { Dispatch, SetStateAction, useEffect } from "react";
import { BodySearch, SearchResult } from "../../types";

import { API_URL } from "../constants";
import useSearchData from "../hooks/useSearchData";
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

type SearchResultsProps = BodySearch & {
  setSelectedMatch: Dispatch<SetStateAction<SearchResult | undefined>>;
  selectedMatch: SearchResult | undefined;
};

export default function SearchResults({
  folder,
  datasets,
  setSelectedMatch,
  selectedMatch,
}: SearchResultsProps) {
  const { classes } = useStyles();

  const { data: results, isFetching, isSuccess } = useSearchData({ folder, datasets });

  useEffect(() => {
    if (isSuccess) {
      setSelectedMatch?.(results?.[0]);
    }
  }, [results]);

  return (
    <Flex className={classes.results} sx={{ overflowX: isFetching ? "hidden" : "auto" }}>
      <LoadingOverlay visible={isFetching} overlayBlur={2} />
      {results?.map((match, i) => (
        <Match key={match.id + "-" + i} onClick={() => setSelectedMatch(match)} {...match} />
      ))}
    </Flex>
  );
}
