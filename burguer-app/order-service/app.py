from flask import Flask, redirect, url_for
from controllers.order_controller import order_bp
from dotenv import load_dotenv
import os

class OrderApp:
    def __init__(self):
        # Carrega as variáveis de ambiente
        load_dotenv()
        
        # Cria a instância da aplicação Flask
        self.app = Flask(__name__)
        self.app.secret_key = os.getenv("SECRET_KEY")
        
        # Configura as rotas
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura as rotas da aplicação"""
        # Registra o blueprint de pedidos
        self.app.register_blueprint(order_bp, url_prefix='/order')
        
        # Redireciona a rota raiz para a lista de pedidos
        @self.app.route('/')
        def index():
            return redirect(url_for('order.list_orders'))
    
    def run(self, host='127.0.0.1', port=5002, debug=True):
        """Executa a aplicação Flask"""
        self.app.run(host=host, port=port, debug=debug)
    
    def get_app(self):
        """Retorna a instância da aplicação Flask"""
        return self.app

# Criação da instância da aplicação
order_app = OrderApp()

# Código original para compatibilidade
from flask import Flask, redirect, url_for
from controllers.order_controller import order_bp
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a instância da aplicação Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Registra o blueprint de pedidos
app.register_blueprint(order_bp, url_prefix='/order')

# Redireciona a rota raiz para a lista de pedidos
@app.route('/')
def index():
    return redirect(url_for('order.list_orders'))

if __name__ == '__main__':
    # Executa a aplicação Flask
    order_app.run(port=5002, debug=True)
    # O debug=True permite recarregar automaticamente a aplicação ao fazer alterações no código
