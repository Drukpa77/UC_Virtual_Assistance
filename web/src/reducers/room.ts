import { createSlice } from '@reduxjs/toolkit';
import { PayloadPacket } from './types';

interface RoomMessage extends PayloadPacket {
  payload: {message: string};
}
interface RoomState {
  roomId: number;
  messages: string[];
}

export const roomSlice = createSlice({
  name: "roomSlice",
  initialState: {
      roomId: 0,
      messages: [],
  } as RoomState,
  reducers: {
    updateMessage: (state, action: RoomMessage) => {
      state.messages = [...state.messages, action.payload.message];
    }
  }
})

export default roomSlice.reducer