import axios from "axios";

let authBridge = {
  getAccessToken: () => null,
  getRefreshToken: () => null,
  refreshSession: async () => null,
  clearSession: () => {},
};

export function configureAuthBridge(nextBridge) {
  authBridge = nextBridge;
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  timeout: 20000,
});

api.interceptors.request.use((config) => {
  const token = authBridge.getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error?.response?.status === 401 &&
      !originalRequest?._retry &&
      authBridge.getRefreshToken()
    ) {
      originalRequest._retry = true;

      try {
        const newAccess = await authBridge.refreshSession();
        if (newAccess) {
          originalRequest.headers.Authorization = `Bearer ${newAccess}`;
          return api(originalRequest);
        }
      } catch {
        authBridge.clearSession();
      }
    }

    return Promise.reject(error);
  },
);
