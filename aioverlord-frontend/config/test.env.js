'use strict'
const merge = require('webpack-merge')
const devEnv = require('./dev.env')
// THIS IS USELESS!!!!! real values are in aioverlord-frontend/build/webpack.e2e.conf.js
module.exports = merge(devEnv, {
  NODE_ENV: '"testing"',
  API_URL: '"http://flask:5000"'
})
