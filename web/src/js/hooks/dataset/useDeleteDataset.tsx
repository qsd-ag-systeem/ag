import { useModals } from "@mantine/modals";
import { cleanNotifications, showNotification } from "@mantine/notifications";
import { IconCheck } from "@tabler/icons";
import { BodyDeleteDataset, Dataset } from "../../../types";
import { deleteDataset } from "../../api/datasets";
import DeleteDatasetForm from "../../components/forms/dataset/DeleteDatasetForm";
import useMutateDatasetData from "./useMutateDatasetData";

export default function useDeleteDataset() {
  const modals = useModals();

  const onSuccess = () => {
    cleanNotifications();

    showNotification({
      title: "Dataset verwijderd",
      message: `De dataset is succesvol verwijderd.`,
      autoClose: 10000,
      icon: <IconCheck />,
    });
  };

  const onError = (error: string) => {
    cleanNotifications();

    showNotification({
      title: `Er ging iets mis`,
      message: `Er is een fout opgetreden tijdens het verwijderen van de dataset. ${error}`,
      color: "red",
    });
  };

  const { mutate } = useMutateDatasetData(deleteDataset, onSuccess, onError);

  const onSubmit = async (values: BodyDeleteDataset) => {
    modals.closeAll();

    showNotification({
      disallowClose: true,
      loading: true,
      title: "Dataset verwijderen",
      message: "Bezig met verwijderen ...",
    });

    await mutate(values);
  };

  const openModal = (dataset: Dataset) => {
    modals.openModal({
      centered: true,
      title: "Weet je het zeker?",
      children: (
        <DeleteDatasetForm
          submitAction={onSubmit}
          cancelAction={() => modals.closeAll()}
          dataset={dataset}
        />
      ),
    });
  };

  return {
    openModal,
  };
}
