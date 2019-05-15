const path = require('path')
const webpack = require('webpack') // eslint-disable-line import/no-extraneous-dependencies
const currentRelease = require('./build/current-release')

module.exports = {
    configureWebpack: {
        resolve: {
            alias: {
                '@': path.resolve(__dirname, './src'),
                sass: path.resolve(__dirname, './src/sass'),
                public: path.resolve(__dirname, './public'),
            },
        },
        plugins: [
            new webpack.DefinePlugin({
                CurrentRelease: JSON.stringify(currentRelease),
            }),
        ],
    },
}
