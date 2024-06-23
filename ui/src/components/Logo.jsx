import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

export default function Logo() {
  return (
    <Box sx={{ height: '100%', maxHeight: '100%', boxSizing: 'border-box' }}>
      <Typography
        textAlign="right"
        sx={{ fontWeight: 'bold', height: '1.33', fontSize: '1.15rem', boxSizing: 'border-box' }}
      >
        Chicago
      </Typography>
      <Typography
        textAlign="right"
        sx={{ fontWeight: 'bold', height: '1.33', fontSize: '1.15rem', boxSizing: 'border-box' }}
      >
        Apartment
      </Typography>
      <Typography
        textAlign="right"
        sx={{ fontWeight: 'bold', height: '1.33', fontSize: '1.15rem', boxSizing: 'border-box' }}
      >
        Data
      </Typography>
    </Box>
  );
}
