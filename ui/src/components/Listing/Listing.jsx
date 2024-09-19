import { Typography } from '@mui/material';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

import './Listing.css';

export default function Listing({ address, price, isOver }) {
  return (
    <Paper className="listing" sx={{ boxShadow: 3, '&:hover': { boxShadow: 10 } }}>
      <Box className="listing-header">
        <div className="listing-header-text">{address}</div>
      </Box>
      <Box className="listing-body">
        <div className="listing-body-price">${price}</div>
        <div className="listing-body-text">{isOver ? 'over the estimated price' : 'below the estimated price'}</div>
      </Box>
    </Paper>
  );
}
