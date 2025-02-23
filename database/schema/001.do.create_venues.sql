create table if not exists venues (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),   
  	name varchar(64) NOT NULL UNIQUE, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   

CREATE INDEX IF NOT EXISTS idx_venues_name ON public.venues(name); 
CREATE INDEX IF NOT EXISTS idx_venues_created_at ON public.venues(created_at); 
  
 