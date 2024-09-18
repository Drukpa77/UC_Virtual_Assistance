import { roomSlice } from '@/reducers/room';
import { MESSAGE_BOT } from '@/reducers/types';
import React from 'react';
import { useDispatch } from 'react-redux';
import useWebSocket from 'react-use-websocket';

interface WebSocketContextType {
  sendMessage: (message: string) => void;
  setLoading: (loading: boolean) => void; 
}

const WebSocketContext = React.createContext<WebSocketContextType | null>(null);

export { WebSocketContext }

interface Props {
  children: React.ReactNode;
  host: string;
  setLoading: (loading: boolean) => void;  // New prop
}

export interface Packet {
  type: string;
  params: Record<string, any>
}

export default ({ children, host, setLoading }: Props) => {
  let ws;
  
  const dispatch = useDispatch();

  const { sendJsonMessage } = useWebSocket(host, {
      onOpen: () => {},
      onMessage: (event: MessageEvent) => {
        const data = JSON.parse(event.data);

        switch(data.type) {
          case "room:message":
            dispatch(roomSlice.actions.updateMessage({message: data.params.payload.message, user: MESSAGE_BOT}));
            setLoading(false);  // Set loading to false when a message is received
            break;
        }
    }
  })

  const sendMessage = (message: string) => {
    const obj: Packet =  {
      "type": "message:send",
      "params": {"value": message}
    }
    setLoading(true);  // Set loading to true when a message is sent
    sendJsonMessage(obj);
  }

  ws = {
    sendMessage,
    setLoading
  }

  return (
    <WebSocketContext.Provider value={ws}>
        {children}
    </WebSocketContext.Provider>
  )
}