import axios from 'axios';

const { VITE_BASE_URL } = import.meta.env;

function serverAxios() {
    const instance = axios.create({
        baseURL: VITE_BASE_URL,
    });

    return instance;
}

export { serverAxios };