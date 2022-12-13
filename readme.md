### Instala ambiente virtual do python

`sudo apt-get update`

`sudo apt-get install python3-venv`

### Clona o repositório do bot

`git clone <nome_do_repositorio>`

`cd <nome_do_repositorio>`

### Cria e inicializa um ambiente virtual Python

`python3 -m venv venv`

`source venv/bin/activate`

### Instala as dependências e executa a aplicação para teste

`pip install -r requirements.txt`

`python app.py`

## Instala um webserver de produção

`pip install gunicorn`

`gunicorn -0.0.0.0:8000 app:app`

## Cria um arquivo de configurações de serviço do Linux

`sudo nano /etc/systemd/system/<nome_do_servico>.service`

> [Unit]
> Description=Telegram Bot App
> After=network.target
> [Service]
> User=ubuntu
> Group=www-data
> WorkingDirectory=/home/ubuntu/<nome_do_diretorio>
> ExecStart=/home/ubuntu/<nome_do_repositorio>/venv/bin/gunicorn -b 0.0.0.0:8000 app:app
> Restart=always
> [Install]
> WantedBy=multi-user.target

### Habilita o serviço

`sudo systemctl daemon-reload`

`sudo systemctl start <nome_do_servico>`

`sudo systemctl enable <nome_do_servico>`

## Testa se o serviço foi inicializado na porta correta

`curl localhost:8000`

### Criar um arquivo Caddyfile

`sudo apt-get install caddy`

`nano Caddyfile`
> <ip_publico_aws>.nip.io {
> reverse_proxy localhost:8000
> }

### Inicializa o serviço do Caddy

`sudo caddy run`