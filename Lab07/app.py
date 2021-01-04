#!/usr/bin/env python3

from aws_cdk import core

from lab07.lab07_stack import Lab07Stack


app = core.App()

region="ap-southeast-1"

Lab07Stack(app, "lab07",env={"region":region})

app.synth()
