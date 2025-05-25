import { AppShell } from '@mantine/core';
import HomePage from '@/Pages/HomePage/HomePage';
import TeamPage from '@/Pages/TeamPage/TeamPage';
import GamedayPage from '@/Pages/GamedayPage/GamedayPage';
import PlayersPage from '@/Pages/PlayersPage/PlayersPage';
import AdminUsersPage from '@/Pages/AdminUsersPage/AdminUsersPage';
import AdminVenuesPage from '@/Pages/AdminVenuesPage/AdminVenuesPage';
import AdminLeagueTeamsPage from '@/Pages/AdminLeagueTeamsPage/AdminLeagueTeamsPage';
import AdminLeaguePlayersPage from '@/Pages/AdminLeaguePlayersPage/AdminLeaguePlayersPage';
import AdminFantasyLeaguesPage from '@/Pages/AdminFantasyLeaguesPage/AdminFantasyLeaguesPage';
import AdminFantasyTeamsPage from '@/Pages/AdminFantasyTeamsPage/AdminFantasyTeamsPage';
import AdminSeasonsPage from '@/Pages/AdminSeasonsPage/AdminSeasonsPage';
import AdminFantasyTeamSeasonLinksPage from '@/Pages/AdminFantasyTeamSeasonLinksPage/AdminFantasyTeamSeasonLinksPage'; 
import AdminLeaguePlayerFantasyTeamSeasonLinksPage from '@/Pages/AdminLeaguePlayerFantasyTeamSeasonLinksPage/AdminLeaguePlayerFantasyTeamSeasonLinkPages';
import { Routes, Route } from 'react-router-dom';
import { RouteNotFoundPage } from '../../Pages/RouteNotFoundPage/RouteNotFoundPage';  
import { AdminSeasonProfilePage } from '@/Pages/AdminSeasonsPage/AdminSeasonProfilePage';
import { AdminVenueProfilePage } from '@/Pages/AdminVenuesPage/AdminVenueProfilePage';
import { AdminLeagueTeamProfilePage } from '@/Pages/AdminLeagueTeamsPage/AdminLeagueTeamProfilePage';
import { ProfileModes } from '@/Components/EntityProfileComponents/MnfpEntityProfile';
 
export function MnfpAppShellMain() { 
  return (
    <AppShell.Main>
      <Routes>
        {/* Define your routes here */}
        <Route path="*" element={<RouteNotFoundPage/>} />
        <Route path="/" element={<HomePage/>} />
        <Route path="/home" element={<HomePage/>} />
        <Route path="/team" element={<TeamPage/>} /> 
        <Route path="/gameday" element={<GamedayPage/>} /> 
        <Route path="/players" element={<PlayersPage/>} /> 
        <Route path="/admin/users" element={<AdminUsersPage/>} />
        <Route path="/admin/venues" element={<AdminVenuesPage/>} />
        <Route path="/admin/leagueTeams" element={<AdminLeagueTeamsPage/>} />
        <Route path="/admin/leaguePlayers" element={<AdminLeaguePlayersPage/>} />
        <Route path="/admin/fantasyLeagues" element={<AdminFantasyLeaguesPage/>} />
        <Route path="/admin/fantasyTeams" element={<AdminFantasyTeamsPage/>} /> 
        <Route path="/admin/seasons" element={ <AdminSeasonsPage /> } />
        <Route path="/admin/fantasyTeamSeasonLinks" element={ <AdminFantasyTeamSeasonLinksPage /> } />
        <Route path="/admin/leaguePlayerFantasyTeamSeasonLinks" element={ <AdminLeaguePlayerFantasyTeamSeasonLinksPage /> } />

        <Route path="/admin/venues/:id" element={<AdminVenueProfilePage mode={ProfileModes.READ}/>} />
        <Route path="/admin/leagueTeams/:id" element={<AdminLeagueTeamProfilePage mode={ProfileModes.READ}/>} />
        <Route path="/admin/leaguePlayers/:id" element={<AdminLeaguePlayersPage/>} />
        <Route path="/admin/fantasyLeagues/:id" element={<AdminFantasyLeaguesPage/>} />
        <Route path="/admin/fantasyTeams/:id" element={<AdminFantasyTeamsPage/>} />
        <Route path="/admin/seasons/:id" element={<AdminSeasonProfilePage mode={ProfileModes.READ}/>} />
        <Route path="/admin/fantasyTeamSeasonLinks/:id" element={<AdminFantasyTeamSeasonLinksPage/>} />
        <Route path="/admin/leaguePlayerFantasyTeamSeasonLinks/:id" element={<AdminLeaguePlayerFantasyTeamSeasonLinksPage/>} />
        <Route path="/admin/users/:id" element={<AdminUsersPage/>} /> 

        <Route path="/admin/seasons/:id/edit" element={<AdminSeasonProfilePage mode={ProfileModes.EDIT}/>} />
        <Route path="/admin/venues/:id/edit" element={<AdminVenueProfilePage mode={ProfileModes.EDIT}/>} />
        <Route path="/admin/leagueTeams/:id/edit" element={<AdminLeagueTeamProfilePage mode={ProfileModes.EDIT}/>} />
        
        {/* Add more routes as needed */}
      </Routes>
    </AppShell.Main>   
  );
}

