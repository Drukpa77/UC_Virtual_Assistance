import Input from '@/components/ui/Input';
import ChatMessage from '@/components/core/ChatMessage';
import ChatAppBar from '../ChatAppBar';
import ArrowUp from '@/components/icons/ArrowUp';
import Row from '@/components/ui/Row';
import ThumbsUpIcon from '@/components/icons/ThumbsUpIcon';
import ThumbsDownIcon from '@/components/icons/ThumbsDownIcon';
import Box from '@/components/ui/Box';
import styles from './style.module.css';
import AccountIcon from '@/components/icons/AccountIcon';
import RobotIcon from '@/components/icons/RobotIcon';

export default function ChatApp() {
  return (
    <div className={styles.container}>
      <div className={styles['chat-bar']}>
        <ChatAppBar/>
      </div>
      <div className={styles['chat-area']}>
          <Row>
            <AccountIcon className={styles['user-icon']}/>
            <Box>
              <Box pl={3}><b>User</b></Box>
              <ChatMessage message='Hello world'/>
            </Box>
          </Row>
          <Row>
            <RobotIcon className={styles['user-icon']}/>
            <Box>
              <Box pl={3}><b>Bot</b></Box>
              <ChatMessage message='Hi'/>
              <Row pl={3}>
                <ThumbsUpIcon className={styles['feedback-icon']}/>
                <ThumbsDownIcon className={`${styles['feedback-icon']} ${styles['feedback-icon-right']}`}/>
              </Row>
            </Box>
          </Row>
      </div>
      <div className={styles['chat-input']}>
        <form className={styles['chat-form']}>
          <Box className={styles['input-container']}>
            <Input className={styles.input} placeholder='type your message'/>
            <button type="submit" className={styles['submit-button']}>
              <ArrowUp/>
            </button>
          </Box>
          
          
        </form>
        <div>UC Bot can make mistakes, consider checking information</div>
      </div>
      
    </div>
  )
}