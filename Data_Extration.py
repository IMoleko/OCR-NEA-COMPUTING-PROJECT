import mysql.connector
import pandas as pd

class DataExtractor:
    def __init__(self, connection, given_user_id):
        self.user_id = given_user_id
        self.connection = connection
        self.cursor = connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()

    def get_lowest_score(self, test_id):
        try:
            query = '''SELECT MIN(score) FROM StudentTestRelationship WHERE test_id = %s;'''
            self.cursor.execute(query, (test_id,))
            result = self.cursor.fetchone()
            return result[0] if result is not None else None
        except mysql.connector.Error as err:
            print(f"Error in get_lowest_score: {err}")

    def get_highest_score(self, test_id):
        try:
            query = '''SELECT MAX(score) FROM StudentTestRelationship WHERE test_id = %s;'''
            self.cursor.execute(query, (test_id,))
            result = self.cursor.fetchone()
            return result[0] if result is not None else None
        except mysql.connector.Error as err:
            print(f"Error in get_highest_score: {err}")

    def get_test_name(self, test_id):
        try:
            query = '''SELECT name FROM Tests WHERE test_id = %s;'''
            self.cursor.execute(query, (test_id,))
            test_name_result = self.cursor.fetchone()
            return test_name_result[0] if test_name_result else None
        except mysql.connector.Error as err:
            print(f"Error in get_test_name: {err}")

    def get_test_score(self, test_id):
        try:
            query = '''SELECT score FROM StudentTestRelationship WHERE user_id = %s AND test_id = %s;'''
            self.cursor.execute(query, (self.user_id, test_id))
            result = self.cursor.fetchone()
            return result[0] if result is not None else None
        except mysql.connector.Error as err:
            print(f"Error in get_test_score: {err}")

    def calc_average_score_for_test(self, test_id):
        try:
            query = '''SELECT AVG(score) FROM StudentTestRelationship WHERE test_id = %s;'''
            self.cursor.execute(query, (test_id,))
            average_score_result = self.cursor.fetchone()

            # Check if average_score_result is not None before accessing its elements
            if average_score_result is not None and average_score_result[0] is not None:
                return int(average_score_result[0])
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error in calc_average_score_for_test: {err}")

    def get_max_score_for_test(self, test_id):
        try:
            query = '''SELECT max_score FROM Tests WHERE test_id = %s;'''
            self.cursor.execute(query, (test_id,))
            max_score_result = self.cursor.fetchone()
            return max_score_result[0] if max_score_result is not None else None
        except mysql.connector.Error as err:
            print(f"Error in get_max_score_for_test: {err}")

    def calc_percentage(self, test_id, score):
        max_score = self.get_max_score_for_test(test_id)
        if max_score is not None and max_score != 0:
            percentage = (score / max_score) * 100
            return int(round(percentage))
        else:
            return None

    def calc_score_difference(self, test_id, score):
        try:
            average_score = self.calc_average_score_for_test(test_id)
            if average_score is not None:
                difference = score - average_score
                return int(difference)
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error in calculate_score_difference: {err}")

    def get_user_name(self):
        try:
            query = '''SELECT name FROM Users WHERE user_id = %s;'''
            self.cursor.execute(query, (self.user_id,))
            name_result = self.cursor.fetchone()
            return name_result[0] if name_result else None
        except mysql.connector.Error as err:
            print(f"Error in get_user_name: {err}")

    def get_num_tests(self):
        query = "SELECT COUNT(*) FROM Tests"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_all_test_ids(self):
        try:
            query = "SELECT test_id FROM Tests"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return [row[0] for row in result] if result else None
        except mysql.connector.Error as err:
            print(f"Error in get_all_test_ids: {err}")

    def get_user_id_from_email(self, email):
        try:
            query = '''SELECT user_id FROM Users WHERE email = %s;'''
            self.cursor.execute(query, (email,))
            user_id_result = self.cursor.fetchone()
            return user_id_result[0] if user_id_result else None
        except mysql.connector.Error as err:
            print(f"Error in get_user_id_from_email: {err}")


if __name__ == "__main__":
    # Database connection
    db_connection = mysql.connector.connect(
        user='thapelomoleko',
        password='Thapeloivan2006*',
        host='db4free.net',
        database='tracker'
    )

    given_user_id = 1
    # Create DataExtractor instance
    data_extractor = DataExtractor(db_connection, given_user_id)
