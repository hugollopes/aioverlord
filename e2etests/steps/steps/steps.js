const fs = require('fs');
const { client } = require('nightwatch-cucumber');
const axios = require('axios');

let creditsValue = 0;


function openApplication() {
  console.info(`devserverURL${client.globals.devServerURL}`);
  client
    .url(client.globals.devServerURL)
    .waitForElementVisible('#app', 5000);
}

function getTopologyId(topology) {
  if (topology === '2 hidden layers') {
    return '1';
  } if (topology === '3 hidden layers') {
    return '2';
  }
  return '';
}

function loginNotVisible() {
  client
    .expect.element('#loginPanel').to.not.be.visible.after(100);
}

function clickSignIn() {
  client
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

function userVisible(user) {
  client
    .waitForElementVisible('#userId', 3000)
    .pause(1000)
    .assert.containsText('#userId', user);
}

function insertUser(user, password, role, credits, neurons) {
  console.info(`loading into DB user ${user} with password ${password} and role ${role}`);

  const postdata = {
    username: user,
    password,
    role,
  };
  const updatedata = {
    username: user,
    password,
    role,
    credits,
    neurons,
  };
  console.info(`api user is: ${client.globals.devAPIURL}`);
  axios.post(`${client.globals.devAPIURL}/createUser`, postdata)
    .then(() => {
      // this.$log.debug(`saved successfully${String(response)}`);
    })
    .catch((error) => {
      // this.$log.debug(`not saved with error code: ${error.response.data.error}`);
      if (error.response.data.error === 'userAlreadyExists') {
        axios.post(`${client.globals.devAPIURL}/updateUserStatus`, updatedata)
          .then(() => {
            //  this.$log.debug(`updated successfully${String(response)}`);
          });
      }
    });
}

function fullfillLogin(user, password) {
  client
    .setValue('input[id=email]', user)
    .setValue('input[id=password]', password);
}

function setCookiesEmpty() {
  client
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

function visibleLogin() {
  client
    .waitForElementVisible('#loginPanel', 1000)
    .assert.containsText('#loginPanel', 'Login');
}

function steps({ Given, Then, After }) {
  Given(/^I open application$/, () => openApplication());
  Given(/^I click button label data$/, () => client
    .click('button[id=Downmenubutton]')
    .pause(4000));
  Given(/^I click button file upload$/, () => client
    .click('button[id=debugFunctions]'));
  Then(/^the title exists$/, () => client.assert.containsText('#title', 'AI Overlord'));
  Then(/^I see is triangle$/, () => client
    .assert.containsText('#classificationName', 'is_triangle'));
  Then(/^I see choose file button$/, () => client
    .waitForElementVisible('#fileuploadarea', 1000));
  Then(/^neurons visible$/, () => client
    .waitForElementVisible('#neuronsLabel', 1000)
    .waitForElementVisible('#neurons', 1000));
  Then(/^network visible$/, () => client
    .waitForElementVisible('#networksvg', 1000));
  Then(/^network neurons visible$/, () => client
    .waitForElementVisible('#neuron1_0', 1000));
  Then(/^network synapses visible$/, () => client
    .waitForElementVisible('#synneuron1_0neuron0_1', 1000));
  Then(/^credits visible$/, () => client
    .waitForElementVisible('#creditsLabel', 1000)
    .waitForElementVisible('#credits', 1000));
  After(() => client
    .end());
  Then(/^I see credits grow$/, () => client
    .waitForElementVisible('#credits', 1100)
    .getText('#credits', (result) => {
      creditsValue = Number(result.value);
    })
    .pause(1000)
    .getText('#credits', (result) => {
      client.assert.ok(Number(result.value) > creditsValue);
    })
    .waitForElementVisible('#credits', 1000));
  Given(/^cookies are empty$/, () => setCookiesEmpty());
  Given(/^user "(.*)" exists in server with password "(.*)" and role "(.*)"$/, (user, password, role) => insertUser(user, password, role, 0, 1));
  Then(/^login dialog is visible$/, () => visibleLogin());
  Then(/^topology is visible$/, () => client
    .waitForElementVisible('#topologydiv', 1000));
  Then(/^buy "(.*)" topology is visible$/, (topology) => {
    client
      .waitForElementVisible(`#buyTopology${getTopologyId(topology)}`, 1000);
  });
  Then(/^click buy topology "(.*)"$/, topology => client
    .waitForElementVisible(`#buyTopology${getTopologyId(topology)}`, 1000)
    .click(`button[id=buyTopology${getTopologyId(topology)}]`));
  Then(/^then topology "(.*)" belongs to user$/, topology => client
    .waitForElementVisible(`#topologyOwned${getTopologyId(topology)}`, 1000));
  Then(/^buy "(.*)" topology is disabled$/, topology => client
    .expect.element(`#buyTopology${getTopologyId(topology)}`).to.have.attribute('disabled').before(1000));
  Then(/^buy "(.*)" topology is enabled$/, topology => client
    .expect.element(`#buyTopology${getTopologyId(topology)}`).to.not.have.attribute('disabled').before(3000));
  Then(/^buy neurons is visible$/, () => client
    .waitForElementVisible('#buyNeuronButton', 1000));
  Then(/^buy neurons is disabled$/, () => client
    .expect.element('#buyNeuronButton').to.have.attribute('disabled').before(1000));
  Then(/^buy neurons is enabled$/, () => client
    .expect.element('#buyNeuronButton').to.not.have.attribute('disabled').before(3000));
  Then(/^network button is visible$/, () => client
    .waitForElementVisible('#showNetworkButton', 1000));
  Then(/^click buy neurons$/, () => client
    .waitForElementVisible('#buyNeuronButton', 1000)
    .click('button[id=buyNeuronButton]'));
  Then(/^I fullfill with user "(.*)" with password "(.*)"$/, (user, password) => fullfillLogin(user, password));
  Then(/^user "(.*)" has "(.*)" neurons and "(.*)" credits$/, (user, neurons, credits) => insertUser(user, '', 'user', Number(credits), Number(neurons)));
  Then(/^I click Sign In$/, () => clickSignIn());
  Then(/^I click topology$/, () => client
    .waitForElementVisible('#topologyButton', 1000)
    .click('button[id=topologyButton]'));
  Then(/^I click network button$/, () => client
    .waitForElementVisible('#showNetworkButton', 1000)
    .click('button[id=showNetworkButton]'));
  Then(/^user is visible with "(.*)"$/, user => userVisible(user));
  Then(/^number of user neurons is "(.*)"$/, neurons => client
    .waitForElementVisible('#neurons', 1000)
    .pause(1000)
    .getText('#neurons', (result) => {
      client.assert.ok(Number(result.value) === Number(neurons));
    }));
  Then(/^after "(.*)" seconds credits are more than "(.*)"$/, (seconds, credits) => client
    .waitForElementVisible('#credits', 1000)
    .pause(seconds * 1000)
    .getText('#credits', (result) => {
      client.assert.ok(Number(result.value) >= Number(credits));
    }));
  Then(/^credits are less than "(.*)"$/, credits => client
    .waitForElementVisible('#credits', 1000)
    .pause(1000)
    .getText('#credits', (result) => {
      client.assert.ok(Number(result.value) < Number(credits));
    }));

  Then(/^user name not visible$/, () => client
    .expect.element('#userId').to.not.be.visible.after(100));
  Then(/^buttons not visible$/, () => client
    .expect.element('#buttonsDiv').to.not.be.visible.after(100));
  Then(/^user cookies are "(.*)" and with password "(.*)"$/, (user, password) => client
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
    }));
  Then(/^Login is not visible$/, () => loginNotVisible());
  Given(/^I open aplication and login with user "(.*)" with password "(.*)" and role "(.*)"$/, (user, password, role) => {
    openApplication();
    insertUser(user, password, role, 0, 1);
    setCookiesEmpty();
    visibleLogin();
    fullfillLogin(user, password);
    clickSignIn();
    userVisible(user);
    loginNotVisible();
    return client;
  });


  // troubleshoot steps
  Given(/^I open Google`s search page$/, () => client
    .url('http://google.com'));

  Given(/^I open DuckDuckGo search page$/, () => client
    .url('https://duckduckgo.com/'));

  Then(/^the title is "(.*?)"$/, text => client.assert.title(text));

  Then(/^the Google search form exists$/, () => client.assert.visible('input[name="q"]'));

  Then(/^the DuckDuckGo search form exists$/, () => client.assert.visible('input[name="q"]'));
  // end troubleshoot steps


  Given(/^Picture "(.*)" exists in the database and a classification exists$/, (picture) => {
    axios.post(`${client.globals.devAPIURL}/create_classification`).then(() => {
      this.$log.debug('classification created successfully');
    });

    fs.readFile(`/app/testdata/${picture}`, (err, data) => {
      if (err) {
        throw err;
      }
      const base64Image =  new Buffer(data, 'binary').toString('base64');
      console.info(`pic. ${base64Image}`);
      const postdata = {
        file_name: picture,
        file_data: base64Image,
      }; // set image and strip initial data
      // post file base64 encoded.
      axios.post(`${client.globals.devAPIURL}/uploadpicture`, postdata)
        .then(() => {
          this.$log.debug('saved successfully');
        });
    });
    return client;
  });
}


module.exports = steps;