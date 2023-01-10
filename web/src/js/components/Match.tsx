import { Badge, Box, createStyles, Flex, Image, Text, Button } from "@mantine/core";
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
    right: theme.spacing.xs,
    top: theme.spacing.xs,
    position: "absolute",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
    maxWidth: 160,
  },
}));

type MatchProps = {
  image?: string;
  percentage?: number;
  fileName?: string;
  isModal?: boolean;
};

export default function Match({ image, percentage, fileName, isModal = false }: MatchProps) {
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
          title: fileName,
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
      {fileName && <Badge className={classes.fileName}>{fileName}</Badge>}
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
          width={isModal ? 800 : 240}
          height={isModal ? 800 : 240}
          draggable={false}
          radius="md"
        />
      </Box>
    </Flex>
  );
}
