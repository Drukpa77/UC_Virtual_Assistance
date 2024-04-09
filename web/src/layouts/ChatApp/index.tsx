import Input from '@/components/ui/Input';
import styles from './style.module.css';
import ChatMessage from '@/components/core/ChatMessage';
import ChatAppBar from '../ChatAppBar';


export default function ChatApp() {
  return (
    <div className={styles.container}>
      <div className={styles['chat-bar']}>
        <ChatAppBar/>
      </div>
      <div className={styles['chat-area']}>
        <ChatMessage message='Hello world'/>
        <ChatMessage message='Hi'/>
      </div>
      <div className={styles['chat-input']}>
        <form className={styles['chat-form']}>
          <Input className={styles.input} placeholder='type your message'/>
        </form>
        <div>UC Bot can make mistakes, consider checking information</div>
      </div>
      
    </div>
  )
}