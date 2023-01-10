import { createStyles, Flex, Loader, Skeleton, LoadingOverlay } from "@mantine/core";
import { useMutation } from "@tanstack/react-query";
import { fetchSearch } from "../api/search";
import { useEffect, useMemo } from "react";
import Match from "./Match";
import { SearchResponse } from "../types";

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
  },
}));

type Match = {
  image: string;
  percentage: number;
};

const matches: Match[] = [
  {
    image:
      "https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    percentage: 80,
  },
  {
    image:
      "https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    percentage: 20,
  },
  {
    image:
      "https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    percentage: 1,
  },
  {
    image:
      "https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    percentage: 50,
  },
  {
    image:
      "https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    percentage: 50,
  },
  {
    image:
      "https://images.unsplash.com/flagged/photo-1570612861542-284f4c12e75f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80",
    percentage: 50,
  },
];

export default function SearchResults({}) {
  const { classes } = useStyles();

  const {
    mutate: search,
    isSuccess,
    data: result,
    isLoading,
  } = useMutation(["results"], fetchSearch, {
    onError: error => {
      alert("Er is iets fout gegaan tijdens het zoeken. Probeer het opnieuw");
    },
  });

  useEffect(() => {
    search({
      folder: "C:/Users/Joel/ag/input/test",
    });
  }, []);

  return (
    <Flex className={classes.results} sx={{ overflowX: isLoading ? "hidden" : "auto" }}>
      <LoadingOverlay visible={isLoading} overlayBlur={2} />
      {isSuccess
        ? result?.data?.map((match, i) => (
            <Match
              image={`${match.dataset}/${match.file_name}`}
              percentage={match.similarity}
              fileName={match.file_name}
              key={`${match.id}-${i}`}
            />
          ))
        : Array.from({ length: 10 })
            .fill(0)
            .map((_, i) => <Match key={i} />)}
    </Flex>
  );
}
