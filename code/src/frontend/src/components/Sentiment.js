import React, { useEffect, useState } from "react";
import axios from "axios";
import { Typography, Box, Divider,Paper } from "@mui/material";
import { getAuthHeaders } from "../services/api";

const API_BASE_URL = "http://localhost:8000";

function Sentiment() {
  const [sentimentData, setSentimentData] = useState(null);

  useEffect(() => {
    const userId = localStorage.getItem("cust_id");
    if (!userId) {
      console.warn("❌ cust_id not found. Please login.");
      return;
    }

    axios
      .get(`${API_BASE_URL}/api/sentiment/${userId}`, getAuthHeaders())
      .then((res) => {
        console.log("✅ Sentiment data:", res.data);
        setSentimentData(res.data);
      })
      .catch((err) => {
        console.error("❌ Sentiment fetch error:", err);
      });
  }, []);

  return (
    <Paper
        elevation={3}
        sx={{
          p: 4,
          borderRadius: 4,
          mt: 6,
          background: "linear-gradient(135deg, #f0f4ff 0%, #e6f7ff 100%)",
        }}
      >
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
         Social Media Sentiment Analysis
      </Typography>

      {!sentimentData ? (
        <Typography>Calculating Overall Sentimental Outlook...</Typography>
      ) : (
        <>
          <Typography variant="subtitle1" sx={{ fontWeight: "bold" }}>
            Overall Sentiment: {sentimentData.overall_sentiment}
          </Typography>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Positive Sentiment Ratio: {(sentimentData.positive_ratio * 100).toFixed(1)}%
          </Typography>

          <Divider sx={{ my: 2 }} />

          {sentimentData.sentiment_analysis.map((item, index) => (
            <Box key={index} sx={{ mb: 1 }}>
              <Typography variant="body2">📝 {item.post}</Typography>
              <Typography variant="caption">Sentiment: <strong>{item.sentiment}</strong></Typography>
            </Box>
          ))}
        </>
      )}
    </Box>
    </Paper>
  );
}

export default Sentiment;
