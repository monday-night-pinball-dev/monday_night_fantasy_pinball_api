 
import { AppShell, Burger, Button, Flex, useComputedColorScheme, useMantineColorScheme } from '@mantine/core';
import { FaRegLightbulb, FaMoon } from 'react-icons/fa'; 

  
export function MnfpAppShellHeader({toggle, opened} : any) {
 
  const { setColorScheme } = useMantineColorScheme();
  const computedColorScheme = useComputedColorScheme('light');

  const toggleColorScheme = () => {
    setColorScheme(computedColorScheme === 'dark' ? 'light' : 'dark');
  };
  
  return (
    <AppShell.Header>
      <Flex justify="space-between" align='center' style={{padding: '10px 20px'}}>
        <Burger
          opened={opened}
          onClick={toggle} 
          hiddenFrom="sm" 
        /> 
        <div> 
            MNFP 
        </div>
        <Button 
          size="sm" 
          variant="link"
          onClick={toggleColorScheme}>
          
          {computedColorScheme === 'dark' ? <FaRegLightbulb/> : computedColorScheme === 'light' ? <FaMoon/> : <FaMoon/>}
        </Button>
      </Flex>
    </AppShell.Header>
  );
}