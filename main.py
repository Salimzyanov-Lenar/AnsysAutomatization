import services
from re_expressions import pattern_for_params, pattern_for_variables


with open("config.txt", "r", encoding="utf-8") as file:
    config = file.read()

parameters_dict = {}

for match in pattern_for_variables.finditer(config):
    key, value = match.groups()
    parameters_dict[key] = value

for match in pattern_for_params.finditer(config):
    key, value = match.groups()
    parameters_dict[key] = value


services.update_params(parameters_dict)

def replace_values(match):
    key = match.group(1)
    return f'Variables=["{key}"], Values=[["{parameters_dict[key]}"]]' if key in parameters_dict else match.group(0)

def replace_params(match):
    key = match.group(1)
    return f'Parameter={key}, Expression="{parameters_dict[key]}"' if key in parameters_dict else match.group(0)

# Updating a config values
new_config = pattern_for_variables.sub(replace_values, config)
new_config = pattern_for_params.sub(replace_params, new_config)


# Creating a new config
with open("updated_config.txt", "w", encoding="utf-8") as file:
    file.write(new_config)

new_config = config
