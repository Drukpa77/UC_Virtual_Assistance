import Fab from "@/components/ui/Fab";
import HideOnScroll from "@/components/utils/HideOnScroll";
import RobotIcon from "@/components/icons/RobotIcon";
import styles from './style.module.css';
import { HTMLAttributes } from "react";

export default function ChatBubble({...props}: HTMLAttributes<HTMLButtonElement>) {
  return (
    <>
      <HideOnScroll direction='right'>
        <Fab {...props} className={styles['bubble']}>
          <RobotIcon/>
        </Fab>
      </HideOnScroll>
    </>
  )
}