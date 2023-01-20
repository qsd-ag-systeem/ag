import { Box, Text } from "@mantine/core";
import { SearchResult } from "../../types";
import usePercentageColor from "../hooks/usePercentageColor";

const Similarity = ({ percentage }: { percentage: SearchResult["similarity"] }) => {
  const color = usePercentageColor(percentage);

  return (
    <Box
      sx={theme => ({
        backgroundColor: color,
        zIndex: 2,
        borderRadius: theme.radius.md,
        padding: theme.spacing.xs,
        left: theme.spacing.xs,
        top: theme.spacing.xs,
        position: "absolute",
      })}
    >
      <Text size={"xs"} color="white" weight={"bold"}>
        {percentage}%
      </Text>
    </Box>
  );
};

export default Similarity;
