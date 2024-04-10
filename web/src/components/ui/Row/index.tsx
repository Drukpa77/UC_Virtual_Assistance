import React from "react";
import { RowProps } from "./types";
import classes from "@/utils/classes";
import Box from "../Box";
import styles from "./style.module.css";


export default function Row({
  justify = "flex-start", 
  alignItem = "stretch", 
  direction = "row",
  wrap,
  className, 
  children, 
  ...props
}: RowProps) {
  const classNames = classes(
    styles["row"], 
    styles[`row-justify-${justify}`], 
    styles[`row-align-item-${alignItem}`], 
    direction === "column" ? styles['row-column'] : '',
    wrap ? styles['row-wrap'] : '',
    className || ''
  );
  return (
    <Box
      component="div"
      className={classNames}
      {...props}
    >
      {children}
    </Box>
  );
}