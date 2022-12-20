import { Container, Title, Input, Text, Button, SimpleGrid, Transition, Paper, Progress } from "@mantine/core";
import DirectoryBrowser from "../components/DirectoryBrowser";
import { enroll } from "../api/enroll";
import { IconPlus, IconX } from "@tabler/icons";
import { useState, useEffect } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

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
  const [enrollData, setEnrollData] = useState<any>(null);
  const [failedFiles, setFailedFiles] = useState<string[]>([]);
  const [enrollFolder, setEnrollFolder] = useState<string>("");


  const handleEnroll = async () => {
    setEnrollStatus(EnrollStatus.Enrolling);
    setEnrollError(null);
    setEnrollData(null);
    setFailedFiles([]);
    setEnrollFolder(location + "");

    console.log("Enroll folder " + enrollFolder + ", location: " + location);

    try {
      const data = await enroll(location);
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

  useEffect(() => {
    socket.on("connect", () => {
      console.log("connected to socket");
    })

    socket.on("enroll", (data: any) => {
      console.log(data);

      // if (data.folder !== enrollFolder) {
      //   console.log(data.folder + " !== " + enrollFolder)
      //   return;
      // }

      if (data.success === false) {
        setFailedFiles((prev) => [...prev, data.file]);
      }

      if (data.current === data.total) {
        setEnrollStatus(EnrollStatus.Enrolled);
      }
      
      setEnrollData(data);
    })

    return () => {
      socket.off("connect");
      socket.off("enroll");
    }
  }, []);


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
      {enrollStatus !== EnrollStatus.Idle && enrollData !== null && (
        <div>
          <div style={{ marginTop: 15 }}>
            <div style={{ marginBottom: 10 }}>
              <Text>
                File: {enrollData?.file}
              </Text>
            </div>
            <Progress size="xl" value={
              enrollData?.current !== undefined ? (enrollData.current / enrollData.total) * 100 : 0
            } striped animate />
          </div>

          <Text>Failed files:</Text>
          <div style={{ marginTop: 15, overflowY: "auto", maxHeight: 300, backgroundColor: "#CCC", borderRadius: "15px", padding: "10px" }}>
            <Text>
              {failedFiles.map((file, i) => (
                <div key={i}>
                  {file}
                </div>
              ))}
            </Text>
          </div>
        </div>
      )}
    </Container>
  );
}
