import { Box, Button, Anchor, Group, Header as MantineHeader } from "@mantine/core";
import { Link, useNavigate } from "react-router-dom";
import AppIcon from "./icons/AppIcon";

export function Header() {
  return (
    <Box>
      <MantineHeader height={60} px="md">
        <Group position="apart" sx={{ height: "100%" }}>
          <Anchor component={Link} to={"/"}>
            <AppIcon height={50} />
          </Anchor>

          <Group>
            <Button disabled>Log in</Button>
          </Group>
        </Group>
      </MantineHeader>
    </Box>
  );
}
