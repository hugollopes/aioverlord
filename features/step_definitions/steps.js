const { defineSupportCode } = require('cucumber')

const steps = require('./steps/steps');
// check here for more examples: https://github.com/jumasheff/nightwatch-cucumber-e2e-testing-example/blob/master/features/step_definitions/steps.js

defineSupportCode((gherkinObj) => {
  steps(gherkinObj)
});
