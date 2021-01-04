import json
import pytest

from aws_cdk import core
from lab10.lab10_stack import Lab10Stack


def get_template():
    app = core.App()
    Lab10Stack(app, "lab10")
    return json.dumps(app.synth().get_stack("lab10").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
