// const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')
const CompressionWebpackPlugin = require('compression-webpack-plugin')


module.exports = {
  assetsDir: './',
  productionSourceMap: false,
  configureWebpack: {
    plugins: [
      // new VuetifyLoaderPlugin(),
      new CompressionWebpackPlugin()
    ]
  },
}