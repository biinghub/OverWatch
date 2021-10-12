import yamale
#Please ensure to run the following command 
#'pip3 install yamale' (since we don't have virtual environments)
def validate_rules(rules):
    # Create a Schema object - ensure it is in the root of library's folder
    schema = yamale.make_schema('./schema.yaml')
    # Create a Data object - parses user-defined rules to yamale parser
    data = yamale.make_date(rules)
    # Validate data against the schema. Throws a ValueError if data is invalid.
    yamale.validate(schema, data)