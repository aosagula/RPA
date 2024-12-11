

import mariadb
import sys
import config
import datetime

# Connect to MariaDB Platform



class Db:

    def __init__ (self, url, user, password, port, dbname):
        self.url = url
        self.user = user
        self.password = password
        self.port = port
        self.dbname = dbname


        conn_params= {
            "user" : user,
            "password" : password,
            "host" : url,
            "database" : dbname,
            "port": port
        }
        try:
            self.conn = mariadb.connect(
                **conn_params )

            self.cursor = self.conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
    def searchDjvesPendientes(self):
        try:
            self.cursor.execute("SELECT id, idsolicitud_djve, idcliente, numop, email_cliente, \
                                email_rva, fecha, hora \
                        FROM roe_verde_armado \
                        WHERE fecha >= CURDATE() - INTERVAL 30 DAY \
                          AND numop = 0 \
                          AND anulado =  0")
            
            #print(self.cursor.rowcount)
            
            #print(*row, sep=' ')
            djve_list = []
            if self.cursor.rowcount > 1:
                for table_row in self.cursor:
                    djve_list.append(table_row)
            else:
                
                row = self.cursor.fetchone()
                if row:
                    djve_list.append(row)

            #print('DJVES:' , djve_list)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
        return djve_list
    
    
    def getOperacion(self, numero_solicitud):
        try:
            print("Busncadno soli: ", numero_solicitud)
            self.cursor.execute("SELECT id, idsolicitud_djve, idcliente, numop, email_cliente, \
                                email_rva, fecha, hora \
                        FROM roe_verde_armado \
                        WHERE fecha >= CURDATE() - INTERVAL 30 DAY \
                          AND id = ? \
                          AND anulado =  0", [numero_solicitud])
            
            
            
            
                
            result = self.cursor.fetchone()[3]
             

            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
        return result

    def setEstadoTarea(self, id, estado, error_desciption=None, subestado_text=None):
        try:
            now = datetime.datetime.now()
            currentdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
            #print(estado)
            print("tarea:", id, " Estado:", estado )
            match estado:
                case 1:
                    tupla = [ 'fecha_inicio', currentdatetime]
                    query = """UPDATE robot_tarea SET 
                                    estado = %d,
                                    fecha_inicio = %s
                                WHERE id = %d
                    """
                case 2:
                    tupla = [ 'fecha_cierre', currentdatetime]
                    query = f"""UPDATE robot_tarea SET 
                                    estado = %d,
                                    fecha_cierre = %s,
                                    error_text = '{error_desciption}'
                                WHERE id = %d
                    """
                case 3:
                    tupla = [ 'fecha_error', currentdatetime]
                    query = f"""UPDATE robot_tarea SET 
                                    estado = %d,
                                    fecha_error = %s,
                                    ultimo_error = '{subestado_text}',
                                    error_text = '{error_desciption.replace("'","|")}'
                                WHERE id = %d
                    """
                case 4:
                    tupla = [ 'fecha_error', currentdatetime]
                    query = f"""UPDATE robot_tarea SET 
                                    estado = %d,
                                    fecha_error = %s,
                                    ultimo_error = '{subestado_text}',
                                    error_text = '{error_desciption.replace("'","|")}'
                                WHERE id = %d
                    """
            
            
           
            #print(query, [(estado, tupla[0], tupla[1], id)]    )
            self.cursor.execute(query, (estado, tupla[1], id) )
            self.conn.commit()
            #self.cursor.close()  
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
        return True

    def insertTarea(self, proceso, referencia, parametros):
        try:
            now = datetime.datetime.now()
            currentdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
            #print(estado)
            print("proceso:", proceso, " Referencia:", referencia )
            currentdatetime = now.strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO robot_tarea ( proceso, estado, parametros, fecha_alta, user_id, referencia) \
                        VALUES ( ?, ?, ?, ?, ?,? )"
            
            
           
            #print(query, [(estado, tupla[0], tupla[1], id)]    )
            self.cursor.execute(query, [proceso, 0, parametros, currentdatetime, "auto", referencia] )
            self.conn.commit()
            #self.cursor.close()  
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
        return True

    def getTareasPendientes(self, proceso):
        print("Obteniendo Tareas....")
        try:
            self.cursor.execute("SELECT id, proceso, parametros, \
                                        concat(auth_user.nombre, ' ', auth_user.apellido) as nomape, \
                                        robot_tarea.fecha_alta \
                                    FROM robot_tarea \
                                    LEFT JOIN auth_user ON auth_user.user_id = robot_tarea.user_id \
                                    WHERE estado IN ( 0, 3) \
                                      AND proceso IN ('fecha_plaza_proceso', 'doc_puerto_proceso') \
                                    ORDER BY fecha_alta asc")
            
            #print(self.cursor.rowcount)
            #
            #print(*row, sep=' ')
            tareas = []
            if self.cursor.rowcount >= 1:
                for table_row in self.cursor:
                    tareas.append([
                        table_row[0], #id 0
                        table_row[2], #parametros 1 
                        table_row[3], #user 2 
                        table_row[4], #fecha_alta 3
                        table_row[1]  #proceso 4
                        
                    ])
            else:
                if self.cursor.rowcount == 1:
                    row= self.cursor.fetchone()
                    tareas.append([row[0], row[2], row[3], row[4], row[1]])
                
            #print('tareas:' , tareas)
            return tareas
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
    def getTareasPendientesProc(self, proceso):
        print("Obteniendo Tareas....")
        try:
            self.cursor.execute("SELECT DISTINCT id, proceso, parametros, referencia, ultimo_error \
                                    FROM robot_tarea \
                                    WHERE estado IN ( 0, 3) \
                                      AND proceso = ? \
                                    ORDER BY fecha_alta asc", [proceso])
            
            print("tareas", self.cursor.rowcount)
            #
            #print(*row, sep=' ')
            tareas = []
            if self.cursor.rowcount >= 1:
                for table_row in self.cursor:
                    tareas.append([
                        table_row[0],
                        
                        table_row[2],
                        table_row[3],
                        table_row[4]
                    ])
            else:
                
                if self.cursor.rowcount == 1:
                    row= self.cursor.fetchone()
                    tareas.append([row[0], row[2], row[3],row[4]])
                
            #print('tareas:' , tareas)
            return tareas
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        
        




db =  Db( config.config.db_url, config.config.db_username,
         config.config.db_password, config.config.db_port,
         config.config.db_name)




