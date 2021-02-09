module.exports = {
    chainWebpack: (config) => {
        config
            .plugin('html')
            .tap((args) => {
                args[0].title = 'Hololive Collab Network';
                return args;
            })
    },
    publicPath: process.env.NODE_ENV === 'production'
    ? '/hololive-collabs/'
    : '/'
}
