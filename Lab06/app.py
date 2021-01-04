#!/usr/bin/env python3

from aws_cdk import core

from lab06.eks_worker_nodes_stack import EksWorkerNodesStack


app = core.App()
env = core.Environment(account='111111111111', region='us-east-1')
EksWorkerNodesStack(app, "eks-worker-nodes", env=env)

app.synth()
