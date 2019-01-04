# Python Proxy Scraper

A proxy scraping class that maintains a pool of usable proxies collected from 4 sources.

## Required Libraries

 - beautifulsoup4
 - requests
 - termcolor

## Usage

#### Initialize a Pool
```python
pool = ProxyPools()
pool.start()
```

Paramaters when initilizing a new pool

| Name        | Type      | Usage		  |
| ------------|:--------: | ------------: |
| intervalTime| int       |  Time between scraping for proxies in seconds |
| maxPoolSize | int       |  Maximun number of given proxies in pool at any given time |
| timeout     | int/double|  Max timeout when checking if proxy is valid in seconds
| debug       | bool      |  Print debug info |

Example
```python
pool = ProxyPools(timeout=5,maxPoolSize=10 )
# Initilize a pool with timeout of 5 seconds 
# and maximum of 10 proxies in pool
```

#### Stopping a Pool
```python
pool.kill()
```

#### Useful Functions
```python
pool.getOne() #get one proxy from pool which has the lowest response time
pool.getList() #get entire list of proxies
pool.getSize() #get size of pool
```