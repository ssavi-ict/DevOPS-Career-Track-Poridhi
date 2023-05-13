import os
import json


class Utility:
    def __init__(self):
        pass

    @staticmethod
    def execute_os_command(cmd):
        print('\n ----- Executing following command ---- ')
        print(cmd)
        output_stream = os.popen(cmd)
        print(' ---- Showing Command Execution Output ---- \n')
        output_stream_show = output_stream.read()
        if len(output_stream_show) > 0:
            print(output_stream_show)
            return output_stream_show
        else:
            print('No Logs Generated for this Command')
            return None

    @staticmethod
    def create_json_file(file_name):
        data = {}
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                json.dump(data, f)
        else:
            with open(file_name, 'r') as f:
                content = f.readlines()
            if len(content) == 0:
                with open(file_name, 'w') as f:
                    json.dump(data, f)

    @staticmethod
    def get_json_content(file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def update_json_file(file_name, json_data):
        with open(file_name, 'w') as f:
            json.dump(json_data, f)

    @staticmethod
    def add_to_json(file_name, key, value):
        json_data = Utility.get_json_content(file_name=file_name)
        if key in json_data:
            json_data[key].append(value)
        else:
            json_data[key] = [value]
        Utility.update_json_file(file_name=file_name, json_data=json_data)
        return True

    @staticmethod
    def remove_from_json(file_name, key, value):
        json_data = Utility.get_json_content(file_name=file_name)
        if key in json_data:
            if value in json_data[key]:
                json_data[key].remove(value)
                if len(json_data[key]) == 0:
                    del json_data[key]
                Utility.update_json_file(file_name=file_name, json_data=json_data)
                return True
            else:
                print(f"{value} not found in {key}. Could Not Remove.")
                return False
        else:
            print(f"{key} not found in DB.  Could Not Remove.")
            return False

    @staticmethod
    def remove_all_json_content(file_name):
        new_data = {}
        with open(file_name, 'w') as f:
            json.dump(new_data, f)

    @staticmethod
    def check_if_found(file_name, ns_id):
        json_data = Utility.get_json_content(file_name=file_name)
        for key in json_data:
            if ns_id in json_data[key]:
                return True
        return False


if __name__ == '__main__':
    fname = 'data.json'
    Utility.create_json_file(file_name=fname)
    # Utility.add_to_json(file_name=fname, key="key1", value="value1")
    # Utility.add_to_json(file_name=fname, key="key1", value="value2")
    # Utility.add_to_json(file_name=fname, key="key2", value="value3")
    # Utility.remove_from_json(file_name=fname, key="key2", value="value3")
    # Utility.remove_from_json(file_name=fname, key="key2", value="value5")
    # Utility.remove_from_json(file_name=fname, key="key2", value="value3")
    # Utility.remove_all_json_content(file_name=fname)

