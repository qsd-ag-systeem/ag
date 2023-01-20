import { Card, Group } from "@mantine/core";
import { IconMatchstick } from "@tabler/icons";
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
      <Group grow sx={{ alignItems: "stretch" }}>
        <Match
          customWidth
          dataset={match.dataset1}
          file_name={match.file1}
          percentage={match.score}
        />
        <Match
          customWidth
          dataset={match.dataset2}
          file_name={match.file2}
          image={`${API_URL}/image/${match.dataset2}/${match.file2}`}
        />
      </Group>
    </Card>
  );
}
