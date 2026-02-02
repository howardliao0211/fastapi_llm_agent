import { useState } from 'react';
import type { SubmitEvent } from 'react';
import type { JSX } from 'react';
import { login } from '../services/token';


export default function Login(): JSX.Element {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    const handleSubmit = async (e: SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();

        setLoading(true);

        try {
            const res = await login(username, password);

            console.log('login success:', res.data);
            localStorage.setItem('token', res.data.access_token);
            alert('Login successful');
        } catch (err: any) {
            const message =
                err.response?.data?.detail ||
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
                        {loading ? 'Logging in...' : 'Login'}
                    </button>

                    <p className=" rounded text-sm justify-items-center bg-neutral-900 px-2">
                        Don’t have an account?{" "}
                        <br />
                        <a href="/signup" className="text-amber-500 hover:underline">
                            Sign up
                        </a>
                    </p>

                </div>
            </div>

        </form>
    );
}
