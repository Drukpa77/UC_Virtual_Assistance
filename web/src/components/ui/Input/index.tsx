
import { InputHTMLAttributes } from 'react';
import styles from './style.module.css'
import classes from '../../../utils/classes';

export default function Input({className, ...props}: InputHTMLAttributes<HTMLInputElement> ) {
  const classNames = classes(styles.input, className);
  return (
    <input className={classNames} {...props}/>
  )
}