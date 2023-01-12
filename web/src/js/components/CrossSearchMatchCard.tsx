import { Card, Group } from "@mantine/core";
import { CrossSearchResult } from "../../types";
import { API_URL } from "../constants";
import Match from "./Match";

type CrossSearchMatchCardProps = {
  match: CrossSearchResult;
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
        <Match
          disableModal
          image={`${API_URL}/image/${match.dataset1}/${match.file1}`}
          percentage={match.score}
        />
        <Match disableModal image={`${API_URL}/image/${match.dataset2}/${match.file2}`} />
      </Group>
    </Card>
  );
}
