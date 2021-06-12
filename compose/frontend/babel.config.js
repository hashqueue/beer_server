const IS_PROD = process.env.NODE_ENV === 'production'

const plugins = []
if (IS_PROD) {
  plugins.push('transform-remove-console')
}

module.exports = {
  presets: ['@vue/cli-plugin-babel/preset'],
  plugins
}
