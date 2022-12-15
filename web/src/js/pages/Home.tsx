import { Container, Title } from "@mantine/core";
import DirectoryBrowser from "../components/DirectoryBrowser";

export default function Home() {
  return (
    <Container fluid>
      <Title>Home</Title>
      <DirectoryBrowser />
    </Container>
  );
}
