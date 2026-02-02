import api from "./api";

const USER_ROUTE = "/api/v1/users";

export interface UserResponse {
    id: number,
    full_name: string;
    email: string;
}

export const createUser = (
    full_name: string,
    email: string,
    password: string
) => {
    return api.post<UserResponse>(
        USER_ROUTE,
        {
            full_name,
            email,
            password,
        }
    );
};

export const getUsers = () => {
    return api.get<UserResponse[]>(USER_ROUTE);
};
