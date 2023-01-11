import { Grid, Paper } from "@mantine/core";
import { useState } from "react";
import { SearchResult } from "../../types";
import CrossSearchDetails from "../components/CrossSearchDetails";
import CrossSearchMatchCard from "../components/CrossSearchMatchCard";
import CrossSearchForm, { CrossSearchFormValues } from "../components/forms/CrossSearchForm";

export default function Home() {
  const onCrossSearch = (values: CrossSearchFormValues) => console.log(values);

  const matches: SearchResult[] = [
    {
      id: "1",
      input_file: "kaaas",
      file_name: "test",
      dataset: "test",
      similarity: 1,
    },
    {
      id: "2",
      input_file: "kaaas",
      file_name: "test",
      dataset: "test",
      similarity: 2,
    },
    {
      id: "3",
      input_file: "kaaas",
      file_name: "test",
      dataset: "test",
      similarity: 3,
    },
    {
      id: "4",
      input_file: "kaaas",
      file_name: "test",
      dataset: "test",
      similarity: 4,
    },
  ] as SearchResult[];

  const [selectedMatch, setSelectedMatch] = useState(matches[0]);

  return (
    <Grid m={0}>
      <Grid.Col span={2}>
        <Paper p={"sm"} withBorder sx={{ height: "100%" }}>
          <CrossSearchForm submitAction={onCrossSearch} />
        </Paper>
      </Grid.Col>
      <Grid.Col span={4}>
        <Paper p={"sm"} withBorder sx={{ overflowY: "scroll", height: "calc(100vh - 76px)" }}>
          {matches.map((match) => (
            <CrossSearchMatchCard
              onClick={() => setSelectedMatch(match)}
              match={match}
              key={`${match.id}-${match.input_file}`}
            />
          ))}
        </Paper>
      </Grid.Col>
      <Grid.Col span={"auto"}>
        <CrossSearchDetails match={selectedMatch} />
      </Grid.Col>
    </Grid>
  );
}
