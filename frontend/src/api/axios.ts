import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem("access");

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  }
);

api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest =
      error.config;

    if (
      error.response?.status ===
        401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry =
        true;

      try {
        const refresh =
          localStorage.getItem(
            "refresh"
          );

        const response =
          await axios.post(
            `${import.meta.env.VITE_API_URL}/auth/refresh/`,
            {
              refresh,
            }
          );

        const newAccess =
          response.data.access;

        localStorage.setItem(
          "access",
          newAccess
        );

        originalRequest.headers.Authorization =
          `Bearer ${newAccess}`;

        return api(
          originalRequest
        );

      } catch {
        localStorage.clear();

        window.location.href =
          "/";
      }
    }

    return Promise.reject(error);
  }
);

export default api;