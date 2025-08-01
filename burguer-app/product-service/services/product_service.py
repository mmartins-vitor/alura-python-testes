<<<<<<< HEAD
from config.database import get_db
from models.product_model import serialize_product
from bson import ObjectId

db = get_db()
products_col = db["products"]

def create_product(name, description, category, price, ingredients, available=True):
    """Cria um novo produto"""
    try:
        price = float(price)
    except (ValueError, TypeError):
        return {"error": "Preço deve ser um número válido"}, 400
    
    product = {
        "name": name,
        "description": description,
        "category": category,
        "price": price,
        "available": available,
        "ingredients": ingredients
    }
    result = products_col.insert_one(product)
    return {"message": "Produto criado com sucesso", "id": str(result.inserted_id)}, 201

def get_all_products():
    """Retorna todos os produtos"""
    products = list(products_col.find().sort([("category", 1), ("name", 1)]))
    return [serialize_product(product) for product in products]

def get_available_products():
    """Retorna apenas produtos disponíveis"""
    products = list(products_col.find({"available": True}).sort([("category", 1), ("name", 1)]))
    return [serialize_product(product) for product in products]

def get_products_by_category(category):
    """Retorna produtos por categoria"""
    products = list(products_col.find({"category": category, "available": True}).sort("name", 1))
    return [serialize_product(product) for product in products]

def get_product_by_id(product_id):
    """Retorna um produto pelo ID"""
    try:
        product = products_col.find_one({"_id": ObjectId(product_id)})
        if product:
            return serialize_product(product)
        return None
    except:
        return None

def update_product(product_id, name, description, category, price, ingredients, available):
    """Atualiza um produto"""
    try:
        price = float(price)
        result = products_col.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {
                "name": name,
                "description": description,
                "category": category,
                "price": price,
                "available": available,
                "ingredients": ingredients
            }}
        )
        return result.modified_count > 0
    except:
        return False

def delete_product(product_id):
    """Deleta um produto"""
    try:
        result = products_col.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
    except:
        return False

def get_categories():
    """Retorna todas as categorias únicas"""
    categories = products_col.distinct("category")
    return sorted(categories)

def initialize_products():
    """Inicializa produtos padrão se não existirem"""
    if products_col.count_documents({}) == 0:
        default_products = [
            # Hambúrgueres
            {
                "name": "Hambúrguer Simples",
                "description": "Pão, carne e queijo",
                "category": "Hambúrgueres",
                "price": 15.90,
                "available": True,
                "ingredients": ["pão", "carne", "queijo"]
            },
            {
                "name": "Hambúrguer Salada",
                "description": "Pão, carne, queijo, alface e tomate",
                "category": "Hambúrgueres",
                "price": 18.90,
                "available": True,
                "ingredients": ["pão", "carne", "queijo", "alface", "tomate"]
            },
            {
                "name": "Hambúrguer Cheddar",
                "description": "Pão, carne, cheddar, alface e tomate",
                "category": "Hambúrgueres",
                "price": 21.90,
                "available": True,
                "ingredients": ["pão", "carne", "cheddar", "alface", "tomate"]
            },
            {
                "name": "Hambúrguer Bacon",
                "description": "Pão, carne, queijo, bacon, alface e tomate",
                "category": "Hambúrgueres",
                "price": 23.90,
                "available": True,
                "ingredients": ["pão", "carne", "queijo", "bacon", "alface", "tomate"]
            },
            {
                "name": "Hambúrguer Cheddar Bacon",
                "description": "Pão, carne, cheddar, bacon, alface e tomate",
                "category": "Hambúrgueres",
                "price": 26.90,
                "available": True,
                "ingredients": ["pão", "carne", "cheddar", "bacon", "alface", "tomate"]
            },
            {
                "name": "Hambúrguer Costela",
                "description": "Hambúrguer de costela, pão, queijo, alface e tomate",
                "category": "Hambúrgueres",
                "price": 28.90,
                "available": True,
                "ingredients": ["pão", "hambúrguer de costela", "queijo", "alface", "tomate"]
            },
            {
                "name": "Hambúrguer Frango",
                "description": "Hambúrguer de frango, pão, queijo, alface e tomate",
                "category": "Hambúrgueres",
                "price": 19.90,
                "available": True,
                "ingredients": ["pão", "hambúrguer de frango", "queijo", "alface", "tomate"]
            },
            {
                "name": "Duplo Hambúrguer",
                "description": "Pão, queijo, duas carnes, alface e tomate",
                "category": "Hambúrgueres",
                "price": 32.90,
                "available": True,
                "ingredients": ["pão", "queijo", "duas carnes", "alface", "tomate"]
            },
            # Bebidas
            {
                "name": "Coca-Cola 350ml",
                "description": "Refrigerante de cola gelado",
                "category": "Refrigerantes e Sucos",
                "price": 5.90,
                "available": True,
                "ingredients": ["água", "açúcar", "extrato de cola"]
            },
            {
                "name": "Guaraná Antarctica 350ml",
                "description": "Refrigerante de guaraná gelado",
                "category": "Refrigerantes e Sucos",
                "price": 5.90,
                "available": True,
                "ingredients": ["água", "açúcar", "extrato de guaraná"]
            },
            {
                "name": "Fanta Laranja 350ml",
                "description": "Refrigerante sabor laranja gelado",
                "category": "Refrigerantes e Sucos",
                "price": 5.90,
                "available": True,
                "ingredients": ["água", "açúcar", "sabor laranja"]
            },
            {
                "name": "Suco de Laranja Natural",
                "description": "Suco natural de laranja",
                "category": "Refrigerantes e Sucos",
                "price": 8.90,
                "available": True,
                "ingredients": ["laranja natural"]
            },
            {
                "name": "Água Mineral 500ml",
                "description": "Água mineral sem gás",
                "category": "Refrigerantes e Sucos",
                "price": 3.90,
                "available": True,
                "ingredients": ["água mineral"]
            }
        ]
        
        products_col.insert_many(default_products)
        print("✅ Produtos iniciais criados com sucesso!")
