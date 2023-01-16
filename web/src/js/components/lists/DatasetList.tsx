import { Button, Card, Checkbox, Group, LoadingOverlay, Stack, Text } from "@mantine/core";
import { IconTrash } from "@tabler/icons";
import { useEffect, useState } from "react";
import useDatasetsData from "../../hooks/dataset/useDatasetsData";
import useDeleteDataset from "../../hooks/dataset/useDeleteDataset";
import { pluralize } from "../../tools";

type DatasetListProps = {
  onUpdateSelected?: (selected: string[]) => void;
};

export default function DatasetList(props: DatasetListProps) {
  const { onUpdateSelected } = props;
  const { data: datasets, isFetching } = useDatasetsData();
  const { openModal: openDeleteDatasetModal } = useDeleteDataset();
  const [selected, setSelected] = useState<string[]>([]);

  const updateSelected = (id: string, value: boolean) => {
    value ? setSelected([...selected, id]) : setSelected(selected.filter((item) => item !== id));
  };

  useEffect(() => {
    onUpdateSelected?.(selected);
  }, [selected]);

  return (
    <div style={{ position: "relative" }}>
      <LoadingOverlay visible={isFetching} overlayBlur={2} />
      {datasets?.map((dataset) => (
        <Card shadow="sm" key={dataset.name} mb={"sm"}>
          <Group>
            <Checkbox
              sx={{ display: "flex" }}
              onChange={(event) => updateSelected(dataset.id, event.currentTarget.checked)}
            />
            <Group position="apart" sx={{ flexGrow: 1 }}>
              <Stack spacing={5}>
                <Text>{dataset.name}</Text>

                <Text color={"dimmed"} size={"sm"} inline>
                  {dataset.count} {pluralize(dataset.count, "gezicht", "gezichten")}
                </Text>
              </Stack>

              <Button color={"red"} onClick={() => openDeleteDatasetModal(dataset)}>
                <IconTrash />
              </Button>
            </Group>
          </Group>
        </Card>
      ))}
    </div>
  );
}
