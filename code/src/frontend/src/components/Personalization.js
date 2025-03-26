import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Box,
} from "@mui/material";
import { getAuthHeaders } from "../services/api";

const API_BASE_URL = "http://localhost:8000";

function Personalization() {
  const [offers, setOffers] = useState([]);
  const [scores, setScores] = useState({ risk_score: null, sentiment_score: null });

  const fetchPersonalization = async () => {
    const userId = localStorage.getItem("cust_id");
    if (!userId) {
      console.warn("❌ cust_id not found. Please login.");
      return;
    }

    try {
      const res = await axios.get(`${API_BASE_URL}/api/personalize/${userId}`, getAuthHeaders());
      console.log("✅ Offers data:", res.data);
      setOffers(res.data.offers || []);
      setScores({
        risk_score: res.data.risk_score,
        sentiment_score: res.data.sentiment_score,
      });
    } catch (err) {
      console.error("❌ Offers fetch error:", err);
    }
  };

  useEffect(() => {
    fetchPersonalization();
  }, []);

  return (
    <Box p={3}>
      <Typography variant="h5" gutterBottom>
        Personalized Financial Offers
      </Typography>

      <Button variant="contained" onClick={fetchPersonalization}>
        🔄 Recalculate & Refresh
      </Button>

      <Box mt={2}>
        {scores.risk_score !== null && scores.sentiment_score !== null && (
          <Typography variant="subtitle1">
            <strong>Risk Score:</strong> {scores.risk_score.toFixed(2)} / 100 &nbsp;|&nbsp;
            <strong>Sentiment Score:</strong> {(scores.sentiment_score * 100).toFixed(1)}%
          </Typography>
        )}
      </Box>

      {offers.length === 0 ? (
        <Typography mt={2}>No offers available.</Typography>
      ) : (
        <TableContainer component={Paper} sx={{ mt: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Title</strong></TableCell>
                <TableCell><strong>Type</strong></TableCell>
                <TableCell><strong>Min Income</strong></TableCell>
                <TableCell><strong>Max Risk</strong></TableCell>
                <TableCell><strong>Min Sentiment</strong></TableCell>
                <TableCell><strong>Description</strong></TableCell>
                <TableCell><strong>Eligibility</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {offers.map((offer, index) => (
                <TableRow key={index}>
                  <TableCell>{offer.title}</TableCell>
                  <TableCell>{offer.type}</TableCell>
                  <TableCell>{offer.min_income}</TableCell>
                  <TableCell>{offer.max_risk}</TableCell>
                  <TableCell>{(offer.min_sentiment * 100).toFixed(0)}%</TableCell>
                  <TableCell>{offer.description}</TableCell>
                  <TableCell>
                    {offer.recommended ? (
                      <span style={{ color: "green", fontWeight: "bold" }}>✔ Recommended</span>
                    ) : (
                      <span style={{ color: "red", fontWeight: "bold" }}>✖ Not Recommended</span>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
}

export default Personalization;