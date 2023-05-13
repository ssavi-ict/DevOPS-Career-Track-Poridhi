import os

from flask import Flask, request
from namespace import NSOperation
from utils.utils import Utility

app = Flask(__name__)
ns = NSOperation()


@app.route("/", methods=['GET'])
def home():
    ret_str = "<b>! Hello From Namespace Manager!</b>" \
              "<h2>Following Are The API list for NameSpace - </h2>" \
              "<p>Create an NS- /app/create_ns/</a></p>"\
              "<p>Delete a specific NS- /app/delete_ns/</a></p>"\
              "<p>Delete All NS of a User- /app/delete_all_my_ns/</a></p>"\
              "<p>Delete All NS - /app/delete_all_ns/</a></p>" \
              "<p>Show All NS- /app/show_all_ns/</a></p>" \
              "<p>Show All NS of a User- /app/show_all_ns/</a></p>"
    return ret_str


@app.route("/app/create_ns/", methods=['GET'])
def create_network_namespace():
    ns_id = ns.create_ns(user_ip=request.remote_addr)
    return f'<b>Your VNET ID: {ns_id}</b>'


@app.route("/app/delete_ns/", methods=['POST'])
def delete_network_namespace():
    user_ip = request.remote_addr
    ns_id = request.form.get('namespace_id')
    if ns.delete_ns(user_ip=user_ip, namespace_id=ns_id):
        return f'<b>VNET ID: {ns_id} Deleted</b>'
    else:
        return f'<b>{ns_id} not found.\nDeletion Failed.</b>'


@app.route("/app/delete_all_my_ns/", methods=['GET'])
def delete_all_namespace_of_a_user():
    user_ip = request.remote_addr
    if ns.delete_namespaces(user_ip=user_ip):
        return f'<b>Deleted all VNET for {user_ip}</b>'
    else:
        return f'<b>No VNET for {user_ip} not found.</b>'


@app.route("/app/delete_all_ns/", methods=['GET'])
def delete_all_namespace():
    if ns.delete_namespaces():
        return f'<b>Deleted all VNET</b>'
    else:
        return f'<b>Some Problem Encountered.</b>'


@app.route("/app/show_all_my_ns/", methods=['GET'])
def show_all_namespaces_of_a_user():
    user_ip = request.remote_addr
    list_ns = ns.show_namespaces(user_ip=user_ip)
    if len(list_ns) > 0:
        ret_string = f"<b>Showing All Namespaces for {user_ip} - </b><br>"
        ret_string += str(list_ns)
        return ret_string
    else:
        return f"<b>No Namespaces Found for - {user_ip}</b>"


@app.route("/app/show_all_ns/", methods=['GET'])
def show_all_namespaces():
    list_ns = ns.show_namespaces()
    if len(list_ns) > 0:
        ret_string = "<b>Showing All Namespaces - </b><br>"
        ret_string += str(list_ns)
        return ret_string
    else:
        return "<b>No Namespaces Found</b>"


if __name__ == '__main__':
    db_file = os.path.join('db', 'active_ns.json')
    Utility.create_json_file(file_name=db_file)
    app.run(host='0.0.0.0', port=2349, debug=True)
