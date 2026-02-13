"""
Скрипт для генерации статического JSON файла со всеми рецептами для WebApp.
Этот файл должен быть загружен на GitHub Pages вместе с webapp_recipe.html.
"""

import json
from pathlib import Path
from services.recipe_service import RecipeService

def generate_webapp_recipes():
    """Генерирует компактный JSON файл со всеми рецептами для WebApp."""
    service = RecipeService()
    
    # Получаем все рецепты напрямую из внутреннего списка
    # Используем приватный атрибут _recipes, так как публичного метода для получения всех рецептов нет
    all_recipes = service._recipes  # type: ignore
    
    # Формируем компактный формат для WebApp
    webapp_data = {}
    for recipe in all_recipes:
        # Формируем ингредиенты
        if recipe.instructions_ingredients:
            ingredients = [line.strip() for line in recipe.instructions_ingredients.split("\n") if line.strip()]
        else:
            ingredients = [f"{ing.name} — {ing.amount}" for ing in recipe.ingredients]
        
        # Формируем инструкции
        if recipe.instructions:
            instructions = [line.strip() for line in recipe.instructions.split("\n") if line.strip()]
        else:
            instructions = []
        
        # Компактный формат
        webapp_data[recipe.id] = {
            "n": recipe.name,  # name
            "c": recipe.calories,  # calories
            "p": recipe.proteins,  # proteins
            "f": recipe.fats,  # fats
            "cb": recipe.carbs,  # carbs
            "i": ingredients,  # ingredients
            "ins": instructions  # instructions
        }
    
    # Сохраняем в файл
    output_file = Path("webapp_recipes.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(webapp_data, f, ensure_ascii=False, separators=(',', ':'))
    
    print(f"✅ Сгенерирован файл {output_file} с {len(webapp_data)} рецептами")
    print(f"📁 Размер файла: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"📤 Загрузите этот файл на GitHub Pages в ту же папку, что и webapp_recipe.html")

if __name__ == "__main__":
    generate_webapp_recipes()
