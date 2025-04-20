import re


# Data parameters regex

# Variables=["Young's Modulus"],
# Values=[["200000000000 [Pa]"]])
pattern_for_variables = re.compile(r'Variables=\["(.*?)"\],\s*Values=\[\["(.*?)"\]\]')

# Parameter = parameter1,
# Expression = "15 [MPa]")
pattern_for_params = re.compile(r'Parameter=(\w+),\s*Expression="(.*?)"')



# Saving path regex
pattern_for_saving_path = re.compile(r'FilePath="([^"]+\.csv)"')