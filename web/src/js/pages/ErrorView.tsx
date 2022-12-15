import { Button, Container, createStyles, Group, Text, Title } from "@mantine/core";

const useStyles = createStyles((theme) => ({
  root: {
    paddingTop: 40,
    paddingBottom: 40,
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

export function ErrorView() {
  const { classes } = useStyles();

  const forceReload = () => {
    window.location.reload();
  };

  return (
    <Container className={classes.root}>
      <Title className={classes.title}>Things didn't go as planned.</Title>
      <Title mb={"md"}></Title>

      <Text color="dimmed" size="lg" align="center" className={classes.description}>
        An error has occurred and the page has crashed. You can reload the application using the
        button below.
      </Text>
      <Group position="center">
        <Button variant="subtle" size="md" onClick={forceReload}>
          Reload the application
        </Button>
      </Group>
    </Container>
  );
}

export default ErrorView;
