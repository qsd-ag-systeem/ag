import { Box, Button, Input, Progress, SimpleGrid, Text } from "@mantine/core";
import { closeAllModals } from "@mantine/modals";
import { showNotification } from "@mantine/notifications";
import { IconPlus, IconX } from "@tabler/icons";
import { useMemo, useState } from "react";
import { useSocket, useSocketEvent } from "socket.io-react-hook";
import { BodyEnroll } from "../../types";
import DirectoryBrowser from "../components/DirectoryBrowser";
import { env } from "../tools";

// const socket = io(env("API_URL"));

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

interface ServerToClientEvents {
  enroll: (data: EnrollData) => void;
}

interface ClientToServerEvents {
  enroll: (data: BodyEnroll) => void;
}

export default function Enroll() {
  const { socket } = useSocket<ServerToClientEvents, ClientToServerEvents>(env("API_URL"));

  const [name, setName] = useState("");
  const [location, setLocation] = useState("");

  const handleEnroll = async () => {
    const data: BodyEnroll = {
      name,
      folder: location,
    };

    if (data.name !== undefined && data.name.trim().length === 0) {
      data.name = undefined;
    }

    sendMessage<EnrollData>(data);
  };

  const onEnroll = (data: EnrollData | undefined) => {
    console.log("ENROLL");

    if (!data) return;

    if (data.status === "enrolled") {
      showNotification({
        title: "Enrollment voltooid",
        message: `De dataset: '${data.dataset}' is succesvol toegevoegd.`,
        color: "green",
        autoClose: false,
      });

      closeAllModals();
    }
  };

  const onCancel = () => {
    console.log("CANCEL");

    showNotification({
      title: "Enrollment geannuleerd",
      message: "",
      color: "red",
      autoClose: true,
    });

    closeAllModals();
  };

  const { lastMessage, sendMessage } = useSocketEvent<EnrollData | undefined>(socket, "enroll", {
    onMessage: onEnroll,
  });
  const { sendMessage: sendCancelMessage } = useSocketEvent(socket, "cancel", {
    onMessage: onCancel,
  });

  const onDirectoryChange = (dir: string) => {
    setLocation(dir);
  };

  const cancelEnroll = () => {
    sendCancelMessage({ folder: location });
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
          <Text>Naam</Text>
          <Input mb={10} value={name} onChange={e => setName(e.currentTarget.value)} />
          <DirectoryBrowser onChange={onDirectoryChange} />
        </Box>
      )}
      <SimpleGrid cols={2}>
        <Button
          color="red"
          variant="outline"
          leftIcon={<IconX size={14} />}
          onClick={cancelEnroll}
          // loading={status !== "idle"}
          // disabled={status !== "idle"}
        >
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
