import { ChatMessageProps } from "./types";
import classes from "@/utils/classes";
import styles from './style.module.css';

export default function ChatMessage({message, className, ...props}: ChatMessageProps) {
  const classNames = classes(styles['message'], className);
  return (
    <div className={classNames} {...props}>
      {message}
    </div>
  )
}