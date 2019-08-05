#!/usr/bin/env python3

from aws_cdk import core

from lab03.lab03_stack import Lab03Stack


app = core.App()
Lab03Stack(app, "lab03",env={"region":"ap-northeast-1"})

app.synth()
