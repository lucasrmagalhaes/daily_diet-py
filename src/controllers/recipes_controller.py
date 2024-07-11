from bson import ObjectId
from flask import Blueprint, jsonify, request
from models.recipe_model import RecipeModel
from datetime import datetime

recipes_controller = Blueprint("recipes", __name__)

def _get_all_recipes():
    recipes = RecipeModel.find()
    return [recipe.to_dict() for recipe in recipes]

def _get_recipe(id: str):
    # ObjectId transforma uma string em ID do MongoDb
    return RecipeModel.find_one({"_id": ObjectId(id)})

@recipes_controller.route("/", methods=["GET"])
def recipe_index():
    recipes_list = _get_all_recipes()
    return jsonify(recipes_list)

@recipes_controller.route("/random", methods=["GET"])
def recipe_random():
    recipe = RecipeModel.get_random()
    if recipe is None:
        return jsonify({"error": "No recipes available"}), 404

    return jsonify(recipe.to_dict()), 200

@recipes_controller.route("/", methods=["POST"])
def recipe_post():
    data = request.json
    new_recipe = RecipeModel(
        {
            "name": data["name"],
            "description": data["description"],
            "time": data["time"],
            "is_diet": data["is_diet"],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    )
    new_recipe.save()
    return jsonify(new_recipe.to_dict()), 201

@recipes_controller.route("/<id>", methods=["PUT"])
def recipe_update(id: str):
    recipe = _get_recipe(id)
    # Exemplo de Validação
    if recipe is None:
        return jsonify({"error": "recipe not found"}), 404
    recipe.update(request.json)
    return jsonify(recipe.to_dict()), 200


@recipes_controller.route("/<id>", methods=["GET"])
def recipe_show(id: str):
    recipe = _get_recipe(id)
    if recipe is None:
        return jsonify({"error": "recipe not found"}), 404
    return jsonify(recipe.to_dict()), 200


@recipes_controller.route("/<id>", methods=["DELETE"])
def recipe_delete(id: str):
    recipe = _get_recipe(id)
    if recipe is None:
        return jsonify({"error": "recipe not found"}), 404

    recipe.delete()
    return jsonify(recipe.to_dict()), 204
