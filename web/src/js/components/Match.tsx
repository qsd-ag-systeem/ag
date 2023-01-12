import { Badge, Box, createStyles, Flex, Image, Text, Button, Divider, Group } from "@mantine/core";
import usePercentageColor from "../hooks/usePercentageColor";
import { openModal } from "@mantine/modals";
import { useCallback } from "react";

const useStyles = createStyles(theme => ({
  match: {
    position: "relative",
    userSelect: "none",
    scrollSnapAlign: "start",
    scrollMargin: theme.spacing.sm,
  },
  percentage: {
    zIndex: 2,
    borderRadius: theme.radius.md,
    padding: theme.spacing.xs,
    left: theme.spacing.xs,
    top: theme.spacing.xs,
    position: "absolute",
  },
  fileName: {
    zIndex: 2,
    left: theme.spacing.xs,
    bottom: theme.spacing.xs,
    position: "absolute",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",

    maxWidth: "90%",
  },
}));

type MatchProps = {
  image?: string;
  percentage?: number;
  fileName?: string;
  inputFile?: string;
  dataset?: string;
  isModal?: boolean;
};

export default function Match({
  image,
  percentage,
  fileName,
  dataset,
  inputFile,
  isModal = false,
}: MatchProps) {
  const color = usePercentageColor(percentage);
  const { classes } = useStyles();

  return (
    <Flex
      className={classes.match}
      sx={{
        cursor: isModal ? "auto" : "pointer",
      }}
      onClick={() => {
        openModal({
          size: "auto",
          overlayBlur: 2,
          title: (
            <Group sx={{ justifyContent: "space-between" }}>
              <Group fw={500}>
                Dataset: <Text fz="sm">{dataset}</Text>
              </Group>
              <Divider />
              <Group fw={500}>
                Input: <Text fz="sm">{inputFile}</Text>
              </Group>
            </Group>
          ),
          children: (
            <Match fileName={fileName} percentage={percentage} image={image} isModal={true} />
          ),
        });
      }}
    >
      {color && (
        <Box
          className={classes.percentage}
          sx={{
            backgroundColor: color,
          }}
        >
          <Text size={"xs"} color="white" weight={"bold"}>
            {percentage}%
          </Text>
        </Box>
      )}
      {fileName && (
        <Badge opacity={1} className={classes.fileName}>
          {fileName}
        </Badge>
      )}
      <Box
        sx={{
          aspectRatio: !isModal ? "1/1" : undefined,
        }}
      >
        <Image
          src={image}
          alt={fileName}
          withPlaceholder
          imageProps={{
            loading: "lazy",
          }}
          width={isModal ? undefined : 240}
          height={isModal ? 600 : 240}
          sx={{ minWidth: isModal ? 600 : 240, minHeight: isModal ? 600 : 240 }}
          draggable={false}
          radius="md"
        />
      </Box>
    </Flex>
  );
}
