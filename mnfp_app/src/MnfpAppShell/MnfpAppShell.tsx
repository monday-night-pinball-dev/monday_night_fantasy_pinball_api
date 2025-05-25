 
import { Icon2fa, IconDatabaseImport, IconFingerprint, IconHome, IconKey, IconReceipt2, IconSettings } from '@tabler/icons-react';
import classes from './MnfpAppShell.module.css';
import { AppShell, Group, ScrollArea } from '@mantine/core';
import { useState } from 'react'; 
import { NavLink, Route, Routes } from 'react-router-dom';

const navbarItems = [
  { link: '/home', label: 'Home', icon: IconHome },
  { link: '/team', label: 'Team', icon: IconReceipt2 },
  { link: '', label: 'Security', icon: IconFingerprint },
  { link: '', label: 'SSH Keys', icon: IconKey },
  { link: '', label: 'Databases', icon: IconDatabaseImport },
  { link: '', label: 'Authentication', icon: Icon2fa },
  { link: '', label: 'Other Settings', icon: IconSettings },
];
export function MnfpAppShell() {
const [active, setActive] = useState('Billing'); 

  const items = navbarItems.map((item) => (
    <NavLink
      className={classes.link}
      data-active={item.label === active || undefined}
      to={item.link}
      key={item.label}
      onClick={(event) => {
        event.preventDefault();
        setActive(item.label);
      }}
    >
      <item.icon className={classes.linkIcon} stroke={1.5} />
      <span>{item.label}</span>
    </NavLink>
  ));

  return (
      <AppShell
        header={{ height: 60 }}
        navbar={{ width: 300, breakpoint: 'sm' }}
        padding="md"
      >
        <AppShell.Header> 
          <Group h="100%" px="md">
            MNFP
          </Group>
        </AppShell.Header>
        <AppShell.Navbar p="md"> 
  
          <AppShell.Section grow my="md" component={ScrollArea}>
            {items}
          </AppShell.Section>
          <AppShell.Section>
            {/* Footer content goes here */}
            Navbar footer – always at the bottom
            
          </AppShell.Section>
        </AppShell.Navbar>

        <AppShell.Main> 
          <Routes>
            <Route path="/home" element={<div>Home Content</div>} />
            <Route path="/team" element={<div>Team Content</div>} />
          </Routes>
        </AppShell.Main>
      
      
      </AppShell> 
  );
}