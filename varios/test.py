import smtp
list = ['alejandro.sagula@gmail.com', 'alejandro.sagula@hotmail.com','itrva@vaclog.com']
tos='itrva@vaclog.com,hbariain@vaclog.com'
smtp.smtp.SendMail(tos.split(','), 'Prueba', "OK", "OK")



    