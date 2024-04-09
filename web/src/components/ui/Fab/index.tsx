// This file is part of the irunawiki client code

import React, { HTMLAttributes } from "react";
import styles from "./style.module.css";
import classes from "@/utils/classes";


export default function Fab({ className, children, ...props }: HTMLAttributes<HTMLButtonElement>) {
  const classNames = classes(styles['fab'], className)
  return (
    <button
      className={classNames}
      {...props}
    >
      <span className={`${styles["fab-label"]}`}>{children}</span>
    </button>
  );
}