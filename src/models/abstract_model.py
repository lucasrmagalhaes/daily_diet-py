# abstract_model.py
from pymongo.collection import ReturnDocument, Collection

class AbstractModel:
    _collection: Collection = None

    def __init__(self, data: dict):
        self.data = data

    def save(self):
        result = self._collection.insert_one(self.data)
        inserted_document = self._collection.find_one(
            {"_id": result.inserted_id}
        )
        self.data = inserted_document
        return self.data

    @classmethod
    def find(cls, query: dict = {}):
        data = cls._collection.find(query)
        return [cls(d) for d in data]

    @classmethod
    def find_one(cls, query: dict = {}):
        data = cls._collection.find_one(query)
        return cls(data) if data else None

    def update(self, data: dict):
        # Por padrão o find_one_and_update retorna o estado anterior do
        # registro, por isso, utilizamos o ReturnDocument.AFTER para
        # retornar a versão pós atualização
        result = self._collection.find_one_and_update(
            {"_id": self.data["_id"]},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )

        self.data = result
        return self.data

    def delete(self):
        self._collection.delete_one({"_id": self.data["_id"]})
