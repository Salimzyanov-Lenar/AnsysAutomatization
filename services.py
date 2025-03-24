def update_params(parameters_dict: dict):
    if parameters_dict is None:
        raise Exception
    print(parameters_dict)
    for key, value in parameters_dict.items():
        print(f"Enter the value for {key}. The old value was: {value}")
        new_value = float(input())
        parameters_dict[key] = new_value
    print("The new parameters is:",parameters_dict)
    return parameters_dict
