import { Container } from "@mantine/core";
import DatasetList from "../../components/lists/DatasetList";
import SearchResults from "../../components/SearchResults";

export default function Search() {
  return (
    <Container fluid>
      <DatasetList />
      <SearchResults folder="input/pytest" />
    </Container>
  );
}
