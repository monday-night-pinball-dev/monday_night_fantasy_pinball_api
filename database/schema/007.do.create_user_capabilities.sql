create table if not exists user_capabilities (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  user_id uuid NOT NULL, 
  capability varchar(64) NOT NULL UNIQUE,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);   
 
CREATE INDEX IF NOT EXISTS idx_user_capabilities_user_id ON public.users(username); 
CREATE INDEX IF NOT EXISTS idx_user_capabilities_name ON public.users(name); 
CREATE INDEX IF NOT EXISTS idx_user_capabilities_created_at ON public.users(created_at); 

-- FKs

ALTER TABLE public.user_capabilities DROP CONSTRAINT IF EXISTS fk_user_capabilities_user_id;

ALTER TABLE public.user_capabilities
  ADD CONSTRAINT fk_user_capabilities_user_id
  FOREIGN KEY (user_id)
  REFERENCES public.users(id); 

 

 