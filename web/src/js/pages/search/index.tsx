import { Anchor, Button, createStyles, Flex, Group, Paper, Title } from "@mantine/core";
import { IconPlus } from "@tabler/icons";
import { useState } from "react";
import { Link } from "react-router-dom";
import DirectoryBrowser from "../../components/DirectoryBrowser";
import DatasetList from "../../components/lists/DatasetList";
import SearchResults from "../../components/SearchResults";

const useStyles = createStyles((theme) => ({
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
            <Anchor component={Link} to={"/enroll"}>
              <Button>
                <IconPlus />
              </Button>
            </Anchor>
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
