// pages/api/stocks.js
import axios from 'axios';

const fetchStockData = async (ticker) => {
  const response = await axios.get(`https://api.example.com/stock/${ticker}`); // Replace with actual API URL
  return response.data;
};

const handler = async (req, res) => {
  const { ticker } = req.query;

  if (!ticker) {
    return res.status(400).json({ error: 'Ticker is required' });
  }

  try {
    const data = await fetchStockData(ticker);
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch stock data' });
  }
};

export default handler;
