import React, { useState } from "react";
import axios from "axios";
import { Box, Button, TextField, Typography, Alert } from "@mui/material";

const API_BASE_URL = "http://localhost:8000";

const Register = () => {
  const [form, setForm] = useState({ customer_id: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post(`${API_BASE_URL}/register`, form);
      setMessage(res.data.message);
      setError("");
    } catch (err) {
      setMessage("");
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 5 }}>
      <Typography variant="h5" gutterBottom>Register</Typography>

      <TextField
        fullWidth
        name="customer_id"
        label="Customer ID (CUST0000)"
        value={form.customer_id}
        onChange={handleChange}
        margin="normal"
      />

      <TextField
        fullWidth
        name="email"
        label="Email"
        value={form.email}
        onChange={handleChange}
        margin="normal"
      />

      <TextField
        fullWidth
        type="password"
        name="password"
        label="Password"
        value={form.password}
        onChange={handleChange}
        margin="normal"
      />

      <Button variant="contained" fullWidth onClick={handleSubmit} sx={{ mt: 2 }}>
        Register
      </Button>

      {message && <Alert severity="success" sx={{ mt: 2 }}>{message}</Alert>}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
    </Box>
  );
};

export default Register;
