import api from "./api";

const CHAT_ROUTE = "/api/v1/chats/";

export interface ShowChat {
    id: number;
    title: string;
};

export interface ShowMessage {
    id: number;
    role: "user" | "assistant";
    content: string;
};

export const createChatWithMessage = async (message: string) => {
    return await api.post<ShowChat>(
        CHAT_ROUTE,
        {
            role: "user",
            content: `${message}`
        }
    );
};

export const getChatWithUser = async () => {
    return await api.get<ShowChat[]>(
        CHAT_ROUTE
    );
};

export const insertMessage = async (chat_id: number, message: string) => {
    return await api.post<ShowMessage>(
        CHAT_ROUTE + `${chat_id}/messages`,
        {
            role: "user",
            content: `${message}`
        }
    );
};

export const getMessageWithChat = async (chat_id: number) => {
    return await api.get<ShowMessage[]>(
        CHAT_ROUTE + `${chat_id}/messages`
    );
}
