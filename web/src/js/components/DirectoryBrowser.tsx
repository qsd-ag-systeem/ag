import { Anchor, Group, Loader, Text, Title } from "@mantine/core";
import { IconArrowBack } from "@tabler/icons";
import { useState } from "react";
import useDirectoriesData from "../hooks/useDirectoriesData";

type DirectoryBrowserProps = {
  onUpdate?: (currentDir: string) => void;
};

export default function DirectoryBrowser(props: DirectoryBrowserProps) {
  const { onUpdate } = props;
  const [currentDir, setCurrentDir] = useState("");

  const { data, isFetching } = useDirectoriesData(currentDir);

  const goToParentDir = () => {
    let parentDir = currentDir.replace(/\\/g, "/").split("/").slice(0, -1).join("/");
    setCurrentDir(parentDir);
    onUpdate?.(parentDir);
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
