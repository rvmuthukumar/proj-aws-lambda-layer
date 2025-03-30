import aws_cdk as cdk
from cdk_app_stack import MyLayerStack

app = cdk.App()

MyLayerStack(app, "MyLayerStack")

app.synth()
