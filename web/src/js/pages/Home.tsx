import { Box, Button, Container, ActionIcon, Text } from "@mantine/core";
import { openModal } from "@mantine/modals";
import { IconPlus } from "@tabler/icons";
import DirectoryBrowser from "../components/DirectoryBrowser";
import SearchResults from "../components/SearchResults";
import Enroll from "./Enroll";

export default function Home() {
  return (
    <Container fluid>
      {/* <DirectoryBrowser /> */}

      <ActionIcon
        variant="outline"
        onClick={() =>
          openModal({
            title: (
              <Text fw={700} fz="xl">
                Dataset toevoegen
              </Text>
            ),
            children: <Enroll />,
            size: "lg",
          })
        }
      >
        <IconPlus />
      </ActionIcon>
      <SearchResults />
    </Container>
  );
}
