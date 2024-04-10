import { configureStore } from '@reduxjs/toolkit'
import roomCounter from '@/reducers/room'

export default configureStore({
  reducer: {
    room: roomCounter
  }
})