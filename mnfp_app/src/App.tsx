import '@mantine/core/styles.css'; 
import { AppShell } from '@mantine/core'; 
import { MnfpAppShellHeader } from './components/MnfpAppShell/MnfpAppShellHeader/MnfpAppShellHeader';
import { MnfpAppShellNavBar } from './components/MnfpAppShell/MnfpAppShellNavBar/MnfpAppShellNavBar';
import { MnfpAppShellMain } from './components/MnfpAppShell/MnfpAppShellMain/MnfpAppShellMain';
import { useDisclosure } from '@mantine/hooks';

export default function App() {
  
  const [opened, {toggle}] = useDisclosure(false);
  
  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{ width: 300, breakpoint: 'sm', collapsed: {mobile: !opened} }}
      padding="md"
    > 
      <MnfpAppShellHeader toggle={toggle} opened={opened}/>
      <MnfpAppShellNavBar/>
      <MnfpAppShellMain/> 
    </AppShell>
  );
}
