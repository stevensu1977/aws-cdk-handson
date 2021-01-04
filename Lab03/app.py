#!/usr/bin/env python3

from aws_cdk import core

from lab03.lab03_stack import Lab03Stack


app = core.App()

region="cn-northwest-1"
#region="us-east-1"
Lab03Stack(app, "lab03-"+region,env={"region":region})


app.synth()
