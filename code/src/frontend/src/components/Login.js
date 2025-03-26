import React, { useState } from "react";
import { Container, TextField, Button, Typography,Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/api";

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await loginUser(email, password);
            
            localStorage.setItem("access_token", response.access_token); 
            localStorage.setItem("cust_id", response["Customer ID"]);    
            
            navigate("/"); 
        } catch (error) {
            alert("Invalid credentials");
        }
    };
    return (
        <Box sx={{ maxWidth: 400, mx: "auto", mt: 5 }}>
        <Container maxWidth="xs">
            <Typography variant="h5">Login</Typography>
            <TextField fullWidth label="Email" onChange={(e) => setEmail(e.target.value)} margin="normal" />
            <TextField fullWidth type="password" label="Password" onChange={(e) => setPassword(e.target.value)} margin="normal" />
            <Button fullWidth variant="contained" color="primary" onClick={handleLogin}>
                Login
            </Button>
            <Typography>New User? <Button onClick={() => navigate("/register")}>Register Here</Button></Typography>
        </Container>
        </Box>
    );
};

export default Login;
