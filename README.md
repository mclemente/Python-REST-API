# Python-REST-API

Uma API para gerenciar lista de IPs de redes Tor.

## Geral

### Blacklist
`GET` irá retornar a lista de endereços IP na blacklist.

`POST` irá obter endereços IPs (https://www.dan.me.uk/tornodes e https://onionoo.torproject.org/summary?limit=5000) e adicioná-los ao banco de dados.

### Whitelist
`GET` retorna os endereços IP que estão no banco de dados.

### Whitelist/IP
`GET` retorna se o endereço IP informado está no banco de dados.

`POST` adiciona o endereço IP informado ao banco de dados.

### Filtro
`GET` retorna todos os IPs da blacklist que não estão na whitelist. Equivalente a `SELECT * FROM ips, whitelist WHERE ips.ip != whitelist.ip`.

## Instalação
`pip install flask, flask_restful, requests, flask_sqlalchemy`
