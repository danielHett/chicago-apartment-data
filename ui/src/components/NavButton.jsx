import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';

export default function NavButton({ label, path }) {
  const navigate = useNavigate();

  return (
    <Button variant="text" color="secondary" onClick={() => navigate(path)}>
      {label}
    </Button>
  );
}
