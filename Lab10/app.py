#!/usr/bin/env python3

from aws_cdk import core

from lab10.lab10_stack import Lab10Stack


app = core.App()
#Lab10Stack(app, "lab10", env={'region': 'us-west-2'})

Lab10Stack(app, "lab10", env={'region': 'cn-northwest-1','account':'188642756190'})


app.synth()
