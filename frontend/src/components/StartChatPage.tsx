import { useState, type JSX } from "react";
import ChatSidebar from "./ChatSidebar";

export default function StartChat(): JSX.Element {
    const [message, setMessage] = useState('');

    const handleSubmitChat = () => {
        alert(`submit message: ${message}`)
    };

    const chats = [
        "test1",
        "test1",
    ];

    return (
        <div className="fixed inset-0 bg-zinc-900">
            <div className="flex h-full w-full">
                <ChatSidebar chats={chats} />

                <main className="flex-1 flex flex-col items-center justify-center text-2xl">
                    <h2 className="mb-4">What's on your mind today?</h2>

                    <textarea
                        className="
                        text-base
                        w-full max-w-2xl
                        rounded-2xl px-6 py-3
                        resize-none border border-white
                        bg-transparent text-white
                        field-sizing-content
                        max-h-80
                        "
                        placeholder="Ask anything"
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key == "Enter") {
                                e.preventDefault();
                                handleSubmitChat();
                            }
                        }}
                    />
                </main>
            </div>
        </div>
    );
}
