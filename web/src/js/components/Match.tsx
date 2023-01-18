import { Badge, Box, createStyles, Flex, Image, Text, Button, Divider, Group } from "@mantine/core";
import usePercentageColor from "../hooks/usePercentageColor";
import { openModal } from "@mantine/modals";
import FacialImage, { FacialImageProps } from "./FacialImage";

const useStyles = createStyles(theme => ({
  match: {
    position: "relative",
    userSelect: "none",
    scrollSnapAlign: "start",
    scrollMargin: theme.spacing.sm,
  },
  percentage: {
    zIndex: 2,
    borderRadius: theme.radius.md,
    padding: theme.spacing.xs,
    left: theme.spacing.xs,
    top: theme.spacing.xs,
    position: "absolute",
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
  disableModal?: boolean;
} & FacialImageProps;

export default function Match(props: MatchProps) {
  const color = usePercentageColor(props.percentage);
  const { classes } = useStyles();

  return (
    <Flex
      className={classes.match}
      sx={{
        cursor: props.isModal ? "auto" : "pointer",
      }}
      onClick={props.onClick}
      // onClick={() => {
      //   !props.disableModal &&
      //     openModal({
      //       size: "auto",
      //       overlayBlur: 2,
      //       title: (
      //         <Group sx={{ justifyContent: "space-between" }}>
      //           <Group fw={500}>
      //             Dataset: <Text fz="sm">{props.dataset}</Text>
      //           </Group>
      //           <Divider />
      //           <Group fw={500}>
      //             Input: <Text fz="sm">{props.file_name}</Text>
      //           </Group>
      //         </Group>
      //       ),
      //       children: <Match {...props} isModal={true} />,
      //     });
      // }}
    >
      <Box
        sx={{
          aspectRatio: !props.isModal ? "1/1" : undefined,
          minWidth: props.isModal ? 600 : 240,
          minHeight: props.isModal ? 600 : 240,
          width: props.isModal ? undefined : 240,
          height: props.isModal ? 600 : 240,
          position: "relative",
          overflow: "hidden",
        }}
      >
        {color && (
          <Box
            className={classes.percentage}
            sx={{
              backgroundColor: color,
            }}
          >
            <Text size={"xs"} color="white" weight={"bold"}>
              {props.percentage}%
            </Text>
          </Box>
        )}
        {props.file_name && (
          <Badge opacity={1} className={classes.fileName}>
            {props.file_name}
          </Badge>
        )}
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
