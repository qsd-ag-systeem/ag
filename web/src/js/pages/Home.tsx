import { Container, Flex } from "@mantine/core";
import DirectoryBrowser from "../components/DirectoryBrowser";
import SearchResults from "../components/Results";

export default function Home() {
  return (
    <Container fluid>
      <DirectoryBrowser />

      <SearchResults />
    </Container>
  );
}
