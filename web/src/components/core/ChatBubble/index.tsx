import Fab from "@/components/ui/Fab";
import HideOnScroll from "@/components/utils/HideOnScroll";
import styles from './style.module.css';

export default function ChatBubble() {
  return (
    <>
      <HideOnScroll direction='right'>
        <Fab className={styles['bubble']}>
          <div>h</div>
        </Fab>
      </HideOnScroll>
    </>
  )
}