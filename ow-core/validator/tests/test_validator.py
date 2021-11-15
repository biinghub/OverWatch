import pytest
from validator import validator
from validator.validator import DuplicateNameException
import unittest


class ValidationTestCases(unittest.TestCase):
    def test_set_rules(self):
        # The test ensures argument parsing for rule declaration works
        v1 = validator.OverwatchValidator("example/rules.yaml", False)
        v2 = validator.OverwatchValidator("ow-core/validator/tests/test.yaml", False)
        assert v1.rule_path == "example/rules.yaml"
        assert v2.rule_path == "ow-core/validator/tests/test.yaml"

    def test_validate_rules_structure(self):
        v2 = validator.OverwatchValidator("example/rules.yaml", False)
        # rules.yaml is an example configuration file that follows the schema
        # defined in schema.yaml
        # therefore, the assertion proves that the validate rules structure function works
        # by returning true
        assert v2.validate_rules_structure() == (True, "Valid Rules File")

    def test_validate_rules_structure_fails(self):
        v3 = validator.OverwatchValidator("ow-core/validator/tests/test.yaml", False)
        # test.yaml is an example configuration file that does NOT follow the schema
        # defined in schema.yaml
        # therefore, the assertion proves that the validate rules structure function works
        # by returning false
        assert v3.validate_rules_structure() == (False, "Invalid Rules File")

    def test_validate_alarm_attributes_works(self):
        v2 = validator.OverwatchValidator("example/rules.yaml", False)
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        assert v2.validate_alarm_attributes() == ["alarmnamestring"]

    def test_validate_alarm_attributes_exception(self):
        v2 = validator.OverwatchValidator("ow-core/validator/tests/test2.yaml", False)
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        with self.assertRaises(DuplicateNameException):
            v2.validate_alarm_attributes()

    def test_validate_metric_attributes(self):
        v2 = validator.OverwatchValidator("example/rules.yaml", False)
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        assert v2.validate_metric_attributes() == ["FilterName"]

    def test_validate_metric_attributes_exception(self):
        v2 = validator.OverwatchValidator("ow-core/validator/tests/test2.yaml", False)
        # rules.yaml only has 1 alarm name, called alarmnamestring
        # assertion shows the function works in grabbing these attribtues
        with self.assertRaises(DuplicateNameException):
            v2.validate_metric_attributes()


if __name__ == "__main__":
    unittest.main()
