 
import { AppShell, Button } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
 
export function MnfpAppShellNavBar() {
  const navigate = useNavigate(); 
  
  return (
    <AppShell.Navbar p="md" style={{gap: '10px'}}>
      <Button
        variant="subtle"
        onClick={() => navigate('/home')}
        style={{ width: '100%', margin: '5px' }}
      >
        Home
      </Button>
      <Button
        variant="subtle"
        onClick={() => navigate('/team')}
        style={{ width: '100%', margin: '5px' }}
      >
        Team
      </Button>
    </AppShell.Navbar>
  );
}