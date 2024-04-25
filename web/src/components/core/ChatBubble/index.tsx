import Fab from "@/components/ui/Fab";
import HideOnScroll from "@/components/utils/HideOnScroll";
import RobotIcon from "@/components/icons/RobotIcon";
import styles from './style.module.css';

export default function ChatBubble() {
  return (
    <>
      <HideOnScroll direction='right'>
        <Fab className={styles['bubble']}>
          <RobotIcon/>
        </Fab>
      </HideOnScroll>
    </>
  )
}