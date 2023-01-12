import { ColorSwatch, Group, Paper, Title } from "@mantine/core";
import { IconCheck } from "@tabler/icons";
import { CrossSearchResult } from "../../types";
import usePercentageColor from "../hooks/usePercentageColor";
import ImageDetails from "./ImageDetails";

type CrossSearchDetailsProps = {
  match: CrossSearchResult;
};

export default function CrossSearchDetails(props: CrossSearchDetailsProps) {
  const { match } = props;
  const color = usePercentageColor(match.score);

  return (
    <>
      <Group grow mb={"md"} sx={{ alignItems: "stretch" }}>
        <ImageDetails
          file_name={match.file1}
          dataset={match.dataset1}
          top_left={match.top_left_1}
          bottom_right={match.bottom_right_1}
          width={match.width1}
          height={match.height1}
        />
        <ImageDetails
          file_name={match.file2}
          dataset={match.dataset2}
          top_left={match.top_left_2}
          bottom_right={match.bottom_right_2}
          width={match.width2}
          height={match.height2}
        />
      </Group>
      <Paper withBorder p={"md"}>
        <Group position={"center"}>
          <Title order={1}>Score: {match.score}%</Title>
          <ColorSwatch color={color} size={48}>
            <IconCheck stroke={3} size={36} color={"white"} />
          </ColorSwatch>
        </Group>
      </Paper>
    </>
  );
}
