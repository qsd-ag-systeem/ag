import { createStyles, Flex, LoadingOverlay } from "@mantine/core";
import { BodySearch } from "../../types";

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

type SearchResultsProps = BodySearch;

export default function SearchResults({ folder, cuda, datasets }: SearchResultsProps) {
  const { classes } = useStyles();

  const { isSuccess, data: results, isFetching } = useSearchData({ folder, cuda, datasets });

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
