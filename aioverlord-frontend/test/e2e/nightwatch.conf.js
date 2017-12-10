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
    //server_path: "/home/hugo/PycharmProjects/AppProject/selenium-server-standalone-3.0.1.jar",
    server_path: require('selenium-server').path,
    //host: 'localhost',
    //port: 4444,
    cli_args: {
      'host': 'localhost',
      'webdriver.chrome.driver': require('chromedriver').path
    }
  },

  test_settings: {
    default: {
      selenium_port: 4444,
      selenium_host: 'chromedriver',
      silent: true,
      globals: {
        devServerURL: 'http://web:' + (process.env.PORT || config.dev.port),
        devServerHost: 'web',
        devAPIURL: 'http://flask:5000',  // should come from config
      }
    },

    chrome: {
      desiredCapabilities: {
        browserName: 'chrome',
        javascriptEnabled: true,
        acceptSslCerts: true,
//        "chromeOptions" : {
//       "args" : ["headless"],

  // }
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
};
