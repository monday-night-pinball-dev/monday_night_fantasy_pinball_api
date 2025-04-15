create table if not exists fantasy_leagues (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),   
  	name varchar(64) NOT NULL UNIQUE, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   

CREATE INDEX IF NOT EXISTS idx_fantasy_leagues_name ON public.fantasy_leagues(name); 
CREATE INDEX IF NOT EXISTS idx_fantasy_leagues_created_at ON public.fantasy_leagues(created_at); 
  
 