#!/usr/bin/env python3

from aws_cdk import core

from lab02.lab02_stack import Lab02Stack


app = core.App()
Lab02Stack(app, "lab02",env={"region":"ap-northeast-1"})

app.synth()
