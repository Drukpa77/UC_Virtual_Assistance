import { PureBoxProps } from "../PureBox/types";


export type TextAlign = "center" | "start" | "end" | "unset";
export type FontWeight = 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800;
export interface BoxProps<T> extends PureBoxProps<T> {
  m?: number; // margin
  mt?: number; // margin-top
  mr?: number; // margin-right
  mb?: number; // margin bottom
  ml?: number; // margin left
  p?: number; // padding
  pt?: number; // padding-top
  pr?: number; // padding-right
  pb?: number; // padding bottom
  pl?: number; // padding left
  textAlign?: TextAlign;
  fontWeight?: FontWeight;
}