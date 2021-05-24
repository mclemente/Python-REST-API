import sqlite3

conn = sqlite3.connect('banco.db')
cur = conn.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS whitelist (ip_id text PRIMARY_KEY, ip text, whitelisted bit)"

cur.execute(cria_tabela)

def cria_whitelist(ip):
    whitelist = "INSERT INTO whitelist VALUES (" + 0

conn.commit()
conn.close()