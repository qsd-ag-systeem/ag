import { Button, Card, Group, LoadingOverlay, Text } from "@mantine/core";
import { IconTrash } from "@tabler/icons";
import useDatasetsData from "../../hooks/dataset/useDatasetsData";
import useDeleteDataset from "../../hooks/dataset/useDeleteDataset";
import { pluralize } from "../../tools";

export default function DatasetList() {
  const { data: datasets, isFetching } = useDatasetsData();
  const { openModal: openDeleteDatasetModal } = useDeleteDataset();

  return (
    <div style={{ position: "relative" }}>
      <LoadingOverlay visible={isFetching} overlayBlur={2} />
      {datasets?.map((dataset) => (
        <Card key={dataset.name} mb={"md"}>
          <Group position="apart">
            <Group spacing={5}>
              <Text>{dataset.name}</Text>

              <Text color={"dimmed"} size={"sm"} inline>
                ({dataset.count} {pluralize(dataset.count, "gezicht", "gezichten")})
              </Text>
            </Group>

            <Button color={"red"} onClick={() => openDeleteDatasetModal(dataset)}>
              <IconTrash />
            </Button>
          </Group>
        </Card>
      ))}
    </div>
  );
}
