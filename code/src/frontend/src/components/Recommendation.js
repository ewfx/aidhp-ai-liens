import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Button, Card, CardContent, Typography } from "@mui/material";
import { getAuthHeaders } from "../services/api";

const API_BASE_URL = "http://localhost:8000";

function Recommendation() {
  const [recommendation, setRecommendation] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const userId = localStorage.getItem("cust_id");
    if (!userId) {
      console.warn("❌ cust_id not found. Please login.");
    }
  }, []);

  const handleFetch = async () => {
    const userId = localStorage.getItem("cust_id");
    if (!userId) return;

    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE_URL}/api/recommend/${userId}`, getAuthHeaders());
      if (res.data?.recommendation) {
        setRecommendation(res.data.recommendation);
      } else {
        setRecommendation("⚠️ Unable to fetch recommendation.");
      }
    } catch (err) {
      console.error("❌ Error fetching recommendation:", err);
      setRecommendation("⚠️ Error fetching recommendation.");
    }
    setLoading(false);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Personalized Financial Product Recommendation
      </Typography>
      <Button
        variant="contained"
        onClick={handleFetch}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? "Loading..." : "Get Recommendation"}
      </Button>

      {recommendation && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
              {recommendation}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}

export default Recommendation;
