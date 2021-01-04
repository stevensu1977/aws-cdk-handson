import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import cdk = require('@aws-cdk/core');
import Lab05 = require('../lib/lab05-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new Lab05.Lab05Stack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});