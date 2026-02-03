import { useState, type JSX } from "react";
import ChatSidebar from "./ChatSidebar";
import { createChatWithMessage } from "../services/chat";
import { useNavigate } from "react-router-dom";

export default function StartChat(): JSX.Element {
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmitChat = async () => {
        try {
            const res = await createChatWithMessage(message);
            const chatId = res.data.id;
            navigate(`/chats/${chatId}`);

        } catch (err) {
            console.error(`Error at starting chat: ${err}`);
        }
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
