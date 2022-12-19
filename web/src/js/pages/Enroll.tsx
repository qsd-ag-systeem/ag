import { Container, Title, Input, Text, Button, SimpleGrid, Transition, Paper } from "@mantine/core";
import DirectoryBrowser from "../components/DirectoryBrowser";
import { enroll } from "../api/enroll";
import { IconPlus, IconX } from "@tabler/icons";
import { useState } from "react";

export default function Enroll() {
  const EnrollStatus = {
    Idle: 0,
    Enrolling: 1,
    Enrolled: 2
  }

  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [enrollStatus, setEnrollStatus] = useState(EnrollStatus.Idle);
  const [enrollError, setEnrollError] = useState<string | null>(null);

  const handleEnroll = async () => {
    setEnrollStatus(EnrollStatus.Enrolling);
    setEnrollError(null);

    try {
      const data = await enroll(location);
      if (data.success === false) {
        throw new Error(data.message);
      }
      setEnrollStatus(EnrollStatus.Enrolled);
      console.log(data);
    } catch (e: any) {
      setEnrollStatus(EnrollStatus.Idle);
      setEnrollError(e.message);

      console.log(e.message);
    }
  };

  const onDirectoryChange = (dir: string) => {
    setLocation(dir);
  };

  return (
    <Container fluid>
      <Title>Dataset toevoegen</Title>
      <Transition mounted={enrollError !== null} transition="fade" duration={400} timingFunction="ease">
        {(styles) => (
          <Paper shadow="xs" p="md" radius="md" bg="red" style={{ ...styles, marginTop: 15, marginBottom: 15 }}>
            <Text color="white">
              {enrollError !== undefined ? enrollError : "Er is een onbekende fout opgetreden."}
            </Text>
          </Paper>
        )}
      </Transition>
      {enrollStatus === EnrollStatus.Enrolled && (
        <Transition mounted={enrollStatus === EnrollStatus.Enrolled} transition="fade" duration={400} timingFunction="ease">
          {(styles) => (
            <Paper shadow="xs" p="md" radius="md" bg="green" style={{ ...styles, marginTop: 15, marginBottom: 15 }}>
              <Text color="white">
                Dataset is toegevoegd.
              </Text>
            </Paper>
          )}
        </Transition>
      )}
      <Text>Naam</Text>
      <Input mb={10} value={name} onChange={(e) => setName(e.currentTarget.value)} />
      <Text>Locatie</Text>
      <div style={{ marginBottom: 10 }}>
        <DirectoryBrowser onChange={onDirectoryChange} />
      </div>
      <SimpleGrid cols={2}>
        <Button variant="gradient" gradient={{ from: "indigo", to: "cyan" }} leftIcon={<IconPlus size={14} />} onClick={handleEnroll} loading={enrollStatus === EnrollStatus.Enrolling} disabled={enrollStatus === EnrollStatus.Enrolling}>
          {enrollStatus === EnrollStatus.Enrolling ? "Bezig met enrollment..." : "Toevoegen"}
        </Button>
        <Button color="red" variant="outline" leftIcon={<IconX size={14} />}>Annuleren</Button>
      </SimpleGrid>
    </Container>
  );
}
