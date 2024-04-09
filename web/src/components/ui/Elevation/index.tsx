// This file is part of the irunawiki client code

import React, { HTMLAttributes } from "react";
import styles from "./style.module.css";
import classes from "@/utils/classes";

const Elevation = React.forwardRef<HTMLDivElement, HTMLAttributes<HTMLElement>>(
  ({ className, children, ...props }, ref) => {
    const internalRef = React.useRef<HTMLDivElement>(null);
    const resolvedRef = ref || internalRef;
    const classNames = classes(styles['elevation'], className)
    return (
      <div
        ref={resolvedRef}
        className={classNames}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Elevation.displayName = "Elevation";
export default Elevation;