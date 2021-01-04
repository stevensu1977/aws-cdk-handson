#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { Lab09Stack } from '../lib/lab09-stack';

const app = new cdk.App();
new Lab09Stack(app, 'Lab09Stack');
