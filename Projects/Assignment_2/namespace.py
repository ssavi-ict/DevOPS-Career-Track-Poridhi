import json
import os
import uuid

from utils.utils import Utility


class NSOperation(object):
    def __init__(self):
        self.db_file = os.path.join('db', 'active_ns.json')

    def create_ns(self, user_ip):
        while True:
            namespace_id = 'test_vnet_'
            vnet_id = uuid.uuid4().hex[:13]
            namespace_id += vnet_id
            if not Utility.check_if_found(file_name=self.db_file, ns_id=namespace_id):
                break

        create_cmd = 'sudo ip netns add ' + namespace_id
        try:
            Utility.execute_os_command(create_cmd)
            print('[Create Namespace] Success ... ')
            Utility.add_to_json(file_name=self.db_file, key=user_ip, value=namespace_id)
            return namespace_id
        except Exception as e:
            print('[Create Namespace] Failure ... ')
            print('Original Message: ', str(e))
            return ""

    def delete_ns(self, user_ip, namespace_id):
        delete_cmd = 'sudo ip netns delete ' + namespace_id
        try:
            Utility.execute_os_command(delete_cmd)
            print('[Delete Namespace] Success ... ')
            Utility.remove_from_json(file_name=self.db_file, key=user_ip, value=namespace_id)
            return True
        except Exception as e:
            print('[Delete Namespace] Failure ... ')
            print('Original Message: ', str(e))
            return False

    def show_namespaces(self, user_ip="ALL"):
        print('===================================')
        print(f'Getting Namespaces For - {user_ip}')
        print('===================================')
        with open(self.db_file, 'r') as f:
            db_content = json.load(f)
        namespace_list = []
        for key, value in db_content.items():
            if key == user_ip or user_ip == "ALL":
                for item in value:
                    print(f'NamesSpace {item} is currently belong to {key}')
                    namespace_list.append(item)
        return namespace_list

    def show_all_ns_from_system(self):
        watch_cmd = 'ip netns list'
        try:
            # Utility.execute_os_command.execute_os_command(watch_cmd)
            print('[Show Namespace] Success ... ')
            return True
        except Exception as e:
            print('[Show Namespace] Failure ... ')
            print('Original Message: ', str(e))
            return False

    def delete_namespaces(self, user_ip="ALL"):
        with open(self.db_file, 'r') as f:
            db_content = json.load(f)
        status = True
        for key, value in db_content.items():
            if key == user_ip or user_ip == "ALL":
                for item in value:
                    print(f'Deleting NamesSpace {item} which is currently belong to {key}')
                    if not self.delete_ns(namespace_id=item, user_ip=key):
                        status = False
        return status


if __name__ == '__main__':
    ns = NSOperation()
    '''ns.create_ns(user_ip='10.1.1.4')
    ns.create_ns(user_ip='10.1.2.4')
    ns.create_ns(user_ip='10.1.3.4')'''

    # ns.delete_namespaces(user_ip='10.1.1.4')
    # ns.delete_namespaces()
    # ns.delete_ns(user_ip='10.1.2.4', namespace_id='test_vnet_c09780436dcf4')

    ns.show_namespaces()
    ns.show_namespaces(user_ip='10.1.1.4')
    ns.show_namespaces(user_ip='10.1.2.4')
