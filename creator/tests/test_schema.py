from creator.utils import validate

print(validate.validate_path("../res/schema/pokemon.json", "../res/data/pokemon.json"))
print(validate.validate_path("../res/schema/pokedex_extra.json", "../res/data/pokedex_extra.json"))
print(validate.validate_path("../res/schema/moves.json", "../res/data/moves.json"))
print(validate.validate_path("../res/schema/evolve.json", "../res/data/evolve.json"))
