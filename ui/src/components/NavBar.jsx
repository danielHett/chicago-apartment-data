import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Logo from './Logo';
import Stack from '@mui/material/Stack';
import NavButton from './NavButton';

const buttons = [
  {
    label: 'Home',
    pathPart: '/',
  },
  {
    label: 'Statistics',
    pathPart: '/stats',
  },
];

export default function NavBar() {
  return (
    <Paper
      sqaure={true}
      variant="outlined"
      className="header"
      sx={{ width: '100%', height: '83px', background: '#ededed', marginBottom: '10px' }}
    >
      <Box
        className="header__container"
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          paddingLeft: '1.25rem',
          paddingRight: '1.25rem',
          height: '100%',
          maxHeight: '100%',
          boxSizing: 'border-box',
        }}
      >
        <Logo />
        <Stack spacing={2} direction="row">
          {buttons.map((button) => {
            return NavButton(button);
          })}
        </Stack>
      </Box>
    </Paper>
  );
}
