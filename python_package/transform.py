import string
import random
from csv import writer
import csv
import json
import pandas as pd


class Transform(object):
    def __init__(self):
        pass

    def generate_random_password(self, range_int):
        random_source = string.ascii_letters + string.digits + string.punctuation
        # select 1 lowercase
        password = random.choice(string.ascii_lowercase)
        # select 1 uppercase
        password += random.choice(string.ascii_uppercase)
        # select 1 digit
        password += random.choice(string.digits)
        # select 1 special symbol
        password += random.choice(string.punctuation)

        # generate other characters
        for i in range(range_int):
            password += random.choice(random_source)

        password_list = list(password)
        # shuffle all characters
        random.SystemRandom().shuffle(password_list)
        password = ''.join(password_list)
        return password

    def append_list_as_row(self, file_name, list_of_elem):

        # Open file in append mode
        with open(file_name, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)

    def load_csv(self, file_name):

        with open(file_name) as f:
            reader = csv.DictReader(f)
            list_of_dict = list(reader)

        return list_of_dict

    def string_to_list_of_dict(self, text):

        response = json.loads(text)

        return response

    def agragate_list_of_dict(self, *args):

        combined_list = []
        for arg in args:
            combined_list = combined_list + arg

        return combined_list

    def group_list_of_dict(self, data):

        df = pd.DataFrame(data)
        numbers = []
        for index, row in df.groupby("number").count().query("numberid<4").iterrows():

            numbers.append({"number": index,
                            "id": df[df["number"] == index]["numberid"].iloc[0],
                            "status": df[df["number"] == index]["status"].iloc[0]})

        return numbers
