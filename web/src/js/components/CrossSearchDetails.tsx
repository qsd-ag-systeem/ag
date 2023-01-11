import { ColorSwatch, Group, Paper, Title } from "@mantine/core";
import { IconCheck } from "@tabler/icons";
import { SearchResult } from "../../types";
import usePercentageColor from "../hooks/usePercentageColor";
import ImageDetails from "./ImageDetails";

type CrossSearchDetailsProps = {
  match: SearchResult;
};

export default function CrossSearchDetails(props: CrossSearchDetailsProps) {
  const { match } = props;
  const color = usePercentageColor(match.similarity);

  return (
    <>
      <Group grow mb={"md"}>
        <ImageDetails file_name={match.file1} dataset={match.dataset1} />
        <ImageDetails file_name={match.file2} dataset={match.dataset2} />
      </Group>
      <Paper withBorder p={"md"}>
        <Group position={"center"}>
          <Title order={1}>Score: {match.similarity}%</Title>
          <ColorSwatch color={color} size={48}>
            <IconCheck stroke={3} size={36} color={"white"} />
          </ColorSwatch>
        </Group>
      </Paper>
    </>
  );
}
