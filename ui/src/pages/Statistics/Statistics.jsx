import { Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import Paper from '@mui/material/Paper';
import StatisticsTable from './StatisticsTable';

const columns = ['Date', 'Total Units', 'Average Price'];

const rows = [
  {
    key: 0,
    Date: '07/01/2024',
    'Total Units': '1,232',
    'Average Price': '$1,231',
  },
  {
    key: 1,
    Date: '07/07/2024',
    'Total Units': '1,442',
    'Average Price': '$1,300',
  },
  {
    key: 2,
    Date: '07/14/2024',
    'Total Units': '1,134',
    'Average Price': '$1,131',
  },
];

export default function Statistics() {
  let [avgRent, setAvgRent] = useState('Loading...');
  let [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAvgRent = async () => {
      setTimeout(() => {
        setAvgRent('$2,300');
        setIsLoading(false);
      }, 4000);
    };

    if (isLoading) fetchAvgRent();
  });

  return (
    <>
      <StatisticsTable title="Average Rent in Chicago" columns={columns} rows={rows} />
    </>
  );
}
