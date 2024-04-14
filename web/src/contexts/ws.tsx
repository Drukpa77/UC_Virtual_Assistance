import { roomSlice } from '@/reducers/room';
import { MESSAGE_BOT } from '@/reducers/types';
import React from 'react';
import { useDispatch } from 'react-redux';
import useWebSocket from 'react-use-websocket';

interface WebSocketContextType {
  sendMessage: (message: string) => void;
}

const WebSocketContext = React.createContext<WebSocketContextType | null>(null);

export { WebSocketContext }

interface Props {
  children: React.ReactNode;
  host: string;
}

export interface Packet {
  type: string;
  params: Record<string, any>
}

export default ({ children, host }: Props) => {
  let ws;
  
  const dispatch = useDispatch();

  const { sendJsonMessage } = useWebSocket(host, {
      onOpen: () => {},
      onMessage: (event: MessageEvent) => {
        const data = JSON.parse(event.data);

        switch(data.type) {
          case "room:message":
            dispatch(roomSlice.actions.updateMessage({message: data.params.payload.message, user: MESSAGE_BOT}));
            break;
        }
    }
  })

  const sendMessage = (message: string) => {
    const obj: Packet =  {
      "type": "message:send",
      "params": {"value": message}
    }
    sendJsonMessage(obj);
  }

  ws = {
    sendMessage
  }

  return (
    <WebSocketContext.Provider value={ws}>
        {children}
    </WebSocketContext.Provider>
  )
}