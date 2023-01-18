import { Button, LoadingOverlay, Table, Text, Title, Box, Paper } from "@mantine/core";
import { IconArrowBack, IconFolder } from "@tabler/icons";
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

  const setDir = (dir: string) => {
    setCurrentDir(dir);
    onUpdate?.(dir.replace(/\\/g, "/"));
  };

  return (
    <Box sx={{ position: "relative", height: "100%", display: "flex", flexDirection: "column" }}>
      <Paper radius={0} withBorder px="sm" py={5}>
        <Title order={5}>{currentDir || "/"}</Title>
      </Paper>
      <Box sx={{ flexGrow: 1, overflowY: "scroll" }}>
        <LoadingOverlay visible={isFetching} overlayBlur={2} transitionDuration={500} />
        <Table striped highlightOnHover withBorder withColumnBorders>
          <tbody>
            <tr>
              {currentDir && (
                <Button
                  leftIcon={<IconArrowBack />}
                  variant="subtle"
                  sx={{ display: "flex", width: "100%" }}
                  onClick={goToParentDir}
                >
                  <Text>Parent directory</Text>
                </Button>
              )}
            </tr>
            {data?.data?.map((item: string, idx: number) => (
              <tr key={idx}>
                <Button
                  leftIcon={<IconFolder />}
                  variant="subtle"
                  sx={{ display: "flex", width: "100%" }}
                  onClick={() => setDir(item)}
                >
                  {item}
                </Button>
              </tr>
            ))}
          </tbody>
        </Table>
      </Box>
    </Box>
  );
}
