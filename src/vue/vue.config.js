const path = require('path')
const webpack = require('webpack') // eslint-disable-line import/no-extraneous-dependencies
const currentRelease = require('./build/current-release')
const CKEditorWebpackPlugin = require('@ckeditor/ckeditor5-dev-webpack-plugin')
const { styles } = require('@ckeditor/ckeditor5-dev-utils')

module.exports = {
    /* The source of CKEditor is encapsulated in ES6 modules. By default, the code
    from the node_modules directory is not transpiled, so you must explicitly tell
    the CLI tools to transpile JavaScript files in all ckeditor5-* modules. */
    transpileDependencies: [
        /ckeditor5-[^/\\]+[/\\]src[/\\].+\.js$/,
    ],

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
            new CKEditorWebpackPlugin({
                language: 'en'
            }),
        ],
    },

    /* Vue CLI would normally use its own loader to load .svg and .css files, however:
    	1. The icons used by CKEditor must be loaded using raw-loader,
    	2. The CSS used by CKEditor must be transpiled using PostCSS to load properly. */
    chainWebpack: config => {
        /* (1.) To handle editor icons, get the default rule for *.svg files first: */
        const svgRule = config.module.rule( 'svg' )

        /* Exclude ckeditor directory from node_modules. */
        svgRule.exclude.add(path.join( __dirname, 'node_modules', '@ckeditor'))

        /* Add an entry for *.svg files belonging to CKEditor. */
        config.module
            .rule('cke-svg')
            .test(/ckeditor5-[^/\\]+[/\\]theme[/\\]icons[/\\][^/\\]+\.svg$/)
            .use('raw-loader')
            .loader('raw-loader')

        /* (2.) Transpile the .css files imported by the editor using PostCSS. */
        config.module
            .rule('cke-css')
            .test(/ckeditor5-[^/\\]+[/\\].+\.css$/)
            .use('postcss-loader')
            .loader('postcss-loader')
            .tap(() => {
                return styles.getPostCssConfig({
                    themeImporter: {
                        themePath: require.resolve('@ckeditor/ckeditor5-theme-lark'),
                    },
                    minify: true,
                })
            })
    }
}
