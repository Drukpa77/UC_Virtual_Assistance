import { HTMLAttributes } from "react";
import { BoxProps } from "../Box/types";

type Justify =
  | "flex-start"
  | "center"
  | "flex-end"
  | "space-between"
  | "space-around"
  | "space-evenly";

type AlignItems = "flex-start" | "center" | "flex-end" | "stretch" | "baseline";
type Direction = "column" | "row";

export interface RowProps extends HTMLAttributes<HTMLElement>, BoxProps<HTMLElement> {
  justify?: Justify;
  alignItem?: AlignItems;
  direction?: Direction;
  wrap?: boolean;
}