import { Container } from "@mantine/core";
import SearchResults from "../../components/SearchResults";

export default function Search() {
  return (
    <Container fluid>
      <SearchResults folder="input/pytest" />
    </Container>
  );
}
