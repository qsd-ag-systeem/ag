import {
  ActionIcon,
  Anchor,
  Box,
  Button,
  Group,
  Header as MantineHeader,
  useMantineColorScheme,
} from "@mantine/core";
import { IconMoonStars, IconSun } from "@tabler/icons";
import { Link } from "react-router-dom";
import AppIcon from "./icons/AppIcon";

export function Header() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  const dark = colorScheme === "dark";

  return (
    <Box>
      <MantineHeader height={60} px="md">
        <Group position="apart" sx={{ height: "100%" }}>
          <Anchor component={Link} to={"/"}>
            <AppIcon height={50} />
          </Anchor>

          <Group>
            <Button disabled>Log in</Button>
            <ActionIcon
              variant="outline"
              color={dark ? "yellow" : "blue"}
              onClick={() => toggleColorScheme()}
              title="Toggle color scheme"
            >
              {dark ? <IconSun size={18} /> : <IconMoonStars size={18} />}
            </ActionIcon>
          </Group>
        </Group>
      </MantineHeader>
    </Box>
  );
}
