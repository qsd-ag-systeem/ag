import { Container, Title, Flex, Text } from "@mantine/core";
import DirectoryBrowser from "../components/DirectoryBrowser";
import Results from "../components/Results";
import styled from "@emotion/styled";

const Grid = styled.div`
  display: grid;
  grid-grid-template-areas: "
    algorithm add-database match
    results results results
  ";
`;

export default function Home() {
  return (
    <Container fluid>
      {/* <DirectoryBrowser /> */}
      <Grid>
        <Flex
          sx={theme => ({
            padding: `${theme.spacing.sm}px ${theme.spacing.md}px`,
            border: `1px solid ${
              theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[3]
            }`,
            borderRadius: theme.radius.md,
            gridArea: "algorithm",
          })}
        />
        <Flex
          sx={theme => ({
            padding: `${theme.spacing.sm}px ${theme.spacing.md}px`,
            border: `1px solid ${
              theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[3]
            }`,
            borderRadius: theme.radius.md,
            gridArea: "add-database",
          })}
        />
        <Flex
          sx={theme => ({
            padding: `${theme.spacing.sm}px ${theme.spacing.md}px`,
            border: `1px solid ${
              theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[3]
            }`,
            borderRadius: theme.radius.md,
            gridArea: "match",
          })}
        />

        <Results />
      </Grid>
    </Container>
  );
}
