create table if not exists league_players (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
	league_team_id uuid NULL, 
	name varchar(255) NOT NULL UNIQUE,   
	global_mnp_id uuid NOT NULL UNIQUE,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
    
CREATE INDEX IF NOT EXISTS idx_league_players_league_team_id ON public.league_players(league_team_id);  
CREATE INDEX IF NOT EXISTS idx_league_players_name ON public.league_players(name); 
CREATE INDEX IF NOT EXISTS idx_league_players_created_at ON public.league_players(created_at);  

ALTER TABLE public.league_players DROP CONSTRAINT IF EXISTS fk_league_players_league_team_id;

ALTER TABLE public.league_players
  ADD CONSTRAINT fk_league_players_league_team_id
  FOREIGN KEY (league_team_id)
  REFERENCES public.league_teams(id); 