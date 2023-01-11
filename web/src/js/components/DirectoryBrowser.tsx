import { Anchor, Group, Loader, Text, Title } from "@mantine/core";
import { useState } from "react";
import useDirectoriesData from "../hooks/useDirectoriesData";
import { IconArrowBack } from "@tabler/icons";

export default function DirectoryBrowser(props: any) {
  const [currentDir, setCurrentDir] = useState("");

  const { data, isFetching } = useDirectoriesData(currentDir);

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
          {data.data.map((item: string) => (
            <Text key={Math.random()}>
              <Anchor onClick={() => setDir(item)}>{item}</Anchor>
            </Text>
          ))}
        </>
      )}
    </>
  );
}
