import { Anchor, Group, Loader, Text, Title } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { fetchDirectories } from "../api/directories";
import { IconArrowBack } from "@tabler/icons";

export default function DirectoryBrowser() {
  const [currentDir, setCurrentDir] = useState("");

  const { data, isFetching } = useQuery(
    ["directories", currentDir],
    () => fetchDirectories(currentDir),
    {
      keepPreviousData: true,
    }
  );

  const goToParentDir = () => {
    let parentDir = currentDir.replace(/\\/g, "/").split("/").slice(0, -1).join("/");
    setCurrentDir(parentDir);
  };

  return (
    <>
      {isFetching ? (
        <Loader />
      ) : (
        <>
          <Title order={5}>{currentDir}</Title>
          {currentDir && (
            <Text>
              <Anchor onClick={goToParentDir}>
                <Group spacing={5}>
                  <IconArrowBack />
                  <Text>Parent directory</Text>
                </Group>
              </Anchor>
            </Text>
          )}
          {data.data.map((item: string) => (
            <Text key={Math.random()}>
              <Anchor onClick={() => setCurrentDir(item)}>{item}</Anchor>
            </Text>
          ))}
        </>
      )}
    </>
  );
}
