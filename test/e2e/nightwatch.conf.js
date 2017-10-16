require('babel-register')
var config = require('../../config')
var nightwatchCucumber = require('nightwatch-cucumber')

// Handles the runner, location of feature files and step definitions,
// and closing of nightwatch
var nightwatchCucumberConf = {
    runner: 'nightwatch',
    featureFiles: 'features',
    stepDefinitions: 'step_definitions',
    closeSession: 'afterFeature'
}

// http://nightwatchjs.org/gettingstarted#settings-file
module.exports = {
  //src_folders: ['test/e2e/specs'],
  src_folders: [nightwatchCucumber(nightwatchCucumberConf)],
  output_folder: 'test/e2e/reports',
  custom_assertions_path: ['test/e2e/custom-assertions'],

  selenium: {
    start_process: false,
    server_path: "/home/hugo/PycharmProjects/AppProject/selenium-server-standalone-3.0.1.jar",
    // server_path: require('selenium-server').path,
    host: 'localhost',
    port: 4444,
    cli_args: {
      'webdriver.chrome.driver': require('chromedriver').path
    }
  },

  test_settings: {
    default: {
      selenium_port: 4444,
      selenium_host: 'localhost',
      silent: true,
      globals: {
        devServerURL: 'http://localhost:' + (process.env.PORT || config.dev.port)
      }
    },

    chrome: {
      desiredCapabilities: {
        browserName: 'chrome',
        javascriptEnabled: true,
        acceptSslCerts: true,
      }
    },

    firefox: {
      desiredCapabilities: {
        browserName: 'firefox',
        javascriptEnabled: true,
        acceptSslCerts: true,
      }
    }
  }
}
