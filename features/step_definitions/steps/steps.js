const axios  = require('axios');

const { client } = require('nightwatch-cucumber');
let creditsValue = 0;

function steps({ Given, Then, After }) {
  Given(/^I open application$/, () => {
    return client
        .url(client.globals.devServerURL)
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
    return client.assert.containsText('#title', 'AI Overlord');
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
  After(() => {
    return client
    .end();
  });
  Then(/^I see credits grow$/, () => {
    return client
      .waitForElementVisible('#credits', 1100)
      .getText('#credits', (result) => {
        creditsValue = Number(result.value);
      })
      .pause(1000)
      .getText('#credits', (result) => {
        client.assert.ok(Number(result.value) > creditsValue);
      })
    .waitForElementVisible('#credits', 1000);
  });
  Given(/^cookies are empty$/, () => {
    return client
    .setCookie({
      name: 'email',
      value: '',
      domain: 'localhost',
      path: '/',
    })
    .setCookie({
      name: 'password',
      value: '',
      domain: 'localhost',
      path: '/',
    });
  });
  Given(/^user "(.*)" exists in server with password "(.*)"$/, (user, password) => {
    console.log(`loading into DB user ${user} with password ${password}`);
    // complete this.

    const postdata = {
      email: user,
      password: password,
    };
    axios.post(client.globals.devAPIURL + '/createuser', postdata)

      //`${process.env.API_URL}/createuser`, postdata)
    .then(() => {
      console.log('saved successfully');
    });
    return client;
  });
  Then(/^login dialog is visible$/, () => {
    return client
    .waitForElementVisible('#loginPanel', 1000)
    .assert.containsText('#loginPanel', 'Login');
  });
  Then(/^I fullfill with user "(.*)" with password "(.*)"$/, (user, password) => {
    return client
    .setValue('input[id=email]', user)
    .setValue('input[id=password]', password);
  });
  Then(/^I click Sign In$/, () => {
    return client
    .waitForElementVisible('#loginButton', 1000)
    .pause(1000)
    .getAttribute('#loginButton', 'disabled', (result) => {
      if (result.value === 'true') {
        client.assert.ok(false);
      } else {
        client.assert.ok(true);
      }
    })
    .click('button[id=loginButton]');
  });
  Then(/^user is visible with "(.*)"$/, (user) => {
    return client
    .waitForElementVisible('#userId', 1000)
    .assert.containsText('#userId', user);
  });
  Then(/^user cookies are "(.*)" and with password "(.*)"$/, (user, password) => {
    return client
    .setCookie({
      name: 'email',
      value: user,
      domain: 'localhost',
      path: '/',
    })
    .setCookie({
      name: 'password',
      value: password,
      domain: 'localhost',
      path: '/',
    });
  });
  Then(/^Login is not visible$/, () => {
    return client
    .expect.element('#loginPanel').to.not.be.visible.after(100);
  });
}



module.exports = steps;
