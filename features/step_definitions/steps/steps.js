const axios  = require('axios');

const { client } = require('nightwatch-cucumber');
let creditsValue = 0;


function openApplication(client) {
  return client
      .url(client.globals.devServerURL)
      .waitForElementVisible('#app', 5000);
    }

function insertUser(client, user, password,role)
  {
    console.log(`loading into DB user ${user} with password ${password} and role ${role}`);

    const postdata = {
      username: user,
      password: password,
      role: role,
    };
    const updatedata = {
      username: user,
      password: password,
      role: role,
      credits: 0,
      neurons: 1,
    };
    axios.post(client.globals.devAPIURL + '/createUser', postdata)
    .then((response) => {
      console.log('saved successfully');
    })
    .catch((error) => {
      console.log("not saved with error code: " + error.response.data.error);
      if (error.response.data.error === 'userAlreadyExists')
      axios.post(client.globals.devAPIURL + '/updateUserStatus', updatedata)
      .then((response) => {
        console.log('updated successfully');
      })
    });
    return client;
  }

  function setCookiesEmpty(client)
  {
      return client;
  }

function steps({ Given, Then, After }) {
  Given(/^I open application$/, () => {
    return openApplication(client);
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
  Given(/^user "(.*)" exists in server with password "(.*)" and role "(.*)"$/, (user, password,role) => {
    return insertUser(client, user, password, role);
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
    .waitForElementVisible('#userId', 3000)
    .pause(1000)
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
  Given(/^I open aplication and login with user "(.*)" with password "(.*)" and role "(.*)"$/, (user, password, role) => {
      openApplication(client);
      insertUser(client, user, password, role);
      return client;
  });
}



module.exports = steps;
