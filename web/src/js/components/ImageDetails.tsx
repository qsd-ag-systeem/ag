import { Stack, Image, Paper, Group, Text } from "@mantine/core";
import React from "react";

type ImageDetailsProps = {
  file_name: string;
  dataset: string;
};

export default function ImageDetails(props: ImageDetailsProps) {
  const { file_name, dataset } = props;

  return (
    <Paper withBorder>
      <Image
        width={"100%"}
        draggable={false}
        src={"https://avatars.githubusercontent.com/u/19374765?v=4"}
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
    </Paper>
  );
}
