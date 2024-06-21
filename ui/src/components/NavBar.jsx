import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

export default function NavBar() {
  return (
    <Paper
      sqaure={true}
      variant="outlined"
      className="header"
      sx={{ width: '100%', height: '10%', background: '#ededed' }}
    >
      <Box
        className="header__container"
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '1.65rem 0',
          paddingLeft: '1.25rem',
          paddingRight: '1.25rem',
          maxHeight: '100%',
          boxSizing: 'border-box',
        }}
      >
        <Typography variant="h5" sx={{ maxHeight: '100%' }}>
          chicago-apartment-data
        </Typography>
      </Box>
    </Paper>
  );
}
