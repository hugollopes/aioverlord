const fs = require('fs');
const { client } = require('nightwatch-cucumber');
const axios = require('axios');
const log4js = require('log4js');

const logger = log4js.getLogger();
const NORMALWAIT = 5000;
const LARGEWAIT = 20000;
logger.level = 'info';
let creditsValue = 0;


function openApplication() {
  logger.info(`devserverURL${client.globals.devServerURL}`);
  client.url(client.globals.devServerURL);
  client.expect.element('#app').to.be.visible.before(LARGEWAIT);
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
  client.expect.element('#loginPanel').to.not.be.visible.before(NORMALWAIT);
}

function clickSignIn() {
  client.expect.element('#loginButton').to.be.visible.before(NORMALWAIT);
  client.expect.element('#loginButton').to.not.have.attribute('disabled').before(NORMALWAIT);
  client.click('#loginButton');
}

function userVisible(user) {
  client.expect.element('#userId').to.be.visible.before(NORMALWAIT);
  client.expect.element('#userId').text.to.contain(user).before(NORMALWAIT);
}

function insertUser(user, password, role, credits, neurons) {
  logger.info(`loading into DB user ${user} with password ${password} and role ${role}`);

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
  logger.info(`api user is: ${client.globals.devAPIURL}`);
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
    .setValue('#email', user)
    .setValue('#password', password);
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
  client.expect.element('#loginPanel').to.be.visible.before(NORMALWAIT);
  client.expect.element('#loginPanel').text.to.contain('Login').before(NORMALWAIT);
}

