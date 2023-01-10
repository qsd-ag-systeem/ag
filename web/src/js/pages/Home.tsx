import { Container, Flex } from "@mantine/core";
import DirectoryBrowser from "../components/DirectoryBrowser";
import SearchResults from "../components/SearchResults";

export default function Home() {
  return (
    <Container fluid>
      <DirectoryBrowser />

      <SearchResults folder="C:/Users/Joel/ag/input/test" />
    </Container>
  );
}
