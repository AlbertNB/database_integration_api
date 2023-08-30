import mysql.connector

class DBManager():
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
          )
        
        self.cursor = self.conn.cursor()


    def insert_jobs(self,parameters):
        try:
            self.cursor.executemany("INSERT INTO sample_db.jobs (id, job) VALUES(%s, %s);",parameters)
            self.conn.commit()
            return {"success": True, "message":"{0} Rows Sucessfully Added".format(len(parameters))}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}

    def insert_departments(self,parameters):
        try:
            self.cursor.executemany("INSERT INTO sample_db.departments (id, department_name) VALUES(%s, %s);",parameters)
            self.conn.commit()
            return {"success": True, "message":"{0} Rows Sucessfully Added".format(len(parameters))}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}

    def insert_employees(self,parameters):
        try:
            self.cursor.executemany("INSERT INTO sample_db.hired_employees (id, name, hired_at, department_id, job_id) VALUES(%s, %s, %s, %s, %s);",parameters)
            self.conn.commit()
            return {"success": True, "message":"{0} Rows Sucessfully Added".format(len(parameters))}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}
