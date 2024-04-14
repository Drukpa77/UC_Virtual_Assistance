import { createSlice } from '@reduxjs/toolkit';
import { PayloadPacket } from './types';

interface RoomMessagePacket extends PayloadPacket {
  payload: {message: string, user: number};
}

export interface RoomMessage {
  user: number;
  message: string;
}
interface RoomState {
  roomId: number;
  messages: RoomMessage[];
}

export const roomSlice = createSlice({
  name: "roomSlice",
  initialState: {
    roomId: 0,
    messages: [],
  } as RoomState,
  reducers: {
    updateMessage: (state, action: RoomMessagePacket) => {
      const { message, user } = action.payload;
      // Push the new message to the messages array
      const newMessages = [...state.messages, { message, user }];
      //state.messages = [...state.messages, {messsage: action.payload.message, user: action.payload.user}];
      return {
        ...state,
        messages: newMessages,
      };
    }
  }
})

export default roomSlice.reducer