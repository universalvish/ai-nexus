import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://ai-nexus-22sc.onrender.com';

class ApiClient {
  private client;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    this.client.interceptors.request.use(
      (config) => {
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          if (typeof window !== 'undefined') {
            localStorage.removeItem('token');
            window.location.href = '/auth/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data, config);
    return response.data;
  }

  async patch<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.patch(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url, config);
    return response.data;
  }
}

export const api = new ApiClient();

export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, unknown>;
}

export function handleApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    return {
      message: axiosError.response?.data?.message || axiosError.message,
      code: axiosError.code,
      details: axiosError.response?.data?.details,
    };
  }
  return { message: 'An unexpected error occurred' };
}

// API Endpoints
export const authApi = {
  login: (email: string, password: string) => api.post('/auth/login', { email, password }),
  register: (data: { email: string; password: string; name: string }) => api.post('/auth/register', data),
  logout: () => api.post('/auth/logout'),
  refresh: () => api.post('/auth/refresh'),
  me: () => api.get('/auth/me'),
};

export const chatApi = {
  send: (message: string, context?: Record<string, unknown>) => api.post('/chat', { message, context }),
  history: (limit = 50) => api.get(`/chat/history?limit=${limit}`),
  clear: () => api.delete('/chat/history'),
};

export const agentsApi = {
  list: () => api.get('/agents'),
  create: (data: unknown) => api.post('/agents', data),
  get: (id: string) => api.get(`/agents/${id}`),
  update: (id: string, data: unknown) => api.patch(`/agents/${id}`, data),
  delete: (id: string) => api.delete(`/agents/${id}`),
  execute: (id: string, action: string, params?: Record<string, unknown>) => 
    api.post(`/agents/${id}/execute`, { action, params }),
};

export const analyticsApi = {
  dashboard: () => api.get('/analytics/dashboard'),
  usage: (period: string) => api.get(`/analytics/usage?period=${period}`),
  revenue: (period: string) => api.get(`/analytics/revenue?period=${period}`),
  exports: (type: string, format: string) => api.get(`/analytics/exports?type=${type}&format=${format}`),
};

export const billingApi = {
  plans: () => api.get('/billing/plans'),
  subscription: () => api.get('/billing/subscription'),
  checkout: (planId: string) => api.post('/billing/checkout', { planId }),
  cancel: () => api.post('/billing/cancel'),
  invoices: () => api.get('/billing/invoices'),
};

export const automationApi = {
  list: () => api.get('/automation'),
  create: (data: unknown) => api.post('/automation', data),
  get: (id: string) => api.get(`/automation/${id}`),
  update: (id: string, data: unknown) => api.patch(`/automation/${id}`, data),
  delete: (id: string) => api.delete(`/automation/${id}`),
  trigger: (id: string) => api.post(`/automation/${id}/trigger`),
  runs: (id: string) => api.get(`/automation/${id}/runs`),
};