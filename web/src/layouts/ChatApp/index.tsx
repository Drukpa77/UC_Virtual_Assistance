import Input from '@/components/ui/Input';
import ChatMessage from '@/components/core/ChatMessage';
import ChatAppBar from '../ChatAppBar';
import ArrowUp from '@/components/icons/ArrowUp';
import Row from '@/components/ui/Row';
import ThumbsUpIcon from '@/components/icons/ThumbsUpIcon';
import ThumbsDownIcon from '@/components/icons/ThumbsDownIcon';
import Box from '@/components/ui/Box';
import AccountIcon from '@/components/icons/AccountIcon';
import RobotIcon from '@/components/icons/RobotIcon';
import { ChangeEvent, FormEvent, useContext, useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { WebSocketContext } from '@/contexts/ws';
import styles from './style.module.css';
import { RoomMessage, roomSlice } from '@/reducers/room';
import { MESSAGE_BOT, MESSAGE_HUMAN } from '@/reducers/types';
import Markdown from 'react-markdown'
import { formatMDLinks } from '@/utils/markdown/strings';

export default function ChatApp({loading}: {loading: boolean}) {
  const messagesEndRef = useRef<null | HTMLDivElement>(null)
  const ws = useContext(WebSocketContext);
  //const [loading, setLoading] = useState<boolean>(false);
  const roomMessages: RoomMessage[] = useSelector((state) => state.room.messages);
  const [message, setMessage] = useState<string>("");
  const dispatch = useDispatch();


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }
  useEffect(() => {
    scrollToBottom()
  }, [roomMessages]);


  const handleSendMessage = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    ws?.sendMessage(message);
    dispatch(roomSlice.actions.updateMessage({message: message, user: MESSAGE_HUMAN}));
    setMessage(""); // clear input
  }

  return (
    <div className={styles.container}>
      <div className={styles['chat-bar']}>
        <ChatAppBar/>
      </div>
      <div className={styles['chat-area']}>
        <Row  mb={2}>
          <RobotIcon className={styles['user-icon']}/>
          <Box className={styles['message-container']}>
            <Box pl={3}><b>InfoOracle</b></Box>
            <ChatMessage message={<Markdown>{`My name is **InfoOracle**, how can I help you today?`}</Markdown>}/>
          </Box>
        </Row>
        {roomMessages.map((value, index) =>
          <Row key={index} mb={2}>
            {value.user === MESSAGE_BOT ? 
              <>
                <RobotIcon className={styles['user-icon']}/>
                <Box className={styles['message-container']}>
                  <Box pl={3}><b>InfoOracle</b></Box>
                  <ChatMessage message={<Markdown>{`${formatMDLinks(value.message)}`}</Markdown>}/>
                  <Row pl={3}>
                    <ThumbsUpIcon className={styles['feedback-icon']}/>
                    <ThumbsDownIcon className={`${styles['feedback-icon']} ${styles['feedback-icon-right']}`}/>
                  </Row>
                </Box>
              </>
            : 
            <>
              <AccountIcon className={styles['user-icon']}/>
              <Box className={styles['message-container']}>
                <Box pl={3}><b>User</b></Box>
                <ChatMessage message={value.message}/>
              </Box>
            </>}
          </Row>
        )}
        {loading &&
        <Row mb={2}> 
          <RobotIcon className={styles['user-icon']}/>
          <Box className={styles['message-container']}>
            <Box pl={3}><b>InfoOracle</b></Box>
            <ChatMessage message={"Thinking..."}/>
          </Box>
        </Row>}
       <div ref={messagesEndRef} className={styles['chat-break']} />
      </div>
     
      <div className={styles['chat-input']}>
        <form className={styles['chat-form']} onSubmit={handleSendMessage}>
          <Box className={styles['input-container']}>
            <Input className={styles.input} placeholder='type your message' value={message} onChange={(e: ChangeEvent<HTMLInputElement>) => setMessage(e.target.value)}/>
            <button type="submit" className={styles['submit-button']}>
              <ArrowUp/>
            </button>
          </Box>


        </form>
        <div>InfoOracle can make mistakes, consider checking information</div>
      </div>
      
    </div>
  )
}