#!/usr/bin/env python3

from aws_cdk import core

from lab04.lab04_stack import Lab04Stack


app = core.App()



Lab04Stack(app, "lab04-app")

app.synth()
