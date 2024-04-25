import { Provider } from 'react-redux'

import ChatApp from '@/layouts/ChatApp'
import ChatBubble from '@/components/core/ChatBubble'
import WebsocketProvider from '@/contexts/ws'
import store from './store'
import { useState } from 'react'
import ChatFabWindow from './layouts/ChatFabWindow'

function App() {
  const [openFab, setOpenFab] = useState<boolean>(false);

  return (
    <Provider store={store}>
      <WebsocketProvider host="ws://localhost:8000/ws/10">
        <ChatApp/>
        <ChatBubble onClick={() => setOpenFab(true)}/>

        {openFab ? <ChatFabWindow onClose={() => setOpenFab(false)}/> : null}
      </WebsocketProvider>
    </Provider>
  )
}

export default App
