return mysql.connector.connect(
    host=cfg["host"],
    user=cfg["user"],
    password=cfg["password"],
    database=cfg["database"],
    port=int(cfg.get("port", 3306)),
    autocommit=True,
    connection_timeout=6,  # evita que quede colgado
)

