import { useState } from "react";

export default function ChatSidebar({ chats }: { chats: string[] }) {
    const [activeIndex, setActiveIndex] = useState<number>(1);

    return (
        <aside className="w-72 h-full bg-black text-white border-r border-zinc-800">
            {/* Header */}
            <div className="px-4 py-3 text-sm text-zinc-400">
                Your chats
            </div>

            {/* Chat list */}
            <div className="px-2 space-y-2">
                {chats.map((title, index) => (
                    <button
                        key={index}
                        onClick={() => setActiveIndex(index)}
                        className={`
                            w-full text-left px-3 py-2 rounded-md text-sm truncate
                            transition-colors
                            ${activeIndex === index
                                ? "bg-zinc-800 text-white"
                                : "text-zinc-400 hover:bg-zinc-800 hover:text-white"
                            }
                            `}
                    >
                        {title}
                    </button>
                ))}
            </div>
        </aside>
    );
}
