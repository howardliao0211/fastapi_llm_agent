import './App.css'
import Login from './components/LoginPage'
import SignUp from './components/SignUpPage'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

// App.jsx
function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
            </Routes>
        </BrowserRouter>
    );
}


export default App
