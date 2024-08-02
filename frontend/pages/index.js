import axios from 'axios';
import { useState } from 'react';
import { Box, Button, Container, Heading, Text, VStack, HStack, ChakraProvider } from '@chakra-ui/react';
import { Bar, Line, Pie, PolarArea } from 'react-chartjs-2';
import { useSpring, animated } from 'react-spring';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
} from 'chart.js';
import withAuth from '../components/withAuth';

ChartJS.register(
  Title, Tooltip, Legend, LineElement, PointElement, BarElement, ArcElement, CategoryScale, LinearScale, RadialLinearScale
);

export const getServerSideProps = async () => {
  const tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'META', 'NVDA', 'NFLX', 'BABA', 'V',
    'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
    'NVDA', 'BA', 'SBUX', 'UDMY', 'WMT'
  ];

  const reports = {};
  const alerts = [];

  for (const ticker of tickers) {
    try {
      const response = await axios.get(`http://127.0.0.1:5004/api/kpi/${ticker}`);
      reports[ticker] = response.data;
    } catch (error) {
      reports[ticker] = { error: 'Failed to fetch data' };
    }
  }

  try {
    const alertsResponse = await axios.get('http://127.0.0.1:5004/api/alerts');
    alerts.push(...alertsResponse.data.alerts);
  } catch (error) {
    console.error('Failed to fetch alerts', error);
  }

  const topGainersLosersResponse = await axios.get('http://127.0.0.1:5004/api/top-gainers-losers');
  const topGainersLosers = topGainersLosersResponse.data;

  return {
    props: {
      reports,
      topGainersLosers,
      alerts,
    }
  };
};

const Home = ({ reports, topGainersLosers, alerts }) => {
  const [activeSection, setActiveSection] = useState('dailyClosingPrices');

  const topGainersData = {
    labels: topGainersLosers.top_gainers.map(gainer => gainer.ticker),
    datasets: [
      {
        label: 'Change (%)',
        data: topGainersLosers.top_gainers.map(gainer => gainer.change_percentage),
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 2,
      },
    ],
  };

  const topLosersData = {
    labels: topGainersLosers.top_losers.map(loser => loser.ticker),
    datasets: [
      {
        label: 'Change (%)',
        data: topGainersLosers.top_losers.map(loser => loser.change_percentage),
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 2,
      },
    ],
  };

  const dailyClosingPricesData = {
    labels: Object.keys(reports),
    datasets: [
      {
        label: 'Daily Closing Price',
        data: Object.values(reports).map(report => report.daily_closing_price),
        type: 'bar',
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
      },
    ],
  };

  const changeData = (timeframe, color) => ({
    labels: Object.keys(reports),
    datasets: [
      {
        label: `${timeframe} Change (%)`,
        data: Object.values(reports).map(report => report[`${timeframe}_change`]),
        type: 'line',
        borderColor: color.borderColor,
        backgroundColor: color.backgroundColor,
      },
    ],
  });

  const pieChartData = {
    labels: Object.keys(reports),
    datasets: [
      {
        label: '30d Change (%)',
        data: Object.values(reports).map(report => report['30d_change']),
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)',
          'rgba(255, 159, 64, 0.5)',
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const polarAreaData = {
    labels: Object.keys(reports),
    datasets: [
      {
        label: '24h Change (%)',
        data: Object.values(reports).map(report => report['24h_change']),
        backgroundColor: [
          'rgba(54, 162, 235, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)',
          'rgba(255, 159, 64, 0.5)',
          'rgba(255, 99, 132, 0.5)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const colors = {
    '24h': { borderColor: 'rgba(54, 162, 235, 1)', backgroundColor: 'rgba(54, 162, 235, 0.5)' },
    '30d': { borderColor: 'rgba(75, 192, 192, 1)', backgroundColor: 'rgba(75, 192, 192, 0.5)' },
    '1y': { borderColor: 'rgba(153, 102, 255, 1)', backgroundColor: 'rgba(153, 102, 255, 0.5)' },
  };

  const fadeIn = useSpring({
    opacity: 1,
    from: { opacity: 0 },
    config: { duration: 1000 },
  });

  return (
    <ChakraProvider>
      <Container maxW="container.xl" p={4}>
        <animated.div style={fadeIn}>
          <Heading as="h1" mb={6} textAlign="center">Stock Market KPI Dashboard</Heading>

          <HStack spacing={4} mb={8} justify="center">
            <Button
              onClick={() => setActiveSection('dailyClosingPrices')}
              bgGradient="linear(to-r, teal.500, green.500)"
              color="white"
              _hover={{ bgGradient: 'linear(to-r, teal.600, green.600)', boxShadow: 'xl' }}
            >
              Daily Closing Prices
            </Button>
            <Button
              onClick={() => setActiveSection('24hChange')}
              bgGradient="linear(to-r, blue.400, cyan.400)"
              color="white"
              _hover={{ bgGradient: 'linear(to-r, blue.500, cyan.500)', boxShadow: 'xl' }}
            >
              24h Change
            </Button>
            <Button
              onClick={() => setActiveSection('30dChange')}
              bgGradient="linear(to-r, pink.600, red.500)"
              color="white"
              _hover={{ bgGradient: 'linear(to-r, pink.700, red.600)', boxShadow: 'xl' }}
            >
              30d Change
            </Button>
            <Button
              onClick={() => setActiveSection('1yChange')}
              bgGradient="linear(to-r, orange.400, yellow.400)"
              color="white"
              _hover={{ bgGradient: 'linear(to-r, orange.500, yellow.500)', boxShadow: 'xl' }}
            >
              1y Change
            </Button>
            <Button
              onClick={() => setActiveSection('topGainers')}
              bgGradient="linear(to-r, purple.500, pink.500)"
              color="white"
              _hover={{ bgGradient: 'linear(to-r, purple.600, pink.600)', boxShadow: 'xl' }}
            >
              Top Gainers
            </Button>
            <Button
              onClick={() => setActiveSection('topLosers')}
              bgGradient="linear(to-r, red.500, orange.500)"
              color="white"
              _hover={{ bgGradient: 'linear(to-r, red.600, orange.600)', boxShadow: 'xl' }}
            >
              Top Losers
            </Button>
          </HStack>

          {activeSection === 'dailyClosingPrices' && (
            <Box>
              <Bar data={dailyClosingPricesData} options={{ responsive: true }} />
            </Box>
          )}
          {activeSection === '24hChange' && (
            <Box>
              <PolarArea data={polarAreaData} options={{ responsive: true }} />
            </Box>
          )}
          {activeSection === '30dChange' && (
            <Box>
              <Pie data={pieChartData} options={{ responsive: true }} />
            </Box>
          )}
          {activeSection === '1yChange' && (
            <Box>
              <Line data={changeData('1y', colors['1y'])} options={{ responsive: true }} />
            </Box>
          )}
          {activeSection === 'topGainers' && (
            <Box>
              <Bar data={topGainersData} options={{ responsive: true }} />
            </Box>
          )}
          {activeSection === 'topLosers' && (
            <Box>
              <Bar data={topLosersData} options={{ responsive: true }} />
            </Box>
          )}
        </animated.div>
      </Container>
    </ChakraProvider>
  );
};

export default withAuth(Home);
