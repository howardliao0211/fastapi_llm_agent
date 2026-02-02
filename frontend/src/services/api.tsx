import axios from "axios";

const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_SERVER_URL;

const api = axios.create({
    baseURL: BACKEND_BASE_URL,
});

export default api;
