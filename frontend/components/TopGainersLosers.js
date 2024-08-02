import React from 'react';

const TopGainersLosers = ({ topGainers, topLosers }) => (
    <div>
        <h2>Top Gainers (24h)</h2>
        <ul>
            {topGainers.map((gainer) => (
                <li key={gainer.ticker}>{gainer.ticker}: {gainer.change_percentage}%</li>
            ))}
        </ul>
        <h2>Top Losers (24h)</h2>
        <ul>
            {topLosers.map((loser) => (
                <li key={loser.ticker}>{loser.ticker}: {loser.change_percentage}%</li>
            ))}
        </ul>
    </div>
);

export default TopGainersLosers;
