create table if not exists league_player_fantasy_team_season_links (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  league_player_id uuid NOT NULL,
  league_team_id_dn uuid NULL,
  fantasy_team_season_link_id uuid NOT NULL, 
  season_id_dn uuid NOT NULL, 
  fantasy_team_id_dn uuid NOT NULL, 
  fantasy_league_id_dn uuid NOT NULL,
  fantasy_team_owner_id_dn uuid NOT NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
 

CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_league_player_id ON public.league_player_fantasy_team_season_links(league_player_id);  
CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_league_team_id_dn ON public.league_player_fantasy_team_season_links(league_team_id_dn);

CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_fantasy_team_season_link_id ON public.league_player_fantasy_team_season_links(fantasy_team_season_link_id);
CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_season_id_dn ON public.league_player_fantasy_team_season_links(season_id_dn);
CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_fantasy_team_id_dn ON public.league_player_fantasy_team_season_links(fantasy_team_id_dn); 
CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_fantasy_league_id_dn ON public.league_player_fantasy_team_season_links(fantasy_league_id_dn); 
CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_fantasy_team_owner_id_dn ON public.league_player_fantasy_team_season_links(fantasy_team_owner_id_dn);

CREATE INDEX IF NOT EXISTS idx_league_player_fantasy_team_season_links_created_at ON public.league_player_fantasy_team_season_links(created_at);  
 
-- FKs
 
ALTER TABLE public.league_player_fantasy_team_season_links DROP CONSTRAINT IF EXISTS fk_league_player_fantasy_team_season_links_fantasy_team_season_link_id;

ALTER TABLE public.league_player_fantasy_team_season_links 
  ADD CONSTRAINT fk_league_player_fantasy_team_season_links_fantasy_team_season_link_id
  FOREIGN KEY (fantasy_team_season_link_id)
  REFERENCES public.fantasy_team_season_links(id); 

ALTER TABLE public.league_player_fantasy_team_season_links DROP CONSTRAINT IF EXISTS fk_league_player_fantasy_team_season_links_league_player_id;
ALTER TABLE public.league_player_fantasy_team_season_links 
  ADD CONSTRAINT fk_league_player_fantasy_team_season_links_league_player_id
  FOREIGN KEY (league_player_id)
  REFERENCES public.league_players(id);
 

 
  


 

 