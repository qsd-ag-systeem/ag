import { Container, Title, Flex, Grid } from "@mantine/core";
import DirectoryBrowser from "../components/DirectoryBrowser";
import Results from "../components/Results";

export default function Home() {
  return (
    <Container fluid>
      {/* <DirectoryBrowser /> */}
      <Grid columns={5} sx={{ height: "100%" }}>
        <Grid.Col span={1}>
          <Flex
            sx={theme => ({
              padding: `${theme.spacing.sm}px ${theme.spacing.md}px`,
              border: `1px solid ${
                theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[3]
              }`,
              borderRadius: theme.radius.md,
            })}
          ></Flex>
        </Grid.Col>
        <Grid.Col span={5}>
          <Results />
        </Grid.Col>
      </Grid>
    </Container>
  );
}
