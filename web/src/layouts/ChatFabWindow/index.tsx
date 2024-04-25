import Markdown from 'react-markdown';
import Row from '@/components/ui/Row';
import RobotIcon from '@/components/icons/RobotIcon';
import Box from '@/components/ui/Box';
import ChatMessage from '@/components/core/ChatMessage';
import { ChangeEvent, FormEvent, useContext, useEffect, useRef, useState } from 'react';
import classes from '@/utils/classes';
import CloseIcon from '@/components/icons/CloseIcon';
import Input from '@/components/ui/Input';
import ArrowUp from '@/components/icons/ArrowUp';
import { WebSocketContext } from '@/contexts/ws';
import { useDispatch, useSelector } from 'react-redux';
import { RoomMessage, roomSlice } from '@/reducers/room';
import { MESSAGE_BOT, MESSAGE_HUMAN } from '@/reducers/types';
import { formatMDLinks } from '@/utils/markdown/strings';
import ThumbsUpIcon from '@/components/icons/ThumbsUpIcon';
import ThumbsDownIcon from '@/components/icons/ThumbsDownIcon';
import AccountIcon from '@/components/icons/AccountIcon';
import { FabWindowProps } from './types';
import styles from './style.module.css';

export default function ChatFabWindow({onClose, ...props}: FabWindowProps) {
  const {className} = {...props}
  const classNames = classes(styles['window'], className);

  const messagesEndRef = useRef<null | HTMLDivElement>(null)
  const ws = useContext(WebSocketContext);
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
    <div className={classNames}>
      <Row justify='flex-end' className={styles['toolbox']}>
        <CloseIcon onClick={onClose}/>
      </Row>
      <Box className={styles['container']}>
        <Row mb={2}>
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
      <div ref={messagesEndRef} className={styles['chat-break']} />
      </Box>

      <div className={styles['chat-input']}>
        <form className={styles['chat-form']} onSubmit={handleSendMessage}>
          <Box className={styles['input-container']}>
            <Input className={styles.input} placeholder='type your message' value={message} onChange={(e: ChangeEvent<HTMLInputElement>) => setMessage(e.target.value)} />
            <button type="submit" className={styles['submit-button']}>
              <ArrowUp/>
            </button>
          </Box>


        </form>
        <div className={styles['footer']}>InfoOracle can make mistakes, consider checking information</div>
      </div>
    </div>
  )
}