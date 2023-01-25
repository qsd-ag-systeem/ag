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
import { useContext } from "react";
import { Link } from "react-router-dom";
import { FacialBorderContext } from "../providers/facial-borders";
import AppIcon from "./icons/AppIcon";

export function Header() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  const { facialBorderVisible, setFacialBorderVisible } = useContext(FacialBorderContext);
  const dark = colorScheme === "dark";

  return (
    <Box>
      <MantineHeader height={60} px="md">
        <Group position="apart" sx={{ height: "100%" }}>
          <Group spacing={"md"}>
            <Group>
              <Anchor component={Link} to={"/"}>
                Zoeken
              </Anchor>

              <Anchor component={Link} to={"/cross-search"}>
                Kruiszoeken
              </Anchor>
            </Group>
          </Group>

          <Group>
            <Button onClick={() => setFacialBorderVisible(!facialBorderVisible)}>
              Toggle Facial Borders
            </Button>
            <ActionIcon
              variant="outline"
              color={dark ? "yellow" : "blue"}
              onClick={() => toggleColorScheme()}
              title="Toggle color scheme"
              size={36}
            >
              {dark ? <IconSun size={18} /> : <IconMoonStars size={18} />}
            </ActionIcon>
          </Group>
        </Group>
      </MantineHeader>
    </Box>
  );
}
