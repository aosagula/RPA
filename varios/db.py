

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

    def setSubidoADux(self, nro_factura):
        query = f"""UPDATE cert_origen_documentos SET 
                           subido_a_dux = 'S' 
                    WHERE nro_factura = '{nro_factura}'
                      AND anulado = 'N'
                """
        self.cursor.execute(query )
        self.conn.commit()
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
                                        robot_tarea.fecha_alta, \
                                        robot_tarea.numop \
                                    FROM robot_tarea \
                                    LEFT JOIN auth_user ON auth_user.user_id = robot_tarea.user_id \
                                    WHERE estado IN ( 0, 3) \
                                      AND proceso IN ('fecha_plaza_proceso', \
                                                      'doc_puerto_proceso', \
                                                      'certificado_origen' , \
                                                      'instruccion_embarque') \
                                    ORDER BY fecha_alta asc")
            
            #print(self.cursor.rowcount)
            #
            #print(*row, sep=' ')
            tareas = []
            if self.cursor.rowcount > 1:
                for table_row in self.cursor:
                    tareas.append([
                        table_row[0], #id 0
                        table_row[2], #parametros 1 
                        table_row[3], #user 2 
                        table_row[4], #fecha_alta 3
                        table_row[1],  #proceso 4
                        table_row[5]   #numop 5
                        
                    ])
            else:
                if self.cursor.rowcount == 1:
                    row= self.cursor.fetchone()
                    tareas.append([row[0], row[2], row[3], row[4], row[1], row[5]])
                
            #print('tareas:' , tareas)
            return tareas
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
    def getInstruccionEmbarque(self,numop ):
        try:
            self.cursor.execute("SELECT ie.idinstruccion, \
                                ie.nro_booking, \
                                ie.lugargiro_id,\
                                ie.lugargiro_nombre, \
                                ie.fecha_cutoff_documental, \
                                ie.hora_cutoff_documental, \
                                ie.fecha_cutoff_fisico, \
                                ie.hora_cutoff_fisico \
                                FROM instruccion_embarque ie WHERE numop = ?", [numop])
            #print(self.cursor.rowcount)
            #print(*row, sep=' ')
            values   = []
            row = self.cursor.fetchone()

            if row:
                column_names = [desc[0] for desc in self.cursor.description]
                values = dict(zip(column_names, row))
            else:
                values = {}  # o None, dependiendo cómo lo quieras manejar
                            
            #print('tareas:' , tareas)
            return values
            
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
        
        

    def getOperacionesRemitos(self, nro_factura):
        try:
            sentence="""SELECT  cof.nro_remito, cof.fecha_factura, cof.numop, 
                            cod.archivo as archivo_factura,
                            cod.total_factura,
                            GROUP_CONCAT(cof.certificado SEPARATOR ',') AS certificados,
                            SUM(cof.precio_unitario) as suma
                          FROM cert_origen_facturacion cof
                          JOIN cert_origen_documentos cod ON cod.nro_factura = cof.nro_factura AND cod.anulado = 'N'
                          WHERE cof.nro_factura = ?
                          AND cof.anulado = 'N'
                          GROUP BY cof.nro_remito, cof.fecha_factura, cof.numop, cod.archivo 
                          """
            
            
            with self.conn.cursor(dictionary=True) as cursor:
                cursor.execute(sentence, [nro_factura])

                table = cursor.fetchall()
                

                return table
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")


db =  Db( config.config.db_url, config.config.db_username,
         config.config.db_password, config.config.db_port,
         config.config.db_name)




