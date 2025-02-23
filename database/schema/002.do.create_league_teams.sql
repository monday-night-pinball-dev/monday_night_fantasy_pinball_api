create table if not exists league_teams (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  home_venue_id uuid NOT NULL,
  name varchar(64) NOT NULL,
  short_name varchar(3) NOT NULL, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
    
CREATE INDEX IF NOT EXISTS idx_league_teams_home_venue_id ON public.league_teams(home_venue_id); 
CREATE INDEX IF NOT EXISTS idx_league_teams_name ON public.league_teams(name); 
CREATE INDEX IF NOT EXISTS idx_league_teams_short_name ON public.league_teams(short_name); 
CREATE INDEX IF NOT EXISTS idx_league_teams_created_at ON public.league_teams(created_at); 

-- FKs

ALTER TABLE public.league_teams DROP CONSTRAINT IF EXISTS fk_league_teams_home_venue_id;

ALTER TABLE public.league_teams
  ADD CONSTRAINT fk_league_teams_home_venue_id
  FOREIGN KEY (home_venue_id)
  REFERENCES public.venues(id);