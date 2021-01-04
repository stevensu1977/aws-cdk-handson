#!/usr/bin/env python3

from aws_cdk import core

from lab11.lab11_stack import Lab11Stack



app = core.App()
Lab11Stack(app, "lab11", env={"account":"596030579944","region":"us-east-1"})

app.synth()





