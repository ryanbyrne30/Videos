import { Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

const Div = styled('div')(({ theme }) => ({
  ...theme.typography.button,
  backgroundColor: theme.palette.background.paper,
  padding: theme.spacing(1),
}));


export default function Home() {
  return (
    <div>
      <Typography variant="h2">
        Home
      </Typography>
    </div>
  )
}
