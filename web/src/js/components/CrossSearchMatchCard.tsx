import { Card, CardProps, Group, PaperStylesParams } from "@mantine/core";
import { DefaultProps } from "@mantine/styles";
import { SearchResult } from "../../types";
import Match from "./Match";

type CrossSearchMatchCardProps = {
  match: SearchResult;
  onClick?: () => void;
};

export default function CrossSearchMatchCard(props: CrossSearchMatchCardProps) {
  const { match, onClick } = props;

  return (
    <Card
      withBorder
      p={"sm"}
      mb={"sm"}
      onClick={onClick}
      sx={{ cursor: onClick ? "pointer" : undefined }}
    >
      <Group grow>
        <Match disableModal percentage={match.similarity} />
        <Match disableModal />
      </Group>
    </Card>
  );
}
