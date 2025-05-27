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
import { AdminSeasonProfileReadPage } from '@/Pages/AdminSeasonsPage/AdminSeasonProfileReadPage';
import { AdminSeasonProfileEditPage } from '@/Pages/AdminSeasonsPage/AdminSeasonProfileEditPage';
import {AdminLeagueTeamProfileEditPage} from '@/Pages/AdminLeagueTeamsPage/AdminLeagueTeamProfileEditPage';
import { AdminVenueProfileReadPage } from '@/Pages/AdminVenuesPage/AdminVenueProfileReadPage';
import { AdminLeagueTeamProfileReadPage } from '@/Pages/AdminLeagueTeamsPage/AdminLeagueTeamProfileReadPage';
import { AdminVenueProfileEditPage } from '@/Pages/AdminVenuesPage/AdminVenueProfileEditPage';
import { AdminLeaguePlayerProfileEditPage } from '@/Pages/AdminLeaguePlayersPage/AdminLeaguePlayerProfileEditPage';
import { AdminLeaguePlayerProfileReadPage } from '@/Pages/AdminLeaguePlayersPage/AdminLeaguePlayerProfileReadPage';
import { AdminFantasyLeagueProfileReadPage } from '@/Pages/AdminFantasyLeaguesPage/AdminFantasyLeagueProfileReadPage';
import { AdminFantasyLeagueProfileEditPage } from '@/Pages/AdminFantasyLeaguesPage/AdminFantasyLeagueProfileEditPage';
import { AdminUserProfileReadPage } from '@/Pages/AdminUsersPage/AdminUserProfileReadPage';
import { AdminUserProfileEditPage } from '@/Pages/AdminUsersPage/AdminUserProfileEditPage';
import { AdminFantasyTeamProfileReadPage } from '@/Pages/AdminFantasyTeamsPage/AdminFantasyTeamProfileReadPage';
import { AdminFantasyTeamProfileEditPage } from '@/Pages/AdminFantasyTeamsPage/AdminFantasyTeamProfileEditPage';
 
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
        <Route path="/admin/league_teams" element={<AdminLeagueTeamsPage/>} />
        <Route path="/admin/league_players" element={<AdminLeaguePlayersPage/>} />
        <Route path="/admin/fantasy_leagues" element={<AdminFantasyLeaguesPage/>} />
        <Route path="/admin/fantasy_teams" element={<AdminFantasyTeamsPage/>} /> 
        <Route path="/admin/seasons" element={ <AdminSeasonsPage /> } />
        <Route path="/admin/fantasy_team_season_links" element={ <AdminFantasyTeamSeasonLinksPage /> } />
        <Route path="/admin/league_player_fantasy_team_season_links" element={ <AdminLeaguePlayerFantasyTeamSeasonLinksPage /> } />

        <Route path="/admin/venues/:id" element={<AdminVenueProfileReadPage/>} />
        <Route path="/admin/league_teams/:id" element={<AdminLeagueTeamProfileReadPage />} />
        <Route path="/admin/league_players/:id" element={<AdminLeaguePlayerProfileReadPage/>} />
        <Route path="/admin/fantasy_leagues/:id" element={<AdminFantasyLeagueProfileReadPage/>} />
        <Route path="/admin/fantasy_teams/:id" element={<AdminFantasyTeamProfileReadPage/>} />
        <Route path="/admin/seasons/:id" element={<AdminSeasonProfileReadPage />} />
        <Route path="/admin/fantasy_team_season_links/:id" element={<AdminFantasyTeamSeasonLinksPage/>} />
        <Route path="/admin/league_player_fantasy_team_season_links/:id" element={<AdminLeaguePlayerFantasyTeamSeasonLinksPage/>} />
        <Route path="/admin/users/:id" element={<AdminUserProfileReadPage/>} /> 

        <Route path="/admin/seasons/:id/edit" element={<AdminSeasonProfileEditPage />} />
        <Route path="/admin/venues/:id/edit" element={<AdminVenueProfileEditPage />} />
        <Route path="/admin/league_teams/:id/edit" element={<AdminLeagueTeamProfileEditPage />} />
        <Route path="/admin/league_players/:id/edit" element={<AdminLeaguePlayerProfileEditPage/>} />
        <Route path="/admin/fantasy_leagues/:id/edit" element={<AdminFantasyLeagueProfileEditPage/>} />  
        <Route path="/admin/fantasy_teams/:id/edit" element={<AdminFantasyTeamProfileEditPage/>} />
        <Route path="/admin/fantasy_team_season_links/:id/edit" element={<AdminFantasyTeamSeasonLinksPage/>} />
        <Route path="/admin/league_player_fantasy_team_season_links/:id/edit" element={<AdminLeaguePlayerFantasyTeamSeasonLinksPage/>} />
        <Route path="/admin/users/:id/edit" element={<AdminUserProfileEditPage/>} />
        
        {/* Add more routes as needed */}
      </Routes>
    </AppShell.Main>   
  );
}

