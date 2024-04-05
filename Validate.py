#####################################################################################
# Name: Ivan Moleko
# bugs or note:
# date: 04/05/23
#####################################################################################
import re
import datetime
# from validate_email_address import validate_email
import validate_email

class IsValid:
    def __init__(self):
        pass

    def Length(self, text, length, switch):  # length check method
        match switch:
            case 0:  # is equal to given length
                if len(text) == length:
                    return True
                else:
                    return False

            case 1:  # is greater than given length
                if length > len(text):
                    return True
                else:
                    return False

            case 2:  # is greater than or equal to given length
                if length >= len(text):
                    return True
                else:
                    return False

            case 3:  # is less than given length
                if length > len(text):
                    return True

            case 4:  # is less than or equal given length
                if length >= len(text):
                    return True

    def Number(self, text):  # valid number format requires a string
        phone_number_pattern = re.compile(
            "(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}")  # is an example format for a number
        match = re.search(phone_number_pattern, text)  # searches if the text fits the pattern
        if match:
            return True

    def Email(self, text):
        email_pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(email_pattern, text):
            return True
        else:
            return False

    def Date(self, text):
        try:
            # Split the date string into month, day, and year
            month, day, year = map(int, text.split('/'))

            # Check if the values fall within appropriate ranges
            if 1 <= month <= 12 and 1 <= day <= 31 and 0 <= year <= 99:
                return True
            else:
                return False
        except (ValueError, IndexError):
            return False

    def name_check(self, name,pattern):
        # Regular expression pattern to match only letters (both uppercase and lowercase)
        if pattern == None:
            pattern = r'^[a-zA-Z]+$'
        else:
            pattern = pattern

        # Check if the name matches the pattern
        if re.match(pattern, name):
            return True
        else:
            return False

    def validate_date_of_birth(self, dob, min_age_days=60):
        # Convert the date string to a datetime object
        try:
            dob_date = datetime.datetime.strptime(dob, "%Y/%m/%d")
        except ValueError:
            # Invalid date format
            return False

        # Get the current date
        current_date = datetime.datetime.now()

        # Calculate the difference in days between the current date and the date of birth
        age_days = (current_date - dob_date).days

        # Check if the age in days is at least the specified minimum age
        if age_days < min_age_days:
            # Date of birth is too recent
            return False
        else:
            return True


if __name__ == "__main__":
    validate = IsValid()
    validate.Email("kingkongkillnumber7@gmail.com")
