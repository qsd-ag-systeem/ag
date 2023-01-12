import { Grid, Paper } from "@mantine/core";
import { useEffect, useState } from "react";
import { BodyCrossSearch, CrossSearchResult } from "../../../types";
import CrossSearchDetails from "../../components/CrossSearchDetails";
import CrossSearchMatchCard from "../../components/CrossSearchMatchCard";
import CrossSearchForm from "../../components/forms/CrossSearchForm";
import useCrossSearchData from "../../hooks/useCrossSearchData";

export default function CrossSearch() {
  const [formValues, setFormValues] = useState<BodyCrossSearch | undefined>();
  const { data: matches, isFetching: isLoading } = useCrossSearchData(formValues);
  const [selectedMatch, setSelectedMatch] = useState<CrossSearchResult | null>(null);

  const onCrossSearch = (values: BodyCrossSearch) => setFormValues(values);

  // Reset selected match when matches change
  useEffect(() => {
    setSelectedMatch(null);
  }, [matches]);

  return (
    <>
      <Grid m={0}>
        <Grid.Col span={2}>
          <Paper p={"sm"} withBorder sx={{ height: "100%" }}>
            <CrossSearchForm isLoading={isLoading} submitAction={onCrossSearch} />
          </Paper>
        </Grid.Col>
        {!isLoading && matches && (
          <>
            <Grid.Col span={4}>
              <Paper p={"sm"} withBorder sx={{ overflowY: "scroll", height: "calc(100vh - 76px)" }}>
                {matches?.data?.map((match) => (
                  <CrossSearchMatchCard
                    onClick={() => setSelectedMatch(match)}
                    match={match}
                    key={`${match.dataset1}-${match.file1}-${match.dataset2}-${match.file2}`}
                  />
                ))}
              </Paper>
            </Grid.Col>
            <Grid.Col span={"auto"}>
              {selectedMatch && <CrossSearchDetails match={selectedMatch} />}
            </Grid.Col>
          </>
        )}
      </Grid>
    </>
  );
}
