import './App.css'
import Login from './components/LoginPage'
import SignUp from './components/SignUpPage'
import StartChat from './components/StartChatPage'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

// App.jsx
function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<StartChat />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
            </Routes>
        </BrowserRouter>
    );
}


export default App
