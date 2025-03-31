from cdk_app.cdk_app_stack import MyLayerStack
import unittest
from aws_cdk import App


class TestMyLayerStack(unittest.TestCase):

    def test_layer_stack_creation(self):
        app = App()
        stack = MyLayerStack(app, "TestStack")
        synthesized_stack = app.synth().get_stack_by_name("TestStack")
        template = synthesized_stack.template

        resources = template["Resources"]
        layer_resources = [
            r for r in resources 
            if resources[r]["Type"] == "AWS::Lambda::LayerVersion"
        ]
        self.assertEqual(
            1, 
            len(layer_resources),
            "There should be exactly one Lambda LayerVersion resource."
        )

if __name__ == "__main__":
    unittest.main()
