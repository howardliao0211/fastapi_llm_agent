import './App.css'
import Chat from './components/ChatPage'
import Login from './components/LoginPage'
import SignUp from './components/SignUpPage'
import StartChat from './components/StartChatPage'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

// App.jsx
function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/chats" element={<StartChat />} />
                <Route path="/chats/:chatId" element={<Chat />} />
            </Routes>
        </BrowserRouter>
    );
}


export default App
