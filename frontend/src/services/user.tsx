import api from "./api";

const USER_ROUTE = "/api/v1/users";

export interface UserResponse {
    id: number;
    full_name: string;
    email: string;
}

export const createUser = async (
    full_name: string,
    email: string,
    password: string
) => {
    return await api.post<UserResponse>(
        USER_ROUTE,
        {
            full_name,
            email,
            password,
        }
    );
};

export const getUsers = async () => {
    return await api.get<UserResponse[]>(USER_ROUTE);
};
