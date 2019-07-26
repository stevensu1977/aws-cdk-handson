#!/usr/bin/env python3

from aws_cdk import core

from lab01.lab01_stack import Lab01Stack


app = core.App()

Lab01Stack(app, "lab01-ap",env={"region":"ap-northeast-1"})
#create second bucket different region
#Lab01Stack(app, "lab01-us",env={"region":"us-west-2"})


app.synth()
