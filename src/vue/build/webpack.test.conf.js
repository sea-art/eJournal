'use strict'
// This is the webpack config used for unit tests.

const path = require('path')
const utils = require('./utils')
const webpack = require('webpack')
const merge = require('webpack-merge')
const baseWebpackConfig = require('./webpack.base.conf')

function resolve (dir) {
  return path.join(__dirname, '..', dir)
}

const webpackConfig = merge(baseWebpackConfig, {
  // use inline sourcemap for karma-sourcemap-loader
  // use babel-loader to also recompile axios to not use ES6,
  // as ES6 is not present in PhantomJS.
    module: {
        rules: [
        	...(utils.styleLoaders()),
            {
                test: /\.js$/,
                loader: 'babel-loader',
                include: [resolve('src'),
        	      resolve('test'),
        	      resolve('node_modules/webpack-dev-server/client'),
        	      resolve('node_modules/axios')]
            }
        ]
    },
    devtool: '#inline-source-map',
    resolveLoader: {
        alias: {
          // necessary to to make lang="scss" work in test when using vue-loader's ?inject option
          // see discussion at https://github.com/vuejs/vue-loader/issues/724
          'scss-loader': 'sass-loader'
        }
    },
    plugins: [
        new webpack.DefinePlugin({
          'process.env': require('../config/test.env')
        })
    ]
})

// no need for app entry during tests
delete webpackConfig.entry

module.exports = webpackConfig
