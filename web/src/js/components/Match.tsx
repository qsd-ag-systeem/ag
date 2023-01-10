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
    ":hover": {
      cursor: "pointer",
    },
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
  },
}));

type MatchProps = {
  image?: string;
  percentage?: number;
  fileName?: string;
};

export default function Match({ image, percentage, fileName }: MatchProps) {
  const color = usePercentageColor(percentage);
  const { classes } = useStyles();

  return (
    <Flex
      className={classes.match}
      onClick={() =>
        openModal({
          children: <Image src={image} withPlaceholder width="60%" height="80%" />,
        })
      }
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
          aspectRatio: "1/1",
        }}
      >
        <Image
          src={image}
          alt={fileName}
          withPlaceholder
          imageProps={{
            loading: "lazy",
          }}
          width={240}
          height={240}
          draggable={false}
          radius="md"
        />
      </Box>
    </Flex>
  );
}
