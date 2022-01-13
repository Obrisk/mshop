const Application = require('thinkjs');

const instance = new Application({
  ROOT_PATH: __dirname,
  proxy: true, // use proxy
  env: 'production'
});

instance.run();

export default {
  proxy_on: true,
  resource_on: false,
  cluster_on: true
}

