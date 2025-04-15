create table if not exists fantasy_team_season_links (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  season_id uuid NOT NULL, 
  fantasy_team_id uuid NOT NULL, 
  fantasy_league_id_dn uuid NOT NULL,
  fantasy_team_owner_id_dn uuid NOT NULL, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
 

CREATE INDEX IF NOT EXISTS idx_fantasy_team_season_links_created_at ON public.fantasy_team_season_links(created_at);  
CREATE INDEX IF NOT EXISTS idx_fantasy_team_season_links_season_id ON public.fantasy_team_season_links(season_id); 
CREATE INDEX IF NOT EXISTS idx_fantasy_team_season_links_fantasy_team_id ON public.fantasy_team_season_links(fantasy_team_id); 
CREATE INDEX IF NOT EXISTS idx_fantasy_team_season_links_fantasy_league_id_dn ON public.fantasy_team_season_links(fantasy_league_id_dn); 
CREATE INDEX IF NOT EXISTS idx_fantasy_team_season_links_fantasy_team_owner_id_dn ON public.fantasy_team_season_links(fantasy_team_owner_id_dn); 
 
-- FKs


ALTER TABLE public.fantasy_team_season_links DROP CONSTRAINT IF EXISTS fk_fantasy_team_season_links_season_id;

ALTER TABLE public.fantasy_team_season_links 
  ADD CONSTRAINT fk_fantasy_team_season_links_season_id
  FOREIGN KEY (season_id)
  REFERENCES public.seasons(id); 

ALTER TABLE public.fantasy_team_season_links DROP CONSTRAINT IF EXISTS fk_fantasy_team_season_links_fantasy_team_id;

ALTER TABLE public.fantasy_team_season_links 
  ADD CONSTRAINT fk_fantasy_team_season_links_fantasy_team_id
  FOREIGN KEY (fantasy_team_id)
  REFERENCES public.fantasy_teams(id);

ALTER TABLE public.fantasy_team_season_links DROP CONSTRAINT IF EXISTS fk_fantasy_team_season_links_fantasy_league_id_dn;

ALTER TABLE public.fantasy_team_season_links 
  ADD CONSTRAINT fk_fantasy_team_season_links_fantasy_league_id_dn
  FOREIGN KEY (fantasy_league_id_dn)
  REFERENCES public.fantasy_leagues(id);

ALTER TABLE public.fantasy_team_season_links DROP CONSTRAINT IF EXISTS fk_fantasy_team_season_links_fantasy_team_owner_id_dn;

ALTER TABLE public.fantasy_team_season_links 
  ADD CONSTRAINT fk_fantasy_team_season_links_fantasy_team_owner_id_dn
  FOREIGN KEY (fantasy_team_owner_id_dn)
  REFERENCES public.users(id);
 
 

 