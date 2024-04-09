// This file is part of the irunawiki client code

import React from "react";

type Direction = "right" | "up" | "down" | "left";
interface IProps {
  children?: React.ReactNode;
  appear: boolean; // default state whether this component is rendered or not
  direction: Direction; // direction of the animation
  flow: boolean; // trigger animation effect
}

const getTransformValue = (direction: Direction) => {
  switch (direction) {
    case "down":
      return "translateY(-150%)";
    case "up":
      return "translateY(150%)";
    case "left":
      return "translateX(-150%)";
    case "right":
      return "translateX(150%)";
    default:
      return "none";
  }
};

export default function Slide({ children, appear, direction, flow }: IProps) {
  const [style, setStyle] = React.useState<React.CSSProperties>({
    visibility: appear ? "visible" : "hidden",
    transition: "0.3s",
    transform: appear ? "none" : getTransformValue(direction),
  });

  React.useEffect(() => {
    if (appear) {
      if (flow) {
        setStyle((prevStyle) => ({
          ...prevStyle,
          visibility: "hidden",
          transform: getTransformValue(direction),
        }));
      } else {
        setStyle((prevStyle) => ({
          ...prevStyle,
          visibility: "visible",
          transform: "none",
        }));
      }
    } else {
      if (flow) {
        setStyle((prevStyle) => ({
          ...prevStyle,
          visibility: "visible",
          transform: "none",
        }));
      } else {
        setStyle((prevStyle) => ({
          ...prevStyle,
          visibility: "hidden",
          transform: getTransformValue(direction),
        }));
      }
    }
  }, [flow, appear, direction]);

  return (
    <div style={{ visibility: style.visibility }}>
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {
            style: {
              ...child.props.style,
              transition: style.transition,
              transform: style.transform,
            },
          });
        }
        return child;
      })}
    </div>
  );
}