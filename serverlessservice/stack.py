import json
from os import path

import aws_cdk as cdk
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_apigateway as apigateway
from aws_cdk.aws_apigateway import Cors, CorsOptions
import aws_cdk.aws_lambda_python_alpha as python_lambda
import aws_cdk.aws_ec2 as ec2 


class DicsCoreServiceStack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        stage = self.node.try_get_context('stage') or 'dev'
        
        cds_name = 'core-data-service'
        
        cds_prefix = f'{stage}-{cds_name}'
        
        print(stage)
        
        core_vpc = ec2.Vpc(
            self, 
            f'{cds_prefix}-vpc', 
            vpc_name=f'{cds_prefix}-vpc',
            ip_addresses= cdk.aws_ec2.IpAddresses.cidr("10.0.0.0/24"),
            max_azs= 2,
            subnet_configuration = [ 
                cdk.aws_ec2.SubnetConfiguration( 
                    name= 'public', 
                    subnet_type= cdk.aws_ec2.SubnetType.PUBLIC 
                )
            ],
            nat_gateways=0
        )
        
        core_db_securitygroup = cdk.aws_ec2.SecurityGroup(
            self, 
            f'{cds_prefix}-security-group',
            vpc = core_vpc,
            allow_all_outbound=True 
        )
        
        core_db_securitygroup.add_ingress_rule(
            peer = cdk.aws_ec2.Peer.any_ipv4(),
            connection=cdk.aws_ec2.Port.tcp(5432),
            description='allow inbound traffic from anywhere to the db on port 5432'
        )
        
        admin_credential_secret = cdk.aws_rds.DatabaseSecret(
            self, 
            f'{cds_prefix}-db-credentials', 
            username='dics_admin',
            dbname= "dics",      
            secret_name= f'{cds_prefix}-db-credentials'
        )
        
        migrator_credential_secret = cdk.aws_rds.DatabaseSecret(
            self, 
            f'{cds_prefix}-db-migrator-credentials', 
            username='dics_migrator',
            dbname= "dics",      
            secret_name= f'{cds_prefix}-db-migrator-credentials'
        )
                
        service_credential_secret = cdk.aws_rds.DatabaseSecret(
            self, 
            f'{cds_prefix}-db-service-credentials', 
            username='dics_service',
            dbname= "dics",      
            secret_name= f'{cds_prefix}-db-service-credentials'
        )
 
        database_credentials = cdk.aws_rds.Credentials.from_secret(admin_credential_secret)
          
        database = cdk.aws_rds.DatabaseInstance(
            self, 
            f'{cds_prefix}-db',
            engine = cdk.aws_rds.DatabaseInstanceEngine.postgres(
                version=cdk.aws_rds.PostgresEngineVersion.VER_16_4
            ), 
            instance_type=cdk.aws_ec2.InstanceType.of(cdk.aws_ec2.InstanceClass.T4G,instance_size=cdk.aws_ec2.InstanceSize.MICRO),
            database_name='dics',
            credentials=database_credentials,
            port=5432,
            vpc=core_vpc,
            publicly_accessible=True,
            auto_minor_version_upgrade=True,
            security_groups=[core_db_securitygroup],
            vpc_subnets=cdk.aws_ec2.SubnetSelection(
                subnets=core_vpc.select_subnets(
                    subnet_type=cdk.aws_ec2.SubnetType.PUBLIC
                ).subnets
            )
        ) 
         
        lambda_function = python_lambda.PythonFunction(
            self,
            f'{cds_prefix}-api-lambda',
            entry=path.join(path.dirname(__file__), "app"),
            runtime=lambda_.Runtime.PYTHON_3_12,
            index="main.py",
            memory_size=1024,
            timeout=cdk.Duration.seconds(300),
            vpc=core_vpc,
            allow_public_subnet=True,
            bundling= python_lambda.BundlingOptions(
                asset_excludes=[
                    "*cdk*"
                ],
                
            )
        )
        
        
        
        database.grant_connect(lambda_function, db_user='dics_service')

        api = apigateway.LambdaRestApi(
            self, 
            f"{cds_prefix}-api-gateway", 
            handler=lambda_function, 
            default_cors_preflight_options=CorsOptions(
                allow_origins=Cors.ALL_ORIGINS, 
                allow_methods=Cors.ALL_METHODS, 
                allow_headers=Cors.DEFAULT_HEADERS + ["Authorization", "Samson-Hydration"]
            ),
            proxy=True,
        )
         
        
         
        
 