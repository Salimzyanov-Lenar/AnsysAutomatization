from regex import pattern_for_params, pattern_for_variables


def get_params_from_config():
    """ 
    Reading added working_config and get params from it 
    Считывает созданный пользователем конфиг и получает параметры из него
    """
    with open("working_config.wbjn", "r", encoding="utf-8") as file:
        config = file.read()

    parameters_dict = {}

    for match in pattern_for_variables.finditer(config):
        key, value = match.groups()
        parameters_dict[key] = value

    for match in pattern_for_params.finditer(config):
        key, value = match.groups()
        parameters_dict[key] = value

    return parameters_dict


def create_new_config(config, parameters_dict):
    """ 
    Updating working_config with a new values 
    Обновляет параметры на новые в рабочем конфиге
    """
    def replace_values(match):
        key = match.group(1)
        return f'Variables=["{key}"], Values=[["{parameters_dict[key]}"]]' if key in parameters_dict else match.group(0)

    def replace_params(match):
        key = match.group(1)
        return f'Parameter={key}, Expression="{parameters_dict[key]}"' if key in parameters_dict else match.group(0)

    # Updating a config values
    new_config = pattern_for_variables.sub(replace_values, config)
    new_config = pattern_for_params.sub(replace_params, new_config)


    with open("working_config.wbjn", "w", encoding="utf-8") as file:
        file.write(new_config)

    new_config = config

def get_needed_param_value(data):
    """
    Getting the param which mappint to the target
    Получает значение параметра который соответствует target
    """
    target  = 'Equivalent Stress Maximum [MPa]'
    needed_param = None
    needed_param_value = None

    for row in data:
        for col in row:
            if target in col:
                needed_param = col.split()[0]
                

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == needed_param:
                needed_param_value = data[i+1][j]

    return needed_param_value