function steps({ Given, Then, After }) {
  Given(/^I open application$/, () => openApplication());
  Given(/^I click button label data$/, () => client
    .click('#Downmenubutton'));
  Given(/^I click button file upload$/, () => client
    .click('#debugFunctions'));
  Then(/^the title exists$/, () => client.assert.containsText('#title', 'AI Overlord'));
  Then(/^I see is triangle$/, () => client.expect.element('#classificationName').text.to.contain('is_triangle').before(NORMALWAIT));
  Then(/^I see choose file button$/, () => client.expect.element('#fileuploadarea').to.be.visible.before(NORMALWAIT));
  Then(/^neurons visible$/, () => {
    client.expect.element('#neuronsLabel').to.be.visible.before(NORMALWAIT);
    client.expect.element('#neurons').to.be.visible.before(NORMALWAIT);
  });
  Then(/^network visible$/, () => client.expect.element('#networksvg').to.be.visible.before(NORMALWAIT));
  Then(/^network neurons visible$/, () => client.expect.element('#neuron1_0').to.be.visible.before(NORMALWAIT));
  Then(/^network synapses visible$/, () => client.expect.element('#synneuron1_0neuron0_1').to.be.visible.before(NORMALWAIT));
  Then(/^credits visible$/, () => {
    client.expect.element('#creditsLabel').to.be.visible.before(NORMALWAIT);
    client.expect.element('#credits').to.be.visible.before(NORMALWAIT);
  });
  Then(/^I see credits grow$/, () => {
    client.expect.element('#credits').to.be.visible.before(NORMALWAIT);
    client.getText('#credits', (result) => {
      creditsValue = Number(result.value);
    });
    client.pause(1000);
    client.getText('#credits', (result) => {
      client.assert.ok(Number(result.value) > creditsValue);
    });
  });
  Given(/^cookies are empty$/, () => setCookiesEmpty());
  Given(/^user "(.*)" exists in server with password "(.*)" and role "(.*)"$/, (user, password, role) => insertUser(user, password, role, 0, 1));
  Then(/^login dialog is visible$/, () => visibleLogin());
  Then(/^topology is visible$/, () => client.expect.element('#topologydiv').to.be.visible.before(NORMALWAIT));
  Then(/^buy "(.*)" topology is visible$/, (topology) => {
    client.expect.element(`#buyTopology${getTopologyId(topology)}`).to.be.visible.before(NORMALWAIT);
  });
  Then(/^click buy topology "(.*)"$/, (topology) => {
    client.expect.element(`#buyTopology${getTopologyId(topology)}`).to.be.visible.before(NORMALWAIT);
    client.click(`#buyTopology${getTopologyId(topology)}`);
  });
  Then(/^user buys agent$/, () => {
    client.expect.element('#buyAgent2').to.be.visible.before(NORMALWAIT);
    client.click('#buyAgent2');
    client.expect.element('#agentsOwned2').to.be.visible.before(NORMALWAIT);
  });
  Then(/^user assigns agent$/, () => {
    client.expect.element('#assignAgent2t2').to.be.visible.before(NORMALWAIT);
    client.click('#assignAgent2t2');
    client.expect.element('#agentsOwned2').text.to.contain('strong agent with status assigned').before(NORMALWAIT);
  });
  Then(/^then topology "(.*)" belongs to user$/, topology => client.expect.element(`#topologyOwned${getTopologyId(topology)}`).to.be.visible.before(NORMALWAIT));
  Then(/^buy "(.*)" topology is disabled$/, topology => client
    .expect.element(`#buyTopology${getTopologyId(topology)}`).to.have.attribute('disabled').before(1000));
  Then(/^buy "(.*)" topology is enabled$/, topology => client
    .expect.element(`#buyTopology${getTopologyId(topology)}`).to.not.have.attribute('disabled').before(3000));
  Then(/^buy neurons is visible$/, () => client.expect.element('#buyNeuronButton').to.be.visible.before(NORMALWAIT));
  Then(/^buy neurons is disabled$/, () => client
    .expect.element('#buyNeuronButton').to.have.attribute('disabled').before(NORMALWAIT));
  Then(/^buy neurons is enabled$/, () => client
    .expect.element('#buyNeuronButton').to.not.have.attribute('disabled').before(NORMALWAIT));
  Then(/^network button is visible$/, () => client.expect.element('#showNetworkButton').to.be.visible.before(NORMALWAIT));
  Then(/^click buy neurons$/, () => {
    client.expect.element('#buyNeuronButton').to.be.visible.before(NORMALWAIT);
    client.click('#buyNeuronButton');
  });
  Then(/^I fullfill with user "(.*)" with password "(.*)"$/, (user, password) => fullfillLogin(user, password));
  Then(/^user "(.*)" has "(.*)" neurons and "(.*)" credits$/, (user, neurons, credits) => insertUser(user, '', 'user', Number(credits), Number(neurons)));
  Then(/^I click Sign In$/, () => clickSignIn());
  Then(/^I click topology$/, () => {
    client.expect.element('#topologyButton').to.be.visible.before(NORMALWAIT);
    client.click('#topologyButton');
  });
  Then(/user accesses world$/, () => {
    client.expect.element('#ShowWorldButton').to.be.visible.before(NORMALWAIT);
    client.click('#ShowWorldButton');
    client.expect.element('#worlddiv').to.be.visible.before(NORMALWAIT);
  });
  Then(/^I click network button$/, () => {
    client.expect.element('#showNetworkButton').to.be.visible.before(NORMALWAIT);
    client.click('#showNetworkButton');
  });
  Then(/^user is visible with "(.*)"$/, user => userVisible(user));
  Then(/^number of user neurons is "(.*)"$/, (neurons) => {
    client.expect.element('#neurons').to.be.visible.before(NORMALWAIT);
    client.expect.element('#neurons').text.to.equal(neurons).before(NORMALWAIT);
  });
  Then(/^after "(.*)" seconds credits are more than "(.*)"$/, (seconds, credits) => {
    client.expect.element('#credits').to.be.visible.before(NORMALWAIT);
    client.pause(seconds * 1000);
    client.getText('#credits', (result) => {
      client.assert.ok(Number(result.value) >= Number(credits));
    });
  });
  Then(/^credits are less than "(.*)"$/, (credits) => {
    client.expect.element('#credits').to.be.visible.before(NORMALWAIT);
    client.pause(1000);
    client.getText('#credits', (result) => {
      client.assert.ok(Number(result.value) < Number(credits));
    });
  });

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
  Given(/^I open application and login with user "(.*)" with password "(.*)" and role "(.*)"$/, (user, password, role) => {
    openApplication();
    insertUser(user, password, role, 0, 1);
    setCookiesEmpty();
    visibleLogin();
    fullfillLogin(user, password);
    clickSignIn();
    userVisible(user);
    loginNotVisible();
  });
  Given(/^Picture "(.*)" exists in the database and a classification exists$/, (picture) => {
    axios.post(`${client.globals.devAPIURL}/create_classification`).then(() => {
      this.$log.debug('classification created successfully');
    });

    fs.readFile(`/app/testdata/${picture}`, (err, data) => {
      if (err) {
        throw err;
      }
      const base64Image = Buffer.from(data, 'binary').toString('base64');
      logger.debug(`pic. ${base64Image}`);
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
//  After(() => client
  //  .end());
}


module.exports = steps;
