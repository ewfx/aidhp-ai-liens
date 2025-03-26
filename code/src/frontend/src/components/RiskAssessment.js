import React, { useEffect, useState } from "react";
import axios from "axios";
import { Typography, Paper } from "@mui/material";
import { getAuthHeaders } from "../services/api";

const API_BASE_URL = "http://localhost:8000";

function RiskAssessment() {
  const [riskScore, setRiskScore] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const userId = localStorage.getItem("cust_id");
    if (!userId) {
      setError("cust_id not found. Please login.");
      return;
    }

    axios
      .get(`${API_BASE_URL}/api/risk/${userId}`, getAuthHeaders())
      .then((res) => {
        console.log("✅ Risk data:", res.data);
        if (res.data.risk_score !== undefined) {
          setRiskScore(res.data.risk_score);
        } else {
          setError("Risk score not available.");
        }
      })
      .catch((err) => {
        console.error("❌ Risk fetch error:", err);
        setError("Failed to fetch risk score.");
      });
  }, []);

  return (
    <>
    <Paper
        elevation={3}
        sx={{
          p: 4,
          borderRadius: 4,
          mt: 6,
          background: "linear-gradient(135deg, #f0f4ff 0%, #e6f7ff 100%)",
        }}
      >
      <Typography variant="h6">Risk Assessment</Typography>
      {error ? (
        <Typography color="error">{error}</Typography>
      ) : riskScore !== null ? (
        <Typography>Your Risk Score: {riskScore}</Typography>
      ) : (
        <Typography>Loading risk score...</Typography>
      )}
      </Paper>
    </>
  );
}

export default RiskAssessment;
