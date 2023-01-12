import { Anchor, Button, Flex, Group, Paper, Title } from "@mantine/core";
import { IconPlus } from "@tabler/icons";
import { useState } from "react";
import { Link } from "react-router-dom";
import DirectoryBrowser from "../../components/DirectoryBrowser";
import DatasetList from "../../components/lists/DatasetList";
import SearchResults from "../../components/SearchResults";

export default function Search() {
  const [selected, setSelected] = useState<string[]>([]);
  const [currentDir, setCurrentDir] = useState<string>("");

  return (
    <Flex gap="sm" p="sm" direction="column">
      <Flex direction="row" gap="sm" sx={{ flexBasis: 1 }}>
        <Paper
          p={"sm"}
          withBorder
          sx={{ flexGrow: 0.5, overflowY: "scroll", flexBasis: "min-content" }}
        >
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

    // <Grid m={0} grow sx={{ height: "calc(100vh - 76px)" }}>
    //   <Grid.Col span={3}>
    //     <Paper
    //       p={"sm"}
    //       withBorder
    //       sx={{ overflowY: "scroll", height: "calc(100vh - 375px - 76px)" }}
    //     >
    //       <Group position={"apart"} pb={"md"}>
    //         <Title order={3}>Datasets</Title>
    //         <Anchor component={Link} to={"/enroll"}>
    //           <Button>
    //             <IconPlus />
    //           </Button>
    //         </Anchor>
    //       </Group>
    //       <DatasetList />
    //       <Button>
    //         <Text></Text>
    //       </Button>
    //     </Paper>
    //   </Grid.Col>
    //   <Grid.Col span={3}>
    //     <Paper
    //       p={"sm"}
    //       withBorder
    //       sx={{ overflowY: "scroll", height: "calc(100vh - 375px - 76px)" }}
    //     ></Paper>
    //   </Grid.Col>
    //   <Grid.Col span={6}>
    // <Paper
    //   p={"sm"}
    //   withBorder
    //   sx={{ overflowY: "scroll", height: "calc(100vh - 375px - 76px)" }}
    // ></Paper>
    //   </Grid.Col>
    //   <Grid.Col span={12} sx={{ overflow: "hidden" }}>
    //     <SearchResults folder="input/pytest" />
    //   </Grid.Col>
    // </Grid>
  );
}
