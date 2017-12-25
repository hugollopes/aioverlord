const axios  = require('axios');
const fs = require('fs');

const { client } = require('nightwatch-cucumber');
let creditsValue = 0;


function openApplication(client) {


  return client
      .url(client.globals.devServerURL)
      .waitForElementVisible('#app', 5000);

    }

function loginNotVisible(client){
  return client
  .expect.element('#loginPanel').to.not.be.visible.after(100);
}

function clickSignIn(client)
{
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
}

function userVisible(client, user)
{
  return client
  .waitForElementVisible('#userId', 3000)
  .pause(1000)
  .assert.containsText('#userId', user);
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

function fullfillLogin(client, user, password)
  {
  return client
  .setValue('input[id=email]', user)
  .setValue('input[id=password]', password);
}

  function setCookiesEmpty(client)
  {

    return client
    .setCookie({
      name: 'email',
      value: '',
      domain: client.globals.devServerHost,
      path: '/',
    })
    .setCookie({
      name: 'password',
      value: '',
      domain: client.globals.devServerHost,
      path: '/',
    });
  }

function visibleLogin(client)
  {
  return client
  .waitForElementVisible('#loginPanel', 1000)
  .assert.containsText('#loginPanel', 'Login');
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
  Then(/^network visible$/, () => {
    return client
      .waitForElementVisible('#networksvg', 1000)
  });
  Then(/^Network neurons visible$/, () => {
    return client
      .waitForElementVisible('#1_0', 1000)
  });
  Then(/^Network synapses visible$/, () => {
    return client
      .waitForElementVisible('#sys1_00_1', 1000)
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
    return setCookiesEmpty(client);
  });
  Given(/^user "(.*)" exists in server with password "(.*)" and role "(.*)"$/, (user, password,role) => {
    return insertUser(client, user, password, role);
  });
  Then(/^login dialog is visible$/, () => {
    return visibleLogin(client);
  });
  Then(/^I fullfill with user "(.*)" with password "(.*)"$/, (user, password) => {
    return fullfillLogin(client, user, password);
  });
  Then(/^I click Sign In$/, () => {
    return clickSignIn(client);
  });
  Then(/^user is visible with "(.*)"$/, (user) => {
    return userVisible(client, user);
  });
  Then(/^user cookies are "(.*)" and with password "(.*)"$/, (user, password) => {
    return client
    .setCookie({
      name: 'email',
      value: user,
      domain: client.globals.devServerHost,
      path: '/',
    })
    .setCookie({
      name: 'password',
      value: password,
      domain: client.globals.devServerHost,
      path: '/',
    });
  });
  Then(/^Login is not visible$/, () => {
    return loginNotVisible(client);
  });
  Given(/^I open aplication and login with user "(.*)" with password "(.*)" and role "(.*)"$/, (user, password, role) => {
      openApplication(client);
      insertUser(client, user, password, role);
      setCookiesEmpty(client);
      visibleLogin(client);
      fullfillLogin(client, user, password);
      clickSignIn(client);
      userVisible(client, user);
      loginNotVisible(client);
      return client;
  });
  Given(/^Picture "(.*)" exists in the database and a classification exists$/, (picture) => {
    axios.post(`${client.globals.devAPIURL}/create_classification`).then(() => {
      this.$log.debug('classification created successfully');
    });
    fs.readFile("features/step_definitions/steps/" + picture, (err, data)=>{
    let base64Image = new Buffer(data, 'binary').toString('base64');
    postdata = {
      file_name: picture,
      file_data: base64Image,
    }; // set image and strip initial data
    // post file base64 encoded.
    axios.post(`${client.globals.devAPIURL}/uploadpicture`, postdata)
    .then(() => {
      this.$log.debug('saved successfully');
    });
    //this.$log.debug(postdata);
    });
    return client;
  });

}



module.exports = steps;
