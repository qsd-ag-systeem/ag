import { Badge, Box, createStyles, Flex } from "@mantine/core";
import FacialImage, { FacialImageProps } from "./FacialImage";
import Similarity from "./Similarity";

const useStyles = createStyles((theme) => ({
  match: {
    position: "relative",
    userSelect: "none",
    scrollSnapAlign: "start",
    scrollMargin: theme.spacing.sm,
  },
  fileName: {
    zIndex: 2,
    left: theme.spacing.xs,
    bottom: theme.spacing.xs,
    position: "absolute",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
    maxWidth: "90%",
  },
}));

type MatchProps = {
  image?: string;
  percentage?: number;
  isModal?: boolean;
  customWidth?: boolean;
} & FacialImageProps;

export default function Match(props: MatchProps) {
  const { classes } = useStyles();

  return (
    <Flex
      className={classes.match}
      sx={{
        cursor: props.isModal ? "auto" : "pointer",
      }}
      onClick={props.onClick}
    >
      {props.percentage && <Similarity percentage={props.percentage} />}
      {props.file_name && (
        <Badge opacity={1} className={classes.fileName}>
          {props.file_name}
        </Badge>
      )}
      <Box
        sx={{
          aspectRatio: !props.isModal ? "1/1" : undefined,

          position: "relative",
          overflow: "hidden",
          ...(!props.customWidth
            ? {
                minWidth: props.isModal ? 600 : 240,
                minHeight: props.isModal ? 600 : 240,
                width: props.isModal ? undefined : 240,
                height: props.isModal ? 600 : 240,
              }
            : {}),
        }}
      >
        <FacialImage
          draggable={false}
          radius="md"
          imageProps={{
            loading: "lazy",
          }}
          sx={{ backgroundPosition: "center", objectFit: "cover", objectPosition: "center" }}
          {...props}
        />
      </Box>
    </Flex>
  );
}
