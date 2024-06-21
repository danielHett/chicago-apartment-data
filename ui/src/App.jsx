import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Container from '@mui/material/Container';
import NavBar from './components/NavBar';
import { Typography } from '@mui/material';

export default function App() {
  return (
    <Box sx={{ height: '100%', width: '100%', display: 'block' }}>
      <NavBar />
      <Container></Container>
    </Box>
  );
}
