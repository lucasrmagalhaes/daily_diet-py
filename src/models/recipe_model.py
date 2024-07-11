import random
from .db import db
from .abstract_model import AbstractModel

class RecipeModel(AbstractModel):
    # Define que a Coleção (=~ tabela) "recipes" do Banco.
    _collection = db["recipes"]

    # Nosso construtor receberá um dicionário (JSON) para instanciar um objeto
    def __init__(self, json_data):
        super().__init__(json_data)
    
    # Retornar uma receita aleatória, é uma regra de negócio especifica
    # Fazendo sentido manter somente para a model Recipe
    @classmethod
    def get_random(cls):
        data = cls.find()
        if not data:
            return
        return random.choice(data)

    # Define as regras de como o objeto JokeModel pode virar um Dict
    def to_dict(self):
        return {
            '_id': str(self.data['_id']),
            'name': self.data['name'],
            'description': self.data['description'],
            'time': self.data['time'],
            'is_diet': self.data['is_diet'],
        }
