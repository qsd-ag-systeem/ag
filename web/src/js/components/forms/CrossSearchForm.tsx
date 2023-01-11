import { AutocompleteItem, Button } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useLogger } from "@mantine/hooks";
import { Dataset } from "../../../types";
import { fetchDatasets } from "../../api/datasets";
import { FancySelect } from "../selects/FancySelect";

export type CrossSearchFormValues = {
  dataset_1: string;
  dataset_2: string;
};

type CrossSearchFormProps = {
  submitText?: string;
  submitAction: (values: CrossSearchFormValues) => void;
  isLoading?: boolean;
};

function CrossSearchForm(props: CrossSearchFormProps) {
  const { submitText, submitAction, isLoading = false } = props;

  const form = useForm<CrossSearchFormValues>({
    initialValues: {
      dataset_1: "",
      dataset_2: "",
    },

    validate: {
      dataset_1: (value) => (value ? null : "Dit veld is verplicht"),
      dataset_2: (value) => (value ? null : "Dit veld is verplicht"),
    },
  });

  return (
    <form onSubmit={form.onSubmit((values) => submitAction(values))}>
      <FancySelect<Dataset>
        error={form.errors.dataset_1 ?? null}
        required
        pb={"sm"}
        label={"Dataset 1"}
        placeholder={"Zoek een dataset"}
        onClear={() => form.setFieldValue("dataset_1", "")}
        onItemSubmit={(item: AutocompleteItem) => form.setFieldValue("dataset_1", item.data.name)}
        queryFn={(query: string) => fetchDatasets(query)}
        labelRenderer={(item: Dataset) => item.name}
      />

      <FancySelect<Dataset>
        error={form.errors.dataset_2 ?? null}
        required
        pb={"sm"}
        label={"Dataset 2"}
        placeholder={"Zoek een dataset"}
        onClear={() => form.setFieldValue("dataset_2", "")}
        onItemSubmit={(item: AutocompleteItem) => form.setFieldValue("dataset_2", item.data.name)}
        queryFn={(query: string) => fetchDatasets(query)}
        labelRenderer={(item: Dataset) => item.name}
      />

      <Button loading={isLoading} type="submit" fullWidth>
        {submitText ?? "Zoek"}
      </Button>
    </form>
  );
}

export default CrossSearchForm;
