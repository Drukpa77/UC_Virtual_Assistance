import Input from '@/components/ui/Input';
import ChatMessage from '@/components/core/ChatMessage';
import ChatAppBar from '../ChatAppBar';
import ArrowUp from '@/components/icons/ArrowUp';
import Row from '@/components/ui/Row';
import ThumbsUpIcon from '@/components/icons/ThumbsUpIcon';
import ThumbsDownIcon from '@/components/icons/ThumbsDownIcon';
import styles from './style.module.css';

export default function ChatApp() {
  return (
    <div className={styles.container}>
      <div className={styles['chat-bar']}>
        <ChatAppBar/>
      </div>
      <div className={styles['chat-area']}>
        <ChatMessage message='Hello world'/>
        <ChatMessage message='Hi'/>
        <Row pl={3}>
          <ThumbsUpIcon className={styles['feedback-icon']}/>
          <ThumbsDownIcon className={`${styles['feedback-icon']} ${styles['feedback-icon-right']}`}/>
        </Row>
      </div>
      <div className={styles['chat-input']}>
        <form className={styles['chat-form']}>
          <Input className={styles.input} placeholder='type your message'/>
          <button type="submit" className={styles['submit-button']}>
            <ArrowUp/>
          </button>
          
        </form>
        <div>UC Bot can make mistakes, consider checking information</div>
      </div>
      
    </div>
  )
}