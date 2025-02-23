import os
import aws_cdk as cdk

from stack import MnfpCoreServiceStack

app = cdk.App()

MnfpCoreServiceStack(
    app,
    "mnfp-core-service-stack",
    env={
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
        "region": os.environ["CDK_DEFAULT_REGION"],
    },
)

app.synth()
