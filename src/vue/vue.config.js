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
                CustomEnv: {
                    API_URL: JSON.stringify(process.env.API_URL),
                    SENTRY_DSN: JSON.stringify(process.env.SENTRY_DSN),
                    SENTRY_ORGANIZATION_SLUG: JSON.stringify(process.env.SENTRY_ORGANIZATION_SLUG),
                    SENTRY_PROJECT_SLUG: JSON.stringify(process.env.SENTRY_PROJECT_SLUG),
                },
            }),
            new webpack.ProvidePlugin({
                introJs: ['intro.js'],
            }),
        ],
    },
}
