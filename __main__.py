import logging
import sys
import pandas

from mapper import Mapper
from transforms import rename_column, anonymize_first_name, anonymize_last_name, anonymize_date, anonymize_mrn


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.NOTSET)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]')
    ch.setFormatter(formatter)
    root.addHandler(ch)


if __name__ == "__main__":
    configure_logging()

    df = pandas.read_csv("QueryResults04042018.csv")

    trans = Mapper(df) \
        .rename_func(rename_column) \
        .drop_cols(["MRN Site ID", "MRN Site ID - 1", "MRN Site - 1", "MRN - 1"]) \
        .transform("First Name", anonymize_first_name) \
        .transform("Last Name", anonymize_last_name) \
        .transform("Middle Name", anonymize_first_name) \
        .transform("Date Of Birth", anonymize_date) \
        .transform("SSN", anonymize_mrn) \
        .transform("MRN", anonymize_mrn) \
        .apply() \
        .save("out.csv")
