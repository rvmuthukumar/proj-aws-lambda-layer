from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    RemovalPolicy,
    BundlingOptions,
    DockerImage,
)

class MyLayerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 bucket for storing artifacts (optional, recommended for distributing to multiple accounts/regions)
        artifact_bucket = s3.Bucket(
            self,
            "LayerArtifactsBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        layer_code_path = "layer_code"  # An empty folder in your repo

        # Create a Lambda Layer with specified dependencies
        my_layer = _lambda.LayerVersion(
            self,
            "MyPythonLayer",
            layer_version_name="mypythonlayer",
            code=_lambda.Code.from_asset(
                layer_code_path,
                bundling=BundlingOptions(
                    image=DockerImage.from_registry("amazonlinux:2"),
                    command=[
                        "bash", "-c",
                        # Install Python 3 + pip, then pip-install dependencies
                        # and zip them up in a structure Lambda expects
                        "yum install -y python3 pip && "
                        "pip3 install "
                        "PyPDF2==3.0.1 "
                        "Faker==15.3.4 "
                        #"boto3==1.36.21 "
                        #"numpy==1.24.2 "
                        #"pandas==1.5.3 "
                        #"scikit-learn==1.2.2 "
                        "-t python/lib/python3.9/site-packages/ && "
                        "rm -rf python/lib/python3.9/site-packages/__pycache__ && "
                        "zip -r layer.zip python && "
                        "mv layer.zip /asset-output/"
                    ],
                    user="root", # When you use AWS CDK’s Docker bundling, you have add the user="root" parameter inside the BundlingOptions
                    # By adding user="root", the container is executed as root, so the yum install commands have the necessary privileges to install Python 3 and pip
                ),
            ),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description="Layer with PyPDF2, Faker, boto3, numpy, pandas, scikit-learn."
            
            
        )

        # Output or store the ARN so other services/stacks can reference the layer
        self.layer_arn = my_layer.layer_version_arn
