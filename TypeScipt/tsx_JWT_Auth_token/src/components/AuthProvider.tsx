import { useState, useEffect, useLayoutEffect, createContext, type ReactNode } from 'react';
import axios, { type InternalAxiosRequestConfig, type AxiosResponse, AxiosError } from 'axios';

// 1. Extend InternalAxiosRequestConfig for our custom property
interface CustomAxiosRequestConfig extends InternalAxiosRequestConfig {
    _retry?: boolean;
}

// 2. Define the shape of FastAPI error responses
interface ApiErrorResponse {
    message?: string;
    detail?: string;
}

// 3. Create the custom Axios instance
export const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true,
});

export const AuthContext = createContext<any>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null | undefined>(undefined);

    useEffect(() => {
        const fetchMe = async () => {
            try {
                const res = await api.get('/api/me');
                setToken(res.data.access_token);
            } catch {
                setToken(null);
            }
        };
        fetchMe();
    }, []);

    // Request Interceptor
    useLayoutEffect(() => {
        const authInterceptor = api.interceptors.request.use(
            // Cast the config inside the interceptor signature
            (config) => {
                const customConfig = config as CustomAxiosRequestConfig;
                if (token && !customConfig._retry) {
                    customConfig.headers.Authorization = `Bearer ${token}`;
                }
                return customConfig;
            }
        );

        return () => {
            api.interceptors.request.eject(authInterceptor);
        };
    }, [token]);

    // Response Interceptor
    useLayoutEffect(() => {
        const refreshInterceptor = api.interceptors.response.use(
            (response: AxiosResponse) => response,
            async (error: AxiosError<ApiErrorResponse>) => {
                const originalRequest = error.config as CustomAxiosRequestConfig | undefined;

                // Ensure originalRequest exists before checking properties or retrying
                if (
                    error.response?.status === 401 &&
                    originalRequest &&
                    !originalRequest._retry
                ) {
                    originalRequest._retry = true; // Mark as retried immediately

                    try {
                        const res = await api.get('/api/refresh_token');
                        const newAccessToken = res.data.access_token;

                        setToken(newAccessToken);

                        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

                        // Pass the verified originalRequest object back to Axios
                        return api(originalRequest);
                    } catch (refreshError) {
                        setToken(null);
                    }
                }

                return Promise.reject(error);
            }
        );

        return () => {
            api.interceptors.response.eject(refreshInterceptor);
        };
    }, []);

    return (
        <AuthContext.Provider value={{ token, setToken }}>
            {token === undefined ? <div>Loading App...</div> : children}
        </AuthContext.Provider>
    );
}