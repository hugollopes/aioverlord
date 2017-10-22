
const { client } = require('nightwatch-cucumber');


function steps({ Given, Then }) {
  Given(/^I open application$/, () => {
    return client
        .url('http://localhost:8080/#/')
        .waitForElementVisible('#app', 5000);
  });
  Given(/^I click button label data$/, () => {
    return client
        .click('button[id=Downmenubutton]')
        .pause(4000);
  });
  Given(/^I click button file upload$/, () => {
    return client
        .click('button[id=debugFunctions]');
  });
  Then(/^the title exists$/, () => {
    return client.assert.containsText('h1', 'AI Overlord');
  });
  Then(/^I see is triangle$/, () => {
    return client
      .assert.containsText('#classificationName', 'is_triangle');
  });
  Then(/^I see choose file button$/, () => {
    return client
      .waitForElementVisible('#fileuploadarea', 1000);
  });
  Then(/^neurons visible$/, () => {
    return client
      .waitForElementVisible('#neuronsLabel', 1000)
      .waitForElementVisible('#neurons', 1000);
  });
  Then(/^credits visible$/, () => {
    return client
    .waitForElementVisible('#creditsLabel', 1000)
    .waitForElementVisible('#credits', 1000);
  });
}

module.exports = steps;
