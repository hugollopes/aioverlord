// For authoring Nightwatch tests, see
// http://nightwatchjs.org/guide#usage
/*
module.exports = {
  'default e2e tests': function test(browser) {
    // automatically uses dev Server port from /config.index.js
    // default: http://localhost:8080
    // see nightwatch.conf.js
    const devServer = browser.globals.devServerURL;

    browser
      .url(devServer)
      .waitForElementVisible('#app', 5000)
      .assert.containsText('h1', 'AI Overlord')
      .assert.containsText('#Downmenubutton', 'label data')
      .click('button[id=Downmenubutton]')
      .pause(4000)
      .assert.containsText('#classificationName', 'is_triangle')
      .end();
  },
}; */
