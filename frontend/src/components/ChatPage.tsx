import { JSX, useEffect, useState } from "react"
import ChatSidebar from "./ChatSidebar";
import { getMessageWithChat, insertMessage } from "../services/chat";
import type { ShowMessage } from "../services/chat";
import { useParams } from "react-router-dom";
import { useRef } from "react";

export default function Chat(): JSX.Element {
    const { chatId } = useParams<{ chatId: string }>();

    const chat_id = Number(chatId);

    if (Number.isNaN(chat_id)) {
        return <div>Invalid chat</div>;
    }

    const loading_id = -1;

    const [isResponding, setIsResponding] = useState(false);
    const [message, setMessage] = useState<string>('');
    const [chatMessages, setChatMessages] = useState<ShowMessage[]>([]);
    const createLoadingMessage = (): ShowMessage => ({
        id: loading_id,
        role: "assistant",
        content: "Thinking…",
    });

    const bottomRef = useRef<HTMLDivElement | null>(null);

    const handleSubmit = async () => {
        const curQuestion: ShowMessage = {
            id: Date.now(),
            role: "user",
            content: message,
        };

        setChatMessages((prev) => [
            ...prev,
            curQuestion,
            createLoadingMessage(),
        ]);
        setIsResponding(true);

        try {
            const res = await insertMessage(chat_id, message);
            setChatMessages((prev) =>
                prev.filter((m) => (m.id != loading_id))
                    .concat(res.data)
            );
            setMessage("");
        } catch (err: any) {
            const message =
                Array.isArray(err.response?.data?.detail)
                    ? err.response.data.detail.map((e: any) => e.msg).join("\n")
                    : err.response?.data?.detail ||
                    err.response?.data?.message ||
                    "Error at asking question";
            alert(message);
        } finally {
            setIsResponding(false);
        }
    };

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatMessages]);

    useEffect(() => {
        if (!chat_id) return;

        const loadMessages = async () => {
            try {
                const res = await getMessageWithChat(chat_id);
                setChatMessages(res.data); // replace state
            } catch (err: any) {
                const message =
                    Array.isArray(err.response?.data?.detail)
                        ? err.response.data.detail.map((e: any) => e.msg).join("\n")
                        : err.response?.data?.detail ||
                        err.response?.data?.message ||
                        "Error at initializing Chat";
                alert(message);
            }
        };

        loadMessages();
    }, [chat_id]);


    return (
        <div className="fixed inset-0 bg-zinc-900">
            <div className="flex h-full w-full">
                <ChatSidebar chats={["test"]} />

                <main className="flex-1 flex flex-col items-center justify-center text-2xl overflow-hidden">

                    {/*Scroll Area*/}
                    <div className="flex-1 w-full overflow-y-auto px-6 py-6 space-y-4">
                        {
                            chatMessages.map((msg) => (
                                <div
                                    key={msg.id}
                                    className={`w-fit max-w-xl px-4 py-2 rounded-2xl text-base ${msg.role === "user"
                                        ? "ml-auto bg-blue-600 text-white"
                                        : msg.id === -1 ?
                                            "mr-auto bg-zinc-700 text-gray-400 italic animate-pulse" :
                                            "mr-auto bg-zinc-700 text-white"
                                        }`}
                                >
                                    {msg.content}
                                </div>
                            ))
                        }
                        <div ref={bottomRef} />
                    </div>

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
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey && !isResponding) {
                                e.preventDefault();
                                handleSubmit();
                            }
                        }}
                    />
                </main>
            </div >
        </div >
    );
};