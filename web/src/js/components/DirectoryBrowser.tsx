import { Anchor, Group, Loader, Text, Title } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { fetchDirectories } from "../api/directories";
import { IconArrowBack } from "@tabler/icons";

export default function DirectoryBrowser(props: any) {
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
    setDir(parentDir);
  };

  const setDir = (dir: string) => {
    setCurrentDir(dir)
    if (props.onChange) {
      props.onChange(dir)
    }
  }

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
          {data.map((item: string) => (
            <Text>
              <Anchor onClick={() => setDir(item)}>{item}</Anchor>
            </Text>
          ))}
        </>
      )}
    </>
  );
}
