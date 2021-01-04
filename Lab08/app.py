#!/usr/bin/env python3

from aws_cdk import core

from lab08.lab08_stack import Lab08Stack


app = core.App()
#Lab08Stack(app, "lab08",env={"region":"us-east-1","account":"596030579944"})
Lab08Stack(app, "lab08",env={"region":"cn-northwest-1","account":"188642756190"})


app.synth()
