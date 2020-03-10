from App.config import getConfiguration


def get_vue_url():
    cfg = getConfiguration()
    vueConfig = cfg.product_config.get('vue', {})
    #return 'http://localhost:8081/app.js'
    return vueConfig.get('dev_url', None)