=======
from config.database import DatabaseConfig
from models.product_model import ProductModel
from bson import ObjectId

class ProductService:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.db = self.db_config.get_db()
        self.products_col = self.db["products"]
        self.product_model = ProductModel()
    
    def create_product(self, name, description, category, price, ingredients, available=True):
        """Cria um novo produto"""
        try:
            price = float(price)
        except (ValueError, TypeError):
            return {"error": "Preço deve ser um número válido"}, 400
        
        # Cria instância do modelo
        product = ProductModel(
            name=name, 
            description=description, 
            category=category, 
            price=price, 
            available=available, 
            ingredients=ingredients
        )
        
        # Valida os dados
        is_valid, message = product.validate()
        if not is_valid:
            return {"error": message}, 400
        
        # Salva no banco
        product_data = product.to_dict()
        result = self.products_col.insert_one(product_data)
        return {"message": "Produto criado com sucesso", "id": str(result.inserted_id)}, 201
    
    def get_all_products(self):
        """Retorna todos os produtos"""
        products = list(self.products_col.find().sort([("category", 1), ("name", 1)]))
        return [self.product_model.serialize(product) for product in products]
    
    def get_available_products(self):
        """Retorna apenas produtos disponíveis"""
        products = list(self.products_col.find({"available": True}).sort([("category", 1), ("name", 1)]))
        return [self.product_model.serialize(product) for product in products]
    
    def get_products_by_category(self, category):
        """Retorna produtos por categoria"""
        products = list(self.products_col.find({"category": category, "available": True}).sort("name", 1))
        return [self.product_model.serialize(product) for product in products]
    
    def get_product_by_id(self, product_id):
        """Retorna um produto pelo ID"""
        try:
            product = self.products_col.find_one({"_id": ObjectId(product_id)})
            if product:
                return self.product_model.serialize(product)
            return None
        except:
            return None
    
    def update_product(self, product_id, name, description, category, price, ingredients, available):
        """Atualiza um produto"""
        try:
            price = float(price)
        except (ValueError, TypeError):
            return {"error": "Preço deve ser um número válido"}, 400
        
        # Cria instância do modelo para validação
        product = ProductModel(
            name=name, 
            description=description, 
            category=category, 
            price=price, 
            available=available, 
            ingredients=ingredients
        )
        
        # Valida os dados
        is_valid, message = product.validate()
        if not is_valid:
            return {"error": message}, 400
        
        # Atualiza no banco
        result = self.products_col.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product.to_dict()}
        )
        
        if result.matched_count == 0:
            return {"error": "Produto não encontrado"}, 404
        
        return {"message": "Produto atualizado com sucesso"}, 200
    
    def delete_product(self, product_id):
        """Deleta um produto"""
        try:
            result = self.products_col.delete_one({"_id": ObjectId(product_id)})
            if result.deleted_count == 0:
                return {"error": "Produto não encontrado"}, 404
            return {"message": "Produto deletado com sucesso"}, 200
        except:
            return {"error": "ID do produto inválido"}, 400
    
    def get_categories(self):
        """Retorna todas as categorias únicas"""
        categories = self.products_col.distinct("category")
        return sorted(categories)
    
    def initialize_products(self):
        """Inicializa produtos padrão se não existirem"""
        if self.products_col.count_documents({}) == 0:
            default_products = [
                # Hambúrgueres
                {
                    "name": "Hambúrguer Simples",
                    "description": "Pão, carne e queijo",
                    "category": "Hambúrgueres",
                    "price": 15.90,
                    "available": True,
                    "ingredients": ["pão", "carne", "queijo"]
                },
                {
                    "name": "Hambúrguer Salada",
                    "description": "Pão, carne, queijo, alface e tomate",
                    "category": "Hambúrgueres",
                    "price": 18.90,
                    "available": True,
                    "ingredients": ["pão", "carne", "queijo", "alface", "tomate"]
                },
                {
                    "name": "Hambúrguer Cheddar",
                    "description": "Pão, carne, cheddar, alface e tomate",
                    "category": "Hambúrgueres",
                    "price": 21.90,
                    "available": True,
                    "ingredients": ["pão", "carne", "cheddar", "alface", "tomate"]
                },
                {
                    "name": "Hambúrguer Bacon",
                    "description": "Pão, carne, queijo, bacon, alface e tomate",
                    "category": "Hambúrgueres",
                    "price": 23.90,
                    "available": True,
                    "ingredients": ["pão", "carne", "queijo", "bacon", "alface", "tomate"]
                },
                {
                    "name": "Hambúrguer Cheddar Bacon",
                    "description": "Pão, carne, cheddar, bacon, alface e tomate",
                    "category": "Hambúrgueres",
                    "price": 26.90,
                    "available": True,
                    "ingredients": ["pão", "carne", "cheddar", "bacon", "alface", "tomate"]
                },
                # Bebidas
                {
                    "name": "Coca-Cola 350ml",
                    "description": "Refrigerante de cola gelado",
                    "category": "Refrigerantes e Sucos",
                    "price": 5.90,
                    "available": True,
                    "ingredients": ["água", "açúcar", "extrato de cola"]
                },
                {
                    "name": "Guaraná Antarctica 350ml",
                    "description": "Refrigerante de guaraná gelado",
                    "category": "Refrigerantes e Sucos",
                    "price": 5.90,
                    "available": True,
                    "ingredients": ["água", "açúcar", "extrato de guaraná"]
                },
                {
                    "name": "Água Mineral 500ml",
                    "description": "Água mineral sem gás",
                    "category": "Refrigerantes e Sucos",
                    "price": 3.90,
                    "available": True,
                    "ingredients": ["água mineral"]
                }
            ]
            
            self.products_col.insert_many(default_products)
            print("✅ Produtos iniciais criados com sucesso!")

# Funções para compatibilidade com código antigo
def create_product(name, description, category, price, ingredients, available=True):
    service = ProductService()
    return service.create_product(name, description, category, price, ingredients, available)

def get_all_products():
    service = ProductService()
    return service.get_all_products()

def get_available_products():
    service = ProductService()
    return service.get_available_products()

def get_products_by_category(category):
    service = ProductService()
    return service.get_products_by_category(category)

def get_product_by_id(product_id):
    service = ProductService()
    return service.get_product_by_id(product_id)

def update_product(product_id, name, description, category, price, ingredients, available):
    service = ProductService()
    return service.update_product(product_id, name, description, category, price, ingredients, available)

def delete_product(product_id):
    service = ProductService()
    return service.delete_product(product_id)

def get_categories():
    service = ProductService()
    return service.get_categories()

def initialize_products():
    service = ProductService()
    return service.initialize_products()
>>>>>>> 14f1c5638fc5d459c596b1b8c06251699ec690ca
