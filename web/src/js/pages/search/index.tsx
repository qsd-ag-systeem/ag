import { Button, createStyles, Flex, Group, Paper, Text, Title } from "@mantine/core";
import { openModal } from "@mantine/modals";
import { IconPlus } from "@tabler/icons";
import { useState } from "react";
import DirectoryBrowser from "../../components/DirectoryBrowser";
import Enroll from "../../components/Enroll";
import DatasetList from "../../components/lists/DatasetList";
import SearchResults from "../../components/SearchResults";

const useStyles = createStyles(theme => ({
  datasetListContainer: {
    flexGrow: 0.5,
    overflowY: "scroll",
    flexBasis: "min-content",
  },
}));

export default function Search() {
  const { classes } = useStyles();

  const [selected, setSelected] = useState<string[]>([]);
  const [currentDir, setCurrentDir] = useState<string>("");

  return (
    <Flex gap="sm" p="sm" direction="column">
      <Flex direction="row" gap="sm" sx={{ flexBasis: 1 }}>
        <Paper p={"sm"} withBorder className={classes.datasetListContainer}>
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
        <Paper sx={{ flexGrow: 1 }} p={"sm"} withBorder>
          <DirectoryBrowser onUpdate={setCurrentDir} />
        </Paper>
        <Paper p={"sm"} withBorder sx={{ flexGrow: 1 }}></Paper>
      </Flex>
      <Flex sx={{ flexGrow: 2 }}>
        <SearchResults folder={currentDir} datasets={selected} />
      </Flex>
    </Flex>
  );
}
