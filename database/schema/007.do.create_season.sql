create table if not exists seasons (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  	season_number int NOT NULL UNIQUE ,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
  
CREATE INDEX IF NOT EXISTS idx_seasons_season_number ON public.seasons(season_number);  
 