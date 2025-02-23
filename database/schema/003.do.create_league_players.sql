create table if not exists league_players (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  league_team_id uuid NULL, 
  full_name varchar(255) NOT NULL UNIQUE,   
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
    
CREATE INDEX IF NOT EXISTS idx_league_players_league_team_id ON public.league_players(league_team_id);  
CREATE INDEX IF NOT EXISTS idx_league_players_full_name ON public.league_players(full_name); 
CREATE INDEX IF NOT EXISTS idx_league_players_created_at ON public.league_players(created_at);  