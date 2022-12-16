import { Button, Container, createStyles, Group, Text, Title } from "@mantine/core";
import { useNavigate } from "react-router-dom";

const useStyles = createStyles((theme) => ({
  root: {
    paddingTop: 40,
    paddingBottom: 40,
  },

  label: {
    textAlign: "center",
    fontWeight: 900,
    fontSize: 220,
    lineHeight: 1,
    marginBottom: theme.spacing.xl * 1.5,
    color: theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[2],

    [theme.fn.smallerThan("sm")]: {
      fontSize: 120,
    },
  },

  title: {
    fontFamily: `Greycliff CF, ${theme.fontFamily}`,
    textAlign: "center",
    fontWeight: 900,
    fontSize: 38,

    [theme.fn.smallerThan("sm")]: {
      fontSize: 32,
    },
  },

  description: {
    maxWidth: 500,
    margin: "auto",
    marginTop: theme.spacing.xl,
    marginBottom: theme.spacing.xl * 1.5,
  },
}));

export default function NotFound() {
  const { classes } = useStyles();
  const navigate = useNavigate();

  return (
    <Container className={classes.root}>
      <div className={classes.label}>404</div>
      <Title className={classes.title}>Page Not Found</Title>
      <Text color="dimmed" size="lg" align="center" className={classes.description}>
        It looks like you have lost your way! You might have entered a wrong address, or the page
        has moved to another location.
      </Text>
      <Group position="center">
        <Button variant="subtle" size="md" onClick={() => navigate("/")}>
          Return to the home page
        </Button>
      </Group>
    </Container>
  );
}
