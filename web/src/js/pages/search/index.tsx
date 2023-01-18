import { Box, Button, createStyles, Flex, Group, Paper, Text, Title } from "@mantine/core";
import { openModal } from "@mantine/modals";
import { IconPlus } from "@tabler/icons";
import { useEffect, useState } from "react";
import { SearchResult } from "../../../types";
import DirectoryBrowser from "../../components/DirectoryBrowser";
import Enroll from "../../components/Enroll";
import FacialImage from "../../components/FacialImage";
import DatasetList from "../../components/lists/DatasetList";
import SearchResults from "../../components/SearchResults";

const useStyles = createStyles((theme) => ({
  datasetListContainer: {
    overflowY: "scroll",
  },

  rowItem: {
    flexBasis: "33.33%",
    height: "calc(100vh - 380px)",
  },
}));

export default function Search() {
  const { classes, cx } = useStyles();

  const [selected, setSelected] = useState<string[]>([]);
  const [currentDir, setCurrentDir] = useState<string>("");
  const [selectedMatch, setSelectedMatch] = useState<SearchResult | undefined>();

  // Reset selected match when selected datasets or current directory changes
  useEffect(() => {
    setSelectedMatch(undefined);
  }, [selected, currentDir]);

  return (
    <Flex gap="sm" p="sm" direction="column">
      <Flex direction="row" gap="sm" sx={{ flexBasis: 1 }}>
        <Paper p={"sm"} withBorder className={cx(classes.rowItem, classes.datasetListContainer)}>
          <Group position={"apart"} pb={"md"}>
            <Title order={3}>Datasets</Title>
            <Button
              onClick={() => {
                openModal({
                  title: (
                    <Text fw={700} fz="xl">
                      Dataset toevoegen
                    </Text>
                  ),
                  children: <Enroll />,
                  size: "lg",
                });
              }}
            >
              <IconPlus />
            </Button>
          </Group>
          <DatasetList onUpdateSelected={setSelected} />
        </Paper>
        <Paper
          className={classes.rowItem}
          p={"sm"}
          withBorder
          sx={{ display: "flex", flexDirection: "column" }}
        >
          <Box sx={{ flexGrow: 1, height: "100%" }}>
            {selectedMatch?.dataset ? (
              <FacialImage {...selectedMatch.input} dataset={currentDir} />
            ) : (
              <DirectoryBrowser onUpdate={setCurrentDir} />
            )}
          </Box>
        </Paper>
        <Paper p={"sm"} withBorder className={classes.rowItem}>
          {selectedMatch?.dataset && <FacialImage {...selectedMatch} />}
        </Paper>
      </Flex>
      <Flex sx={{ flexGrow: 2 }}>
        <SearchResults
          folder={currentDir}
          datasets={selected}
          setSelectedMatch={setSelectedMatch}
          selectedMatch={selectedMatch}
        />
      </Flex>
    </Flex>
  );
}
