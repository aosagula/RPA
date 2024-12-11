class Config:
    def __init__(self, dux_username, dux_password, djve_xml_path="", db_url="", db_name="", 
                db_username="", db_password="", db_port="", dux_url="" ,
                email_host="", email_port="", email_user="", email_password="", download_path="", dux_txt_to_sim=""):
        self.dux_username = dux_username
        self.dux_password = dux_password
        self.djve_xml_path = djve_xml_path
        self.db_url = db_url
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_port = db_port
        self.dux_url = dux_url
        self.email_host = email_host
        self.email_port = email_port
        self.email_user = email_user
        self.email_password = email_password
        self.download_path = download_path
        self.dux_txt_to_sim = dux_txt_to_sim

config = Config('sistemas', 'Cocoloco', 'J:\SOLICITUD DJVE', '10.20.0.60',
                'run2', 'vots_ssl', 'Cgz6EsQ4',3306, 'http://srv-duxweb02/dux/XZS001P001.aspx',
                "mail.itservices.vaclog.com", 465, 'auto@itservices.vaclog.com','5nCWmcUGW7Dr', 
                'C:\\Users\\auto\\Downloads', "J:\\DJVE_TXT_DUX")



class Config:
    def __init__(self, dux_username, dux_password, djve_xml_path="", db_url="", db_name="", 
                db_username="", db_password="", db_port="", dux_url="" ,
                email_host="", email_port="", email_user="", email_password="", download_path="", dux_txt_to_sim=""):
        self.dux_username = dux_username
        self.dux_password = dux_password
        self.djve_xml_path = djve_xml_path
        self.db_url = db_url
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_port = db_port
        self.dux_url = dux_url
        self.email_host = email_host
        self.email_port = email_port
        self.email_user = email_user
        self.email_password = email_password
        self.download_path = download_path
        self.dux_txt_to_sim = dux_txt_to_sim

config = Config('sistemas', 'Cocoloco', 'J:\SOLICITUD DJVE', '10.20.0.60',
                'run2', 'vots_ssl', 'Cgz6EsQ4',3306, 'http://srv-duxweb02/dux/XZS001P001.aspx',
                "mail.itservices.vaclog.com", 465, 'auto@itservices.vaclog.com','5nCWmcUGW7Dr', 
                'C:\\Users\\auto\\Downloads', "J:\\DJVE_TXT_DUX")

