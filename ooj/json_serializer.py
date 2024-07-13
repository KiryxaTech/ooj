import json

from .exceptions.exceptions import NotSerializableException

class JsonSerializer:
    """A class for serializing and deserializing objects."""

    def __init__(self, options: dict = None):
        """
        Initializing serialization settings.

        Parameters:
        - options (dict): Optional dictionary with settings.
        """
        self._options = options if options else {}
        self._date_format = self._options.get("date_format", "iso8601")
        self._encoding = self._options("encoding", "utf-8")
        self._ignore_errors = self._options.get("ignore_errors", False)
        self._custom_types = self._options.get("custom_types", {})
        self._transform_rules = self._options.get("transform_rules", {})
        self._indent = self._options.get("indent", None)
        self._include_fields = self._options.get("include_fields", None)
        self._exclude_fields = self._options.get("exclude_fields", None)
        self._handle_cycles = self._options.get("handle_cycles", "error")

    def serialize(self, obj: object) -> str:
        """
        Converting an object to a JSON string.

        Parameters:
        - obj (object): Serializable object.

        Returns:
        - str: Serialized JSON string.
        """
        if self.is_serializable(obj):
            return json.dumps(obj.__dict__, indent=self._indent)
        
        self.handle_error(NotSerializableException)
    
    def deserialize(self, json_str: str, cls: type) -> object:
        """
        Converts a JSON string into an object of the specified class.

        Parameters:
        - json_str (str): JSON string.
        - cls (type): Target class type.

        Returns:
        - object: Deserialized object.
        """
        if self.is_serializable(cls):
            data = json_str.__dict__

            obj = cls.__new__(cls)
            for name, value in data.items():
                setattr(obj, name, value)

            return obj
        
        self.handle_error(NotSerializableException)
    
    def serialize_to_file(self, obj: object, file_path: str):
        """
        Saving a JSON representation of an object to a file.

        Parameters:
        - obj (object): Serializable object.
        - file_path (str): Path to the file.
        """
        if self.is_serializable(obj):
            with open(file_path, 'w', encoding=self._encoding) as json_file:
                json.dump(obj.__dict__, json_file, indent=self._indent)
        
        self.handle_error(NotSerializableException)

    def deserialize_from_file(self, file_path: str, cls: type) -> object:
        """
        Loading an object from a JSON file.

        Parameters:
        - file_path (str): Path to the file.
        - cls (type): Target class type.

        Returns:
        - object: Deserialized object.
        """
        if self.is_serializable(cls):
            with open(file_path, 'r', encoding=self._encoding) as serealize_data_file:
                data = json.load(serealize_data_file)

            obj = cls.__new__(cls)
            for name, value in data.items():
                setattr(obj, name, value)

            return obj
        
        self.handle_error(NotSerializableException)
    
    def register_custom_type(self, cls: type, serializer: callable):
        """
        Registers a custom type for specific serialization and deserialization.

        Parameters:
        - cls (type): Class type.
        - serializer (callable): Custom serializer function.
        """
        self._custom_types[cls] = serializer

    def handle_error(self, error: Exception):
        """
        Handling and logging errors that occur during serialization and deserialization.

        Parameters:
        - error (Exception): Error to be handled.
        """
        if error not in self._ignore_errors:
            raise error
    
    def is_serializable(self, obj: object) -> bool:
        """
        Checking if an object can be serialized.

        Parameters:
        - obj (object): Object to check.

        Returns:
        - bool: True if the object is serializable, False otherwise.
        """
        return hasattr(obj, '__dict__')

    def get_serialization_options(self) -> dict:
        """
        Getting current serialization and deserialization options.

        Returns:
        - dict: Dictionary of options.
        """
        return self._options