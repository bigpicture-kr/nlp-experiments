c.ServerApp.allow_root = True
c.ServerApp.allow_origin = '*'
c.ServerApp.root_dir = '/nlp'
c.ServerApp.password_required = True
c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$BaLOJQXLSsOjQ9Qu8LxBwA$Jj5/AH6T0uQbMd4Nr18chbQU9fL7lZiUCFlEP4d00Rg'
c.ServerApp.open_browser = False
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 443

# SSL
c.ServerApp.certfile = '/root/.ssl/cert1.pem'
c.ServerApp.keyfile = '/root/.ssl/privkey1.pem'
