// this file belongs to irunawiki organisation

import { SVGProps } from "react";
import classes from "@/utils/classes";
import styles from "./style.module.css";

export default function SVGIcon({ className, children, ...props }: SVGProps<SVGSVGElement>) {
  const classNames = classes(styles['svg-icon'], className);
  return (
    <svg
      className={classNames}
      {...props}
    >
      {children}
    </svg>
  );
}