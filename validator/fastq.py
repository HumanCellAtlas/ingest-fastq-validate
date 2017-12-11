from functools import reduce

class Validator:
    PLUS_CHAR = 43
    AT_CHAR = 64

    def __init__(self):
        self.validation_results = None
        self
        pass

    def validate(self, file_path):
        valid = False
        with open(file_path, "rb") as source:
            record = list()
            validation_results = list()
            for line in source:
                line = line.rstrip()
                line_is_not_empty = line # added for readability
                if line_is_not_empty:
                    record.append(line)
                    record_is_ready = len(record) == 4
                    if record_is_ready:
                        validation_results.append(self._validate_record(record))
                        record.clear()
            valid = len(record) == 0
            if valid:
                valid = reduce(lambda val_result, next_val_result: val_result and next_val_result, validation_results)
        return valid

    def _validate_record(self, record):
        return self._validate_identifier_line(record[0]) \
               and self._validate_bases(record[1]) \
               and self._validate_plus(record[2]) \
               and self._validate_qc(record[3]) \
               and self._validate_bases_length_equals_qc_length(record[1], record[3])

    def _validate_identifier_line(self, line):
        # is the first char @ ?
        has_at_char = line[0] == Validator.AT_CHAR
        # all ascii chars?
        all_ascii = Validator._all_ascii(line)
        return has_at_char and all_ascii

    #TODO implement case insensitive check
    def _validate_bases(self, line):
        has_n_char = False
        for symbol in line:
            if symbol not in (ord(value) for value in "ACGTN."):
                return False
            else:
                if symbol == ord("N"):
                    has_n_char = True
                if has_n_char and symbol == ord("."):
                    return False
        return True

    def _validate_plus(self, line):
        # is the first char a plus sign?
        has_plus_char = line[0] == Validator.PLUS_CHAR
        return has_plus_char

    def _validate_qc(self, line):
        # TODO
        return True

    def _validate_bases_length_equals_qc_length(self, base_line, qc_line):
        return len(base_line) == len(qc_line)

    @staticmethod
    def _all_ascii(line):
        for char in line:
            if char > 128:
                return False
        return True
