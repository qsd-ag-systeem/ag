import { AutocompleteItem, Button } from "@mantine/core";
import { useForm } from "@mantine/form";
import { BodyCrossSearch, Dataset } from "../../../types";
import { fetchDatasets } from "../../api/datasets";
import { FancySelect } from "../selects/FancySelect";

type CrossSearchFormProps = {
  submitText?: string;
  submitAction: (values: BodyCrossSearch) => void;
  isLoading?: boolean;
};

function CrossSearchForm(props: CrossSearchFormProps) {
  const { submitText, submitAction, isLoading = false } = props;

  const form = useForm<BodyCrossSearch>({
    initialValues: {
      dataset1: "",
      dataset2: "",
    },

    validate: {
      dataset1: (value) => (value ? null : "Dit veld is verplicht"),
      dataset2: (value) => (value ? null : "Dit veld is verplicht"),
    },
  });

  return (
    <form onSubmit={form.onSubmit((values) => submitAction(values))}>
      <FancySelect<Dataset>
        error={form.errors.dataset1 ?? null}
        required
        pb={"sm"}
        label={"Dataset 1"}
        placeholder={"Zoek een dataset"}
        onClear={() => form.setFieldValue("dataset1", "")}
        onItemSubmit={(item: AutocompleteItem) => form.setFieldValue("dataset1", item.data.name)}
        queryFn={(query: string) => fetchDatasets(query)}
        labelRenderer={(item: Dataset) => item.name}
      />

      <FancySelect<Dataset>
        error={form.errors.dataset2 ?? null}
        required
        pb={"sm"}
        label={"Dataset 2"}
        placeholder={"Zoek een dataset"}
        onClear={() => form.setFieldValue("dataset2", "")}
        onItemSubmit={(item: AutocompleteItem) => form.setFieldValue("dataset2", item.data.name)}
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
