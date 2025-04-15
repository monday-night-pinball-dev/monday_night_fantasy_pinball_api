create table if not exists users (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
  league_player_id uuid NULL,
  username varchar(320) NOT NULL, 
  name varchar(255) NOT NULL UNIQUE, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
 
CREATE INDEX IF NOT EXISTS idx_users_username ON public.users(username); 
CREATE INDEX IF NOT EXISTS idx_users_name ON public.users(name); 
CREATE INDEX IF NOT EXISTS idx_users_created_at ON public.users(created_at); 

-- FKs

ALTER TABLE public.users DROP CONSTRAINT IF EXISTS fk_users_league_player_id;

ALTER TABLE public.users
  ADD CONSTRAINT fk_users_league_player_id
  FOREIGN KEY (league_player_id)
  REFERENCES public.league_players(id); 
 