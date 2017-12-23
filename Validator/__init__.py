import gzip

from ValidationReport import ValidationReport, State, RecordError


class Validator:
    PLUS_CHAR = 43
    AT_CHAR = 64

    def __init__(self):
        self.validation_results = None
        self.sequence_symbols = list()
        for symbol in "ACTGN.":
            self.sequence_symbols.append(ord(symbol))


    def validate(self, file_path):
        try:
            with gzip.open(file_path) as source:
                return self._validate_source_bytes(source)
        except OSError:
            with open(file_path, 'rb') as source:
                return self._validate_source_bytes(source)

    def _validate_source_bytes(self, source):
        valid = True
        record = list()
        report = State.INVALID.report()
        for line in source:
            if not valid:
                break
            line = line.rstrip()
            line_is_not_empty = line  # added for readability
            if line_is_not_empty:
                record.append(line)
                record_is_ready = len(record) == 4
                if record_is_ready:
                    errors = self._find_errors(record)
                    valid = valid and not errors
                    if not valid:
                        report.errors = errors
                    record.clear()
            else:
                valid = False
        if len(record) != 0:
            #TODO consider using error codes instead of actual error messages
            report.log_error("does not contain a multiple of 4 lines. Please check that the file has "
                             "not been truncated.")
        valid = valid and len(record) == 0
        return State.VALID.report() if valid \
        else report

    def _find_errors(self, record):
        errors = []
        sequence_id = record[0].decode('UTF-8')
        if not self._validate_identifier_line(record[0]):
            errors.append(1)
        if not self._validate_bases(record[1]):
            errors.append(RecordError.Type.INVALID_SEQUENCE.report_error(sequence_id))
        if not self._validate_plus(record[2]):
            errors.append(1)
        if not self._validate_quality_scores(record[3]):
            errors.append(1)
        if not self._validate_bases_length_equals_qc_length(record[1], record[3]):
            errors.append(1)
        return errors

    def _validate_identifier_line(self, line):
        # is the first char @ ?
        has_at_char = line[0] == Validator.AT_CHAR
        # all ascii chars?
        all_ascii = Validator._all_ascii(line)
        return has_at_char and all_ascii

    #TODO implement case insensitive check
    def _validate_bases(self, line):
        valid = False
        has_n_char = False
        has_period = False
        for symbol in line:
            valid = symbol in self.sequence_symbols
            if valid:
                if symbol == ord("N"):
                    has_n_char = True
                if symbol == ord("."):
                    has_period = True
            else:
                break
        return valid and not (has_n_char and has_period)

    def _validate_plus(self, line):
        # is the first char a plus sign?
        has_plus_char = line[0] == Validator.PLUS_CHAR
        return has_plus_char

    def _validate_quality_scores(self, line):
        for symbol in line:
            if not (33 <= symbol <= 126):
                return False
        return True

    def _validate_bases_length_equals_qc_length(self, base_line, qc_line):
        base_length = len(base_line)
        quality_length = len(qc_line)
        return base_length == quality_length

    @staticmethod
    def _all_ascii(line):
        for char in line:
            if char > 128:
                return False
        return True