import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import NavBar from '../components/NavBar';

export default function Root() {
  return (
    <Box sx={{ height: '100%', width: '100%', display: 'block' }}>
      <NavBar />
      <Container>
        <Outlet />
      </Container>
    </Box>
  );
}
