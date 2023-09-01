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

    def query_1(self, year):
        query = """
            SELECT d.department_name,
            	j.job, 
            	COUNT(CASE WHEN QUARTER(hired_at) = 1 THEN 1 ELSE 0 END) AS Q1,
            	COUNT(CASE WHEN QUARTER(hired_at) = 2 THEN 1 ELSE 0 END) AS Q2,
            	COUNT(CASE WHEN QUARTER(hired_at) = 3 THEN 1 ELSE 0 END) AS Q3,
            	COUNT(CASE WHEN QUARTER(hired_at) = 4 THEN 1 ELSE 0 END) AS Q4
            FROM hired_employees AS he
            LEFT JOIN departments AS d
            ON he.department_id = d.id 
            LEFT JOIN jobs AS j
            ON he.job_id = j.id 
            WHERE YEAR(hired_at) = %s
            GROUP BY 1,2
            ORDER BY 1,2;
        """

        self.cursor.execute(query,(year,))
        return self.cursor.description, self.cursor.fetchall()

    def query_2(self, year):
        query = """
            WITH hired_by_departments AS(
                SELECT d.id,
                    d.department_name,
                    COUNT(*) AS hired
                FROM hired_employees AS he
                LEFT JOIN departments AS d
                ON he.department_id = d.id
                WHERE YEAR(hired_at) = %s
                GROUP BY 1,2

            ),

            most_hiring_departments AS (
                SELECT id,
                    department_name,
                    hired
                FROM hired_by_departments
                WHERE hired > (SELECT AVG(hired) FROM hired_by_departments)

            )

            SELECT * FROM most_hiring_departments;
        """

        self.cursor.execute(query,(year,))
        return self.cursor.description, self.cursor.fetchall()


    def insert_jobs(self,parameters):
        try:
            self.cursor.executemany("INSERT IGNORE INTO sample_db.jobs (id, job) VALUES(%s, %s);",parameters)
            self.conn.commit()
            return {"success": True, "message":"Batch Sucessfully Added Ignoring Duplicates"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}

    def insert_departments(self,parameters):
        try:
            self.cursor.executemany("INSERT IGNORE INTO sample_db.departments (id, department_name) VALUES(%s, %s);",parameters)
            self.conn.commit()
            return {"success": True, "message":"Batch Sucessfully Added Ignoring Duplicates"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}

    def insert_employees(self,parameters):
        try:
            self.cursor.executemany("INSERT IGNORE INTO sample_db.hired_employees (id, name, hired_at, department_id, job_id) VALUES(%s, %s, %s, %s, %s);",parameters)
            self.conn.commit()
            return {"success": True, "message":"Batch Sucessfully Added Ignoring Duplicates"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}

    def truncate_employees(self):
        try:
            self.cursor.execute("TRUNCATE TABLE sample_db.hired_employees;")
            self.conn.commit()
            return {"success": True, "message":"Table 'hired_employees' Sucessfully Truncated"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}

    def truncate_departments(self):
        try:
            self.cursor.execute("TRUNCATE TABLE sample_db.departments;")
            self.conn.commit()
            return {"success": True, "message":"Table 'departments' Sucessfully Truncated"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}

    def truncate_jobs(self):
        try:
            self.cursor.execute("TRUNCATE TABLE sample_db.jobs;")
            self.conn.commit()
            return {"success": True, "message":"Table 'jobs' Sucessfully Truncated"}
        except Exception as e:
            self.conn.rollback()
            return {"success": False, "message":str(e)}