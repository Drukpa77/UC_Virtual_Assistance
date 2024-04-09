// This file is part of the irunawiki client code

import React, { HTMLAttributes } from 'react';
import styles from './style.module.css'
import classes from '../../../utils/classes';

export default function Input({className, ...props}: HTMLAttributes<HTMLInputElement>) {
  const classNames = classes(styles.input, className);
  return (
    <input className={classNames} {...props}/>
  )
}