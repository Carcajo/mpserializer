# Library for serializing and deserializing python objects into different formats & console utility for converting from one format to another

### serializers:
- serializer - main class (you should initialize with the name of parser) that allows serializing and deserializing into chosen format 
- serialization - set of functions that handles serialization/deserialization of python objects
- /parsers
    - contains different parsers (json, yaml, toml, pickle)
    - parser_factory_method - function that returns parser by its name

### tests
- test_serialization - tests for serialization/deserialization of different function 
