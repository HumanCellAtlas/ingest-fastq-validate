import os
import unittest

from validator.fastq import Validator

BASE_DIR = os.path.dirname(__file__)

class TestFastqFileValidation(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.validator = Validator()

    #### single record tests###

    def test_validates_ascii(self):
        self._do_test_validate_as_valid('single_valid')

    def test_fails_with_invalid_ascii(self):
        self._do_test_validate_as_invalid('single_invalid-ascii')

    def test_correct_number_of_lines_and_valid_ascii(self):
        self._do_test_validate_as_valid('single_correct-num-lines')

    def test_no_plus_char_on_third_line(self):
        self._do_test_validate_as_invalid('single_no-plus-char')

    def test_no_ampersand_as_first_char(self):
        self._do_test_validate_as_invalid('single_no-at-symbol')

    def test_validates_data_with_n_in_sequence(self):
        self._do_test_validate_as_valid('single_valid-with-n-char')

    def test_validates_data_with_period_in_sequence(self):
        self._do_test_validate_as_valid('single_valid-with-period')

    def test_validates_data_with_mixed_n_and_period(self):
        self._do_test_validate_as_invalid('single_invalid-has-n-then-period')
        self._do_test_validate_as_invalid('single_invalid-has-period-then-n')

    def test_big_record(self):
        self._do_test_validate_as_valid('single_big')

    # multiple record tests

    def test_validates_ascii_multiple_records(self):
        self._do_test_validate_as_valid('multiple_valid-ascii')

    def test_invalid_multiple_records(self):
        self._do_test_validate_as_invalid('multiple_non-matching-lengths')

    def test_invalid_multiple_records_with_missing_lines(self):
        self._do_test_validate_as_invalid('multiple_missing-lines')

    # test templates

    def _do_test_validate_as_valid(self, test_data):
        self._do_test_validate(test_data, self.assertTrue)

    def _do_test_validate_as_invalid(self, test_data):
        self._do_test_validate(test_data, self.assertFalse)

    def _do_test_validate(self, test_data, assertion):
        file_name = "%s.fastq" % (test_data)
        file_path = os.path.join(BASE_DIR, 'test_files', 'fastq', file_name) # $BASE_DIR/test_files/fastq/<file_name>
        results = self.validator.validate(os.path.abspath(file_path))
        assertion(results)