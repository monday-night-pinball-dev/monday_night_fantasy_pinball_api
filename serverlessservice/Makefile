define install-dependencies

	@echo 
	@echo ------------------------ 
	@echo Exporting requirements.txt to root dir
	@echo 

	poetry export --without-hashes --format=requirements.txt > ./requirements.txt

	@echo ------------------------ 
	@echo ------------------------ 
	@echo Exporting requirements.txt to ./app/

	@echo	
	poetry export --without-hashes --format=requirements.txt > ./app/requirements.txt
	@echo ------------------------ 

endef

define cdk-deploy-dev
	$(call install-dependencies)
	cdk deploy --context stage="dev"
endef

define cdk-deploy-prod
	$(call install-dependencies)
	cdk deploy --context stage="prod"
endef 

install-dependencies:
	$(call install-dependencies)

cdk-deploy-dev:
	$(call cdk-deploy-dev)

cdk-deploy-prod:
	$(call cdk-deploy-prod)