import { useState } from 'react';
import type { SubmitEvent } from 'react';
import type { JSX } from 'react';
import { createUser } from '../services/user';
import { useNavigate } from 'react-router-dom';

interface TokenResponse {
    access_token: string;
    token_type: string;
}


export default function SignUp(): JSX.Element {
    const navigate = useNavigate();
    const [fullname, setFullname] = useState<string>('');
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    const handleSubmit = async (e: SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();

        setLoading(true);

        try {
            const res = await createUser(fullname, username, password);
            alert(`Successfully sign up for ${res.data.email}`);
            navigate("/login");
        } catch (err: any) {
            const message =
                Array.isArray(err.response?.data?.detail)
                    ? err.response.data.detail.map((e: any) => e.msg).join("\n")
                    : err.response?.data?.detail ||
                    err.response?.data?.message ||
                    "Invalid username or password";
            alert(message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form
            className='px-40 py-80 font-mono flex flex-col bg-linear-to-r from-slate-900 to-blue-200 text-gray-500'
            onSubmit={handleSubmit}
        >
            <div className='text-base flex flex-col mt-8 gap-2'>
                <h2 className='mt-4 text-4xl text-white align-top'>Welcome</h2>
                <input
                    className='mt-6 rounded bg-gray-600 text-blue-300 px-10 py-2 border'
                    type="text"
                    name="fullname"
                    placeholder="Full Name"
                    value={fullname}
                    onChange={(e) => setFullname(e.target.value)}
                    required
                />

                <input
                    className='rounded bg-gray-600 text-blue-300 px-10 py-2 border'
                    type="text"
                    name="username"
                    placeholder="Email"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />

                <input
                    className='rounded bg-gray-600 text-blue-300 px-10 py-2 border'
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <div className='flex gap-2 justify-center'>
                    <button type="submit" disabled={loading}>
                        {loading ? 'Signing Up...' : 'Sign Up'}
                    </button>

                </div>
            </div>

        </form>
    );
}
