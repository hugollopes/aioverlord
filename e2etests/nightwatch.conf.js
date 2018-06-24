const seleniumServer = require('selenium-server')
const phantomjs = require('phantomjs-prebuilt')
const chromedriver = require('chromedriver')

require('nightwatch-cucumber')({
  cucumberArgs: ['--require', 'steps/steps.js', '--format', 'json:reports/cucumber.json', 'features']
})

module.exports = {
  output_folder: 'reports',
  custom_assertions_path: '',
  live_output: false,
  disable_colors: false,
  selenium: {
    start_process: false,
    server_path: seleniumServer.path,
    log_path: '',
    host: 'chromedriver',
    port: 4444
  },
  test_settings: {
    default: {
      //launch_url: 'http://localhost:8087',
      selenium_port: 4444,
      selenium_host: 'chromedriver',
      globals: {
        devServerURL: 'http://web:8080', //+ (process.env.PORT || config.dev.port),
        devServerHost: 'web',
        devAPIURL: 'http://flask:5000',  // should come from config
      },
      desiredCapabilities: {
        browserName: 'chrome',
        javascriptEnabled: true,
        acceptSslCerts: true,
      }
    },
    chrome: {
      desiredCapabilities: {
        browserName: 'chrome',
        javascriptEnabled: true,
        acceptSslCerts: true
      },
      selenium: {
        cli_args: {
          'webdriver.chrome.driver': chromedriver.path
        }
      }
    },
    firefox: {
      desiredCapabilities: {
        browserName: 'firefox',
        javascriptEnabled: true,
        acceptSslCerts: true
      }
    }
  }
}
