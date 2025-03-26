import React from "react";
import { Box, Typography, Container, Paper } from "@mui/material";

const HomePage = ()=>{
    

  return (
    <Container maxWidth="md">
      <Paper
        elevation={3}
        sx={{
          p: 4,
          borderRadius: 4,
          mt: 6,
          background: "linear-gradient(135deg, #f0f4ff 0%, #e6f7ff 100%)",
        }}
      >
        <Typography
          variant="h4"
          sx={{ fontWeight: "bold", color: "#1a237e", mb: 2 }}
        >
          Welcome to <span style={{ color: "#3949ab" }}>FinVasion</span> – Your Smart Finance Partner
        </Typography>
        <Typography variant="body1" sx={{ fontSize: "1.1rem", color: "#424242" }}>
          FinVasion empowers you to make informed financial decisions through personalized recommendations.
          By analyzing your spending behavior, financial risk, and even your social sentiment, we help you discover
          credit cards, loans, and investment products that truly suit <strong>you</strong>.
          All tailored, secure, and easy.
        </Typography>
      </Paper>
    </Container>
  );
};


export default HomePage;