#!/usr/bin/env node
import 'source-map-support/register';
import cdk = require('@aws-cdk/core');
import { Lab05Stack } from '../lib/lab05-stack';

const app = new cdk.App();
new Lab05Stack(app, 'Lab05Stack',{env: {
    region: 'us-east-1',
    account:'596030579944'
  }});
