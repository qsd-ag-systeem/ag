import { useMantineTheme } from "@mantine/core";

export default function usePercentageColor(percentage?: number) {
  const theme = useMantineTheme();

  if (!percentage) return undefined;

  if (percentage < 50) {
    return theme.colors.red[7];
  }

  if (percentage < 75) {
    return theme.colors.yellow[7];
  }

  return theme.colors.green[7];
}
