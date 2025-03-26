import axios from "axios";

const API_BASE_URL = "http://localhost:8000";



export const loginUser = async (email, password) => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/login`,
            { email, password },
            { headers: { "Content-Type": "application/json" } }
        );

        // ✅ Update key names
        if (response.data.access_token && response.data["Customer ID"]) {
            return response.data;
        } else {
            throw new Error("Invalid login response");
        }
    } catch (error) {
        console.error("Login failed:", error.response?.data || error.message);
        throw new Error(error.response?.data?.detail || "Invalid credentials");
    }
};

export function getUserIdFromToken(token) {
    if (!token) return null;
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.user_id || payload.sub || null;
  }  


export const logoutUser = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("cust_id");
};

export const getRecommendation = async () => {
    const userId = localStorage.getItem("cust_id");
    const response = await axios.get(`${API_BASE_URL}/api/recommend/${userId}`, getAuthHeaders());
    return response.data;
};

export const getSentiment = async () => {
    const userId = localStorage.getItem("cust_id");
    const response = await axios.get(`${API_BASE_URL}/api/sentiment/${userId}`, getAuthHeaders());
    return response.data;
};

export const getRisk = async () => {
    const userId = localStorage.getItem("cust_id");
    const response = await axios.get(`${API_BASE_URL}/api/risk/${userId}`, getAuthHeaders());
    return response.data;
};

export const getPersonalization = async () => {
    const userId = localStorage.getItem("cust_id");
    const response = await axios.get(`${API_BASE_URL}/api/personalize/${userId}`, getAuthHeaders());
    return response.data;
};

export function getAuthHeaders() {
    const token = localStorage.getItem("access_token");
    return {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
  }
  