create table if not exists fantasy_teams (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
  owner_id uuid NOT NULL, 
  name varchar(255) NOT NULL, 
  fantasy_league_id uuid NOT NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
 
CREATE INDEX IF NOT EXISTS idx_fantasy_teams_owner_id ON public.fantasy_teams(owner_id); 
CREATE INDEX IF NOT EXISTS idx_fantasy_teams_name ON public.fantasy_teams(name); 
CREATE INDEX IF NOT EXISTS idx_ufantasy_teams_created_at ON public.fantasy_teams(created_at); 
CREATE INDEX IF NOT EXISTS idx_fantasy_teams_fantasy_league_id ON public.fantasy_teams(fantasy_league_id);
 
-- FKs

ALTER TABLE public.fantasy_teams DROP CONSTRAINT IF EXISTS fk_fantasy_teams_owner_id;

ALTER TABLE public.fantasy_teams
  ADD CONSTRAINT fk_fantasy_teams_owner_id
  FOREIGN KEY (owner_id)
  REFERENCES public.users(id);
 
ALTER TABLE public.fantasy_teams DROP CONSTRAINT IF EXISTS fk_fantasy_teams_fantasy_league_id;

ALTER TABLE public.fantasy_teams
  ADD CONSTRAINT fk_fantasy_teams_fantasy_league_id
  FOREIGN KEY (fantasy_league_id)
  REFERENCES public.fantasy_leagues(id);
 