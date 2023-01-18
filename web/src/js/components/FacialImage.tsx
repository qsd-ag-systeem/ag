import { Image, ImageProps } from "@mantine/core";
import { useEffect, useRef } from "react";
import { API_URL } from "../constants";

export type FacialImageProps = {
  dataset: string;
  file_name: string;
  top_left?: number[];
  bottom_right?: number[];
  width?: number;
  height?: number;
  debug?: boolean;
} & ImageProps;

export default function FacialImage(props: FacialImageProps) {
  const { dataset, file_name, top_left, bottom_right, width = 0, height = 0, ...restProps } = props;
  const shouldDrawRectangle = top_left && bottom_right;

  const imageRef = useRef<HTMLImageElement>(null);
  const rectangleRef = useRef<HTMLDivElement>(null);

  const getContainedSize = (img: HTMLImageElement) => {
    var ratio = img.naturalWidth / img.naturalHeight;
    var width = img.height * ratio;
    var height = img.height;

    if (width > img.width) {
      width = img.width;
      height = img.width / ratio;
    }

    return [width, height];
  };

  const drawRectangle = () => {
    if (!shouldDrawRectangle || !imageRef.current) return;

    let [imageWidth, imageHeight] = getContainedSize(imageRef.current);

    let widthFactor = imageWidth / width;
    let heightFactor = imageHeight / height;

    let top_distance = top_left![1] * heightFactor - 5;
    let left_distance = top_left![0] * heightFactor - 5;
    let rectangleWidth = (bottom_right![0] - top_left![0]) * widthFactor + 10;
    let rectangleHeight = (bottom_right![1] - top_left![1]) * heightFactor + 10;

    rectangleRef.current!.style.top = `${top_distance}px`;
    rectangleRef.current!.style.left = `${left_distance}px`;
    rectangleRef.current!.style.width = `${rectangleWidth}px`;
    rectangleRef.current!.style.height = `${rectangleHeight}px`;
  };

  useEffect(() => {
    window.addEventListener("resize", drawRectangle);

    return () => {
      window.removeEventListener("resize", drawRectangle);
    };
  });

  useEffect(() => {
    drawRectangle();
  }, [top_left, bottom_right]);

  const onLoad = () => drawRectangle();

  return (
    <div style={{ position: "relative", height: "100%" }}>
      {shouldDrawRectangle && (
        <div
          ref={rectangleRef}
          style={{
            zIndex: 1,
            position: "absolute",
            border: "3px solid red",
          }}
        />
      )}
      <Image
        onLoad={onLoad}
        imageRef={imageRef}
        width={"100%"}
        height={"100%"}
        fit="contain"
        styles={{
          image: {
            objectPosition: "top left",
          },
          imageWrapper: { height: "100%" },
          figure: { height: "100%" },
          root: {
            height: "100%",
            width: "100%",
          },
        }}
        draggable={false}
        src={`${API_URL}/image/${dataset}/${file_name}`}
        {...restProps}
      />
    </div>
  );
}
