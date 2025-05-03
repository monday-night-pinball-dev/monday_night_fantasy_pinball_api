import { AppShell } from '@mantine/core';
import HomePage from '@/components/HomePage/HomePage';
import TeamPage from '@/components/TeamPage/TeamPage';
import { Routes, Route } from 'react-router-dom';
import { RouteNotFoundPage } from '../RouteNotFoundPage/RouteNotFoundPage';
 
export function MnfpAppShellMain() { 
  return (
    <AppShell.Main>
      <Routes>
        {/* Define your routes here */}
        <Route path="*" element={<RouteNotFoundPage/>} />
        <Route path="/" element={<HomePage/>} />
        <Route path="/home" element={<HomePage/>} />
        <Route path="/team" element={<TeamPage/>} />
        {/* Add more routes as needed */}
      </Routes>
    </AppShell.Main>   
  );
}

