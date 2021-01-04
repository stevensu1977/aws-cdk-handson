import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as Lab09 from '../lib/lab09-stack';

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new Lab09.Lab09Stack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});
