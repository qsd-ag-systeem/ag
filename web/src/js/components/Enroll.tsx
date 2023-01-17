import { Box, Button, Input, Progress, SimpleGrid, Text } from "@mantine/core";
import { closeAllModals } from "@mantine/modals";
import { showNotification } from "@mantine/notifications";
import { IconPlus, IconX } from "@tabler/icons";
import { useMemo, useState } from "react";
import { useSocket, useSocketEvent } from "socket.io-react-hook";
import { BodyEnroll } from "../../types";
import DirectoryBrowser from "./DirectoryBrowser";
import { env } from "../tools";
import { useQueryClient } from "@tanstack/react-query";

interface EnrollData {
  success: boolean;
  file: string;
  dataset: string;
  filesProcessed: number;
  totalFiles: number;
  status: "idle" | "processing" | "enrolled";
  folder: string;
  progress: number;
}

interface EnrollCancelData {
  success: boolean;
}

interface EnrollErrorData {
  message: string;
}

interface ServerToClientEvents {
  enroll: (data: EnrollData) => void;
}

interface ClientToServerEvents {
  enroll: (data: BodyEnroll) => void;
}

export default function Enroll() {
  const { socket } = useSocket<ServerToClientEvents, ClientToServerEvents>(env("API_URL"));
  const queryClient = useQueryClient();

  const [location, setLocation] = useState("");

  const handleEnroll = async () => {
    const data: BodyEnroll = {
      folder: location,
    };

    if (data.name !== undefined && data.name.trim().length === 0) {
      data.name = undefined;
    }

    sendEnrollMessage<EnrollData>(data);
  };

  const onEnroll = (data: EnrollData | undefined) => {
    if (!data) return;

    if (data.status === "enrolled") {
      showNotification({
        title: "Enrollment voltooid",
        message: `De dataset: '${data.dataset}' is succesvol toegevoegd.`,
        color: "green",
        autoClose: false,
      });

      queryClient.invalidateQueries("datasets");

      closeAllModals();
    }
  };

  const onCancel = (data: EnrollCancelData | undefined) => {
    if (data === undefined) return;

    showNotification({
      title: "Enrollment geannuleerd",
      message: "",
      color: "red",
      autoClose: true,
    });

    closeAllModals();
  };

  const onError = (data: EnrollErrorData | undefined) => {
    if (data === undefined) return;

    showNotification({
      title: "Enrollment mislukt",
      message: data.message,
      color: "red",
      autoClose: true,
    });
  };

  const { lastMessage, sendMessage: sendEnrollMessage } = useSocketEvent<EnrollData | undefined>(
    socket,
    "enroll",
    {
      onMessage: onEnroll,
    }
  );

  const { sendMessage: sendCancelMessage } = useSocketEvent<EnrollCancelData | undefined>(
    socket,
    "cancel",
    {
      onMessage: onCancel,
    }
  );

  useSocketEvent<EnrollErrorData | undefined>(socket, "err", {
    onMessage: onError,
  });

  const onDirectoryChange = (dir: string) => {
    setLocation(dir);
  };

  const cancelEnroll = () => {
    if (status === "processing") {
      sendCancelMessage({ folder: location });
    } else {
      closeAllModals();
    }
  };

  const status = useMemo(() => (lastMessage ? lastMessage.status : "idle"), [lastMessage]);

  const progress = useMemo(() => (lastMessage ? lastMessage.progress : 0), [lastMessage]);

  return (
    <Box>
      {status !== "idle" && (
        <Box mb="md">
          <Progress size="xl" value={progress} />
        </Box>
      )}

      {status === "idle" && (
        <Box mb="xs">
          <DirectoryBrowser onUpdate={onDirectoryChange} />
        </Box>
      )}
      <SimpleGrid cols={2}>
        <Button color="red" variant="outline" leftIcon={<IconX size={14} />} onClick={cancelEnroll}>
          Annuleren
        </Button>
        <Button
          leftIcon={<IconPlus size={14} />}
          onClick={handleEnroll}
          loading={status !== "idle"}
          disabled={status !== "idle"}
        >
          Toevoegen
        </Button>
      </SimpleGrid>
    </Box>
  );
}
