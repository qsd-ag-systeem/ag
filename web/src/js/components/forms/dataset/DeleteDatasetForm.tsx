import { Button, Checkbox, Group, Input, TextInput, Text } from "@mantine/core";
import { useForm } from "@mantine/form";
import { BodyDeleteDataset, Dataset } from "../../../../types";

type DeleteDatasetFormProps = {
  dataset: Dataset;
  submitText?: string;
  submitAction: (values: BodyDeleteDataset) => void;
  cancelAction?: () => void;
  isLoading?: boolean;
};

export default function DeleteDatasetForm(props: DeleteDatasetFormProps) {
  const { dataset, submitText, submitAction, cancelAction, isLoading = false } = props;

  const form = useForm<BodyDeleteDataset>({
    initialValues: {
      dataset: dataset.id,
      files: [],
      remove_file: false,
    },
  });

  return (
    <form onSubmit={form.onSubmit((values) => submitAction(values))}>
      <TextInput
        label="Bestandsnamen"
        description="Voer de bestandsnamen in die je wilt verwijderen. Meerdere bestanden scheiden met een komma."
        placeholder="image1.png,image2.png"
        mb={"md"}
        onChange={(event) => {
          form.setFieldValue(
            "files",
            event.currentTarget.value.length > 0
              ? event.currentTarget.value.split(",").map((value) => value.trim())
              : []
          );
        }}
      />

      <Input.Wrapper label={"Bestanden verwijderen"} mb={"md"}>
        <Checkbox
          mt={"xs"}
          label={
            form.values.files.length > 0
              ? "Verwijder de ingevoerde bestanden van deze dataset"
              : "Verwijder alle bestanden van deze dataset"
          }
          {...form.getInputProps("remove_file", { type: "checkbox" })}
        />
      </Input.Wrapper>

      <Text size="sm" mb={"md"}>
        Je staat op het punt om dataset '{dataset.name}' en mogelijk bijbehorende bestanden te
        verwijderen uit het systeem. Dit is een permanente actie en kan niet ongedaan worden
        gemaakt. Weet je het zeker?
      </Text>

      <Group grow>
        <Button onClick={() => cancelAction?.()}>Annuleren</Button>
        <Button type="submit" color="red">
          {submitText ?? "Verwijderen"}
        </Button>
      </Group>
    </form>
  );
}
