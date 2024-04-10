import { Provider } from 'react-redux'

import ChatApp from '@/layouts/ChatApp'
import ChatBubble from '@/components/core/ChatBubble'
import WebsocketProvider from '@/contexts/ws'
import store from './store'

function App() {
  return (
    <Provider store={store}>
      <WebsocketProvider host="ws://localhost:8000/10">
        <ChatApp/>
        <ChatBubble/>
      </WebsocketProvider>
    </Provider>
  )
}

export default App
