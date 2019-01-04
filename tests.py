from proxyPools import ProxyPools
from time import sleep

newPool = ProxyPools(debug=True, timeout=2,maxPoolSize=10)
newPool.start()
sleep(30)
newPool.kill()