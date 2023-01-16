import { Group, Paper, Stack, Text } from "@mantine/core";
import FacialImage from "./FacialImage";

type ImageDetailsProps = {
  file_name: string;
  dataset: string;
  top_left?: number[];
  bottom_right?: number[];
  width?: number;
  height?: number;
};

export default function ImageDetails(props: ImageDetailsProps) {
  const {
    file_name,
    dataset,
    top_left,
    bottom_right,
    width: image_width,
    height: image_height,
  } = props;

  return (
    <Paper withBorder>
      <Stack justify="space-between" sx={{ height: "100%" }}>
        <FacialImage
          dataset={dataset}
          file_name={file_name}
          top_left={top_left}
          bottom_right={bottom_right}
          width={image_width}
          height={image_height}
        />

        <Group p={"md"} position={"apart"}>
          <Stack spacing="xs">
            <Text weight={500}>Dataset</Text>
            <Text>{dataset}</Text>
          </Stack>
          <Stack spacing="xs">
            <Text weight={500}>Bestandsnaam</Text>
            <Text>{file_name}</Text>
          </Stack>
        </Group>
      </Stack>
    </Paper>
  );
}
