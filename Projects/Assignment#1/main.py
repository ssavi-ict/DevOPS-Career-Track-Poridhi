import os
import time


class NetworkNameSpaceVETHConnection(object):
    def __init__(self, ns1, ns2, ip1, ip2, veth1, veth2):
        self.first_namespace = ns1
        self.second_namespace = ns2
        self.first_namespace_ip = ip1
        self.second_namespace_ip = ip2
        self.first_VETH = veth1
        self.second_VETH = veth2

    def execute_os_command(self, cmd):
        print(' ----- Executing following command ---- ')
        print(cmd)
        output_stream = os.popen(cmd)
        print(' ---- Showing Command Execution Output ---')
        output_stream_show = output_stream.read()
        if len(output_stream_show) > 0:
            print(output_stream_show)
            return output_stream_show
        else:
            print('No Logs Generated for this Command')
            return None

    def create_namespaces(self):
        ns1_cmd = 'sudo ip netns add ' + self.first_namespace
        ns2_cmd = 'sudo ip netns add ' + self.second_namespace
        self.execute_os_command(ns1_cmd)
        self.execute_os_command(ns2_cmd)

    def create_veth(self):
        veth_cmd = 'sudo ip link add ' + self.first_VETH + ' type veth peer name ' + self.second_VETH
        self.execute_os_command(veth_cmd)

    def connect_ns_veth(self):
        ns1_con_cmd = 'sudo ip link set ' + self.first_VETH + ' netns ' + self.first_namespace
        ns2_con_cmd = 'sudo ip link set ' + self.second_VETH + ' netns ' + self.second_namespace
        self.execute_os_command(ns1_con_cmd)
        self.execute_os_command(ns2_con_cmd)

    def configure_ip_and_init_connection(self):
        print(' --- Configuring IP ---')
        ns1_connect = 'sudo ip -n ' + self.first_namespace + ' addr add ' + self.first_namespace_ip + ' dev ' + self.first_VETH
        ns2_connect = 'sudo ip -n ' + self.second_namespace + ' addr add ' + self.second_namespace_ip + ' dev ' + self.second_VETH
        self.execute_os_command(ns1_connect)
        self.execute_os_command(ns2_connect)

        print(' --- Powering UP vETH Connection ---')
        time.sleep(2)
        cmd_ns1 = 'sudo ip -n ' + self.first_namespace + ' link set ' + self.first_VETH + ' up'
        cmd_ns2 = 'sudo ip -n ' + self.second_namespace + ' link set ' + self.second_VETH + ' up'
        self.execute_os_command(cmd_ns1)
        self.execute_os_command(cmd_ns2)

        time.sleep(1)
        print(' --- Powering UP lo Connection ---')
        cmd_ns1 = 'sudo ip -n ' + self.first_namespace + ' link set lo up'
        cmd_ns2 = 'sudo ip -n ' + self.second_namespace + ' link set lo up'
        self.execute_os_command(cmd_ns1)
        self.execute_os_command(cmd_ns2)

        print('-- Showing Information --')
        cmd_ns1 = 'sudo ip -n ' + self.first_namespace +' addr show'
        cmd_ns2 = 'sudo ip -n ' + self.second_namespace +' addr show'
        self.execute_os_command(cmd_ns1)
        self.execute_os_command(cmd_ns2)


    def ping_and_show(self, ns_id, ip):
        ping_cmd = 'sudo ip netns exec ' + self.first_namespace + ' ping -c10 ' + ip
        if ns_id == 2:
            ping_cmd = 'sudo ip netns exec ' + self.second_namespace + ' ping -c10 ' + ip
        if self.execute_os_command(ping_cmd):
            print('Successfully pinged')
        else:
            print('Some Error Occured')


if __name__ == '__main__':
    name_space_1 = 'ns_red'
    name_space_2 = 'ns_green'
    ns_1_ip = '10.0.1.1/24'
    ns_2_ip = '10.0.1.2/24'
    veth1 = 'veth_ns_1'
    veth2 = 'veth_ns_2'
    print('--- Showing NS and VETH information -- ')
    print(name_space_1)
    print(name_space_2)
    print(ns_1_ip)
    print(ns_2_ip)
    print(veth1)
    print(veth2)
    inst = NetworkNameSpaceVETHConnection(ns1=name_space_1, ns2=name_space_2, ip1=ns_1_ip, ip2=ns_2_ip, veth1=veth1,
                                          veth2=veth2)
    inst.create_namespaces()
    inst.create_veth()
    inst.connect_ns_veth()
    inst.configure_ip_and_init_connection()
    inst.ping_and_show(ns_id=1, ip='10.0.1.2')
