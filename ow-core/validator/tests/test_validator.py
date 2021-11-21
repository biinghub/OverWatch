import pytest
from validator import validator
from validator.validator import DuplicateNameException
from validator.validator import ValidationException
import unittest


class ValidationTestCases(unittest.TestCase):
    def test_set_rules(self):
        # The test ensures argument parsing for rule declaration works
        v1 = validator.OverwatchValidator("ow-core/example", False)
        v2 = validator.OverwatchValidator("ow-core/validator/tests/test2", False)
        assert v1.rules_dir_path == "ow-core/example/"
        assert v2.rules_dir_path == "ow-core/validator/tests/test2/"

    def test_validate_rules_structure(self):
        v2 = validator.OverwatchValidator("ow-core/validator/tests/test2", False)
        v2.load_rules()
        # rules.yaml is an example configuration file that follows the schema
        # defined in schema.yaml
        # therefore, the assertion proves that the validate rules structure function works
        # by returning true
        assert v2.validate_rules_structure() == (True, "All Rules Files Valid")

    def test_validate_rules_structure_fails(self):
        v3 = validator.OverwatchValidator("ow-core/validator/tests/test1", False)
        v3.load_rules()
        # test.yaml is an example configuration file that does NOT follow the schema
        # defined in schema.yaml
        # therefore, the assertion proves that the validate rules structure function works
        # by raising exception
        assert v3.validate_rules_structure() == (
            False,
            "Invalid Rules File - more_bad_rule.yaml - Schema Error",
        )

    def test_validate_alarm_attributes_works(self):
        v2 = validator.OverwatchValidator("ow-core/example/", False)
        v2.load_rules()
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        assert v2.validate_alarm_attributes() == ["simple-rule", "simple-rule2"]

    def test_validate_alarm_attributes_exception(self):
        v2 = validator.OverwatchValidator("ow-core/validator/tests/test2", False)
        v2.load_rules()
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        with self.assertRaises(ValidationException):
            v2.validate_alarm_attributes()

    def test_validate_metric_attributes(self):
        v2 = validator.OverwatchValidator("ow-core/example", False)
        v2.load_rules()
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        assert v2.validate_metric_attributes() == ["simple-filter", "simple-filter2"]

    def test_validate_metric_attributes_exception(self):
        v2 = validator.OverwatchValidator("ow-core/validator/tests/test2", False)
        v2.load_rules()
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        with self.assertRaises(ValidationException):
            v2.validate_metric_attributes()


if __name__ == "__main__":
    unittest.main()
