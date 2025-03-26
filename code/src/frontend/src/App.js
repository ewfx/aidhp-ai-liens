import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Button, Typography, Box } from "@mui/material";
import icon from "./icon.jpg";
import Sentiment from "./components/Sentiment";
import RiskAssessment from "./components/RiskAssessment";
import Personalization from "./components/Personalization";
import Recommendation from "./components/Recommendation";
import Login from "./components/Login";
import Register from "./components/Register";
import HomePage from "./components/HomePage";

function App() {
    return (
        <Router>
           
            <AppBar position="static" sx={{ bgcolor: "red", padding: "10px" }}>
                <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
                    
                    <img src={icon} alt="App Logo" style={{ height: 40, marginRight: 5 }} />
                    <Typography variant="h5" sx={{ color: "white", fontWeight: "bold" }}>
                        FinVasion - The Future of Financial Services
                    </Typography>

                
                    <Box sx={{ display: "flex", gap: "10px" }}>
                        <Button component={Link} to="/register" sx={{ color: "white" }}>Register</Button>
                        <Button component={Link} to="/login" sx={{ color: "white" }}>Login</Button>
                        <Button component={Link} to="/" sx={{ color: "white" }}>Home</Button>
                        <Button component={Link} to="/recommendation" sx={{ color: "white" }}>Recommendation</Button>
                        <Button component={Link} to="/sentiment" sx={{ color: "white" }}>Sentiment</Button>
                        <Button component={Link} to="/risk" sx={{ color: "white" }}>Risk</Button>
                        <Button component={Link} to="/personalization" sx={{ color: "white" }}>Personalization</Button>
                    </Box>

                </Toolbar>
            </AppBar>

            
            <Routes>
                <Route path="/" element={<HomePage/>} />    
                <Route path="/login" element={<Login />} /> 
                <Route path="/register" element={<Register />} />
                <Route path="/recommendation" element={<Recommendation />} />
                <Route path="/sentiment" element={<Sentiment />} />
                <Route path="/risk" element={<RiskAssessment />} />
                <Route path="/personalization" element={<Personalization />} />
            </Routes>
        </Router>
    );
}

export default App;
