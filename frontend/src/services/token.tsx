import api from "./api";

const TOKEN_ROUTE = "/api/v1/token";

export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export const login = async (username: string, password: string) => {
    return await api.post<TokenResponse>(
        TOKEN_ROUTE,
        new URLSearchParams({
            username,
            password,
        }),
        {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        }
    );
};