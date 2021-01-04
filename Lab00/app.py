#!/usr/bin/env python3

from aws_cdk import core

from lab00.lab00_stack import Lab00Stack


app = core.App()

#region="us-west-1"
region="cn-northwest-1"

#Lab00Stack(app, "lab00")
Lab00Stack(app, "lab00-"+region,env={"region":region})

app.synth()
