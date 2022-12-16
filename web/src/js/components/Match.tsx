import { Flex, Box, createStyles, Text, Image } from "@mantine/core";
import usePercentageColor from "../hooks/usePercentageColor";

const useStyles = createStyles(theme => ({
  match: { position: "relative", userSelect: "none" },
  percentage: {
    zIndex: 2,
    borderRadius: theme.radius.md,
    padding: theme.spacing.xs,
    left: theme.spacing.xs,
    top: theme.spacing.xs,
    position: "absolute",
  },
}));

type MatchProps = {
  image: string;
  percentage: number;
};

export default function Match({ image, percentage }: MatchProps) {
  const color = usePercentageColor(percentage);
  const { classes } = useStyles();

  return (
    <Flex className={classes.match}>
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
      <Box
        sx={{
          aspectRatio: "1/1",
        }}
      >
        <Image src={image} width={240} height={240} draggable={false} radius="md" />
      </Box>
    </Flex>
  );
}
