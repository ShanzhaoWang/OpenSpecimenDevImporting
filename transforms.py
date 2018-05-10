import datetime
import logging
import names


def rename_column(x):
    return str(x).replace("Participant_", "")


def anonymize_first_name(_):
    return names.get_first_name()


def anonymize_last_name(_):
    return names.get_last_name()


def anonymize_ssn(ssn):
    if ssn == "nan" or ssn is None:
        return ssn

    ssn = str(ssn).split(" ")
    if len(ssn) < 3:
        logging.warning("Skipping SSN:" + str(ssn))
        return ssn

    first = (int(ssn[0]) + 10) % 1000
    second = (int(ssn[1]) + 10) % 100
    third = ssn[2]

    return "{0} {1} {2}".format(first, second, third)


def anonymize_date(start_date):
    try:
        date_1 = datetime.datetime.strptime(str(start_date), "%m-%d-%Y %H:%M")

        end_date = date_1 + datetime.timedelta(days=1)
        return end_date
    except ValueError:
        logging.warning("Skipping Date:" + str(start_date))
        return start_date


def anonymize_mrn(x):
    # Add 1 to the first character...

    if str(x) == "nan" or x is None:
        return x
    return str((int(str(x)[0]) + 1) % 10) + str(x)[1:]
