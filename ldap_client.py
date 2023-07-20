import json
import ldap3
import os
from ldap3 import Server, Connection, ALL, core


def get_ldap_config():
    f = open('config.json', 'r')
    content = f.read()
    config = json.loads(content)
    f.closed
    ldap_conf_list = [
        "LDAP_host",
        "LDAP_port",
        "LDAP_admin",
        "LDAP_admin_passwd",
        "LDAP_base_dn"
    ]
    ldapconfig = {}
    for n in ldap_conf_list:
        if os.getenv(n) is None:
            ldapconfig[n] = config.get("LDAP").get(n)
        else:
            ldapconfig[n] = os.getenv(n)
    return ldapconfig


class LdapOpt(object):
    def __init__(self, username=None, password=None):
        '''
        :param host: ldap 服务器
        :param port:  端口
        :param BaseDN:
        :param user_name:
        :param password:
        :param user_dn:用户dn

        '''
        self.host = get_ldap_config().get("LDAP_host")
        self.port = int(get_ldap_config().get("LDAP_port"))
        self.BaseDN = get_ldap_config().get("LDAP_base_dn")
        if username == None:
            self.user_name = get_ldap_config().get("LDAP_admin")
        else:
            self.user_name = username
        if password == None:
            self.password = get_ldap_config().get("LDAP_admin_passwd")
        else:
            self.password = password
        print(self.host, self.port, self.BaseDN, username, )
        self.UserDN = "cn=" + self.user_name + ',' + self.BaseDN

    def check_server(self):
        try:
            s = Server(self.host, self.port, use_ssl=False, get_info=ALL, connect_timeout=5, )
            c = Connection(s)  # define an ANONYMOUS connection
            conn_stat = c.bind()
            c.closed
            if conn_stat:
                print("check_ldap_server OK", )
                return True
            else:
                print("check_ldap_server false")
                return False

        except ldap3.core.exceptions.LDAPSocketOpenError:
            print("check_server False", )
            return False

    def check_user(self):
        if self.check_server():
            try:
                s = Server(self.host, self.port, use_ssl=False, get_info=ALL, connect_timeout=5, )
                # print("服务器信息 ", s.address_info, )
                conn = Connection(s, self.UserDN, self.password, auto_bind=True, read_only=True)
                stat = conn.bind()
                conn.closed
                if stat:
                    return True
                else:
                    return False

            except ldap3.core.exceptions.LDAPBindError:
                # print("bind 错误")
                return False
        else:
            return False

    def get_user_list(self):
        if self.check_server():
            print("auth-server----ok")
            try:
                s = Server(self.host, self.port, use_ssl=False, get_info=ALL, connect_timeout=5, )
                conn = Connection(s, self.UserDN, self.password, auto_bind=True, read_only=True)
                # print("用户连接状态", conn, )
                print("管理员", conn.extend.standard.who_am_i(), )

                conn.search(search_base=self.BaseDN, search_filter='(objectClass=inetOrgPerson)',
                            attributes=['cn', "mail", 'displayName'], )
                users_dict = {}
                for n in conn.response:
                    cn = n["attributes"]["cn"][0]
                    mail = n["attributes"]["mail"][0]
                    display_name = n["attributes"]["displayName"]
                    # 打印显示
                    print(cn, mail, display_name)
                    users_dict[cn] = {}
                    users_dict[cn]["cn"] = cn
                    users_dict[cn]["mail"] = mail
                    users_dict[cn]["displayname"] = display_name

                if conn.result["description"] == "success":
                    print(conn.result["description"])
                    return users_dict
                else:
                    return False

            except ldap3.core.exceptions.LDAPBindError:
                print("bind 错误")
                return False
        else:
            print("服务器无法连接")
            return False

# 调试用获取ldap 用户列表
a = LdapOpt()
a.get_user_list()
