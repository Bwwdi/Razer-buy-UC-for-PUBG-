import sqlite3 as sql
class Data_base:
    def __init__(self):
        self.con = sql.connect("Razer.db")
        self.cur = self.con.cursor()
        table_users = 'CREATE TABLE IF NOT EXISTS User(id INTEGER PRIMARY KEY,Name Text,time_subscribe INT)'
        self.cur.execute(table_users)
        print("Бд активна")
        self.con.commit()


    def Set_new_user(self,user_id,Name):
        action = """INSERT OR IGNORE INTO User(id,Name,time_subscribe) VALUES(?,?,?)"""
        self.cur.execute(action,[user_id,Name,0])
        self.con.commit()


    def Set_new_subscribe(self,username,time_subscribe):
        try:
            action = """Update User set time_subscribe = ? WHERE Name = ?"""
            self.cur.execute(action, [time_subscribe,username])
            self.con.commit()
            return True
        except:
            return False


    def Take_subscribe(self,username):
        try:
            action = """Update User set time_subscribe = ? WHERE Name = ?"""
            self.cur.execute(action, [0, username])
            self.con.commit()
            return True
        except:
            return False


    def check_subscribe(self,username,now_time):
        action = """SELECT time_subscribe from User WHERE Name = ?"""
        self.cur.execute(action,[username])
        time=self.cur.fetchone()[0]
        if now_time>time:
            return False
        else:
            return True


    # def get_new_order(self,number):
    #     try:
    #         data_number=int(number)-1
    #         action = """SELECT * from New_Orders"""
    #         self.cur.execute(action)
    #         Base=self.cur.fetchall()
    #         Data = Base[data_number]
    #         text=(f"""Описание:{Data[1]}\nДата:{Data[2]}\nЦена:{Data[3]}\nСсылка для связи:{Data[4]}""")
    #         return text
    #     except:
    #         return f"№{number}-В этой ячейке нет заказов."
    #
    # def get_active_order(self,number):
    #     try:
    #         data_number=int(number)-1
    #         action = """SELECT * from Active_Orders"""
    #         self.cur.execute(action)
    #         Base=self.cur.fetchall()
    #         Data = Base[data_number]
    #         text=(f"""Описание:{Data[1]}\nДата:{Data[2]}\nЦена:{Data[3]}\nПрогресс:{Data[6]}\nСсылка для связи:{Data[7]}""")
    #         return text
    #     except:
    #         return f"№{number}-В этой ячейке нет заказов."
    #
    #
    # def set_new_order(self,user_id,description,date,money,Name):
    #     action= 'INSERT INTO New_Orders(id,description,date,money,name) VALUES(?, ?, ?, ?, ?)'
    #     self.cur.execute(action,[user_id,description,date,money,f"t.me/{Name}"])
    #     self.con.commit()
    #     action="""SELECT * from New_Orders"""
    #     self.cur.execute(action)
    #     orders_value=len(self.cur.fetchall())
    #     self.con.commit()
    #     text=f"""Новый заказ №-{orders_value}."""
    #     return  text
    #
    # def Complete_order(self,number):
    #     data_number = int(number) - 1
    #     action = """SELECT * from Active_Orders"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     Data = Base[data_number]
    #     return Data
    #
    #
    # def new_order_to_active_order(self,number):
    #     data_number = int(number) - 1
    #     action = """SELECT * from New_Orders"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     Data = Base[data_number]
    #     self.con.commit()
    #     action_d = 'INSERT INTO Active_Orders(id,description,date,money,Name) VALUES(?, ?, ?, ?, ?)'
    #     self.cur.execute(action_d, [Data[0], Data[1], Data[2], Data[3], Data[4]])
    #     self.con.commit()
    #     action = """DELETE from New_Orders where id = ?"""
    #     self.cur.execute(action, [Data[0]])
    #     self.con.commit()
    #     return Data
    #
    #
    # def Denied_new_order(self,number):
    #     data_number = int(number) - 1
    #     action = """SELECT * from New_Orders"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     Data = Base[data_number]
    #     self.con.commit()
    #     action_d = 'INSERT INTO Base_Orders(id,description,date,money,cause,Name) VALUES(?, ?, ?, ?, ?, ?)'
    #     self.cur.execute(action_d, [Data[0], Data[1], Data[2], Data[3],"Denied",Data[7]])
    #     self.con.commit()
    #     action="""DELETE from New_Orders where id = ?"""
    #     self.cur.execute(action,[Data[0]])
    #     self.con.commit()
    #     return Data
    #
    #
    # def Refuse_active_order(self,number):
    #     data_number = int(number) - 1
    #     action = """SELECT * from Active_Orders"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     Data = Base[data_number]
    #     self.con.commit()
    #     action_d = 'INSERT INTO Base_Orders(id,description,date,money,cause,Name) VALUES(?, ?, ?, ?, ?, ?)'
    #     self.cur.execute(action_d, [Data[0], Data[1], Data[2], Data[3], "Refuse",Data[7]])
    #     self.con.commit()
    #     action = """DELETE from Active_Orders where id = ?"""
    #     self.cur.execute(action, [Data[0]])
    #     self.con.commit()
    #     return Data
    #
    #
    # def Complete_active_order(self, user_id):
    #     action = """SELECT * FROM Active_Orders WHERE id = ?"""
    #     self.cur.execute(action,[user_id])
    #     Data = self.cur.fetchone()
    #     self.con.commit()
    #     action_d = 'INSERT INTO Base_Orders(id,description,date,money,cause,File,invoice_id,Name) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
    #     self.cur.execute(action_d, [Data[0], Data[1], Data[2], Data[3],"Complete",Data[4],Data[5],Data[7]])
    #     self.con.commit()
    #     action = """DELETE from Active_Orders where id = ?"""
    #     self.cur.execute(action, [Data[0]])
    #     self.con.commit()
    #     return Data
    #
    # def get_count_new_orders(self):
    #     action="""SELECT * from New_Orders"""
    #     self.cur.execute(action)
    #     count=len(self.cur.fetchall())
    #     return count
    #
    #
    # def get_count_active_orders(self):
    #     action="""SELECT * from Active_Orders"""
    #     self.cur.execute(action)
    #     count=len(self.cur.fetchall())
    #     return count
    #
    # def get_id_active_orders(self,number):
    #     data_number = int(number) - 1
    #     action = """SELECT * from Active_Orders"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     Data = Base[data_number]
    #     return Data
    #
    #
    # def check_New_order(self, user_id):
    #     query = 'SELECT * FROM New_Orders WHERE id = ? '
    #     result = self.cur.execute(query, (user_id,)).fetchall()
    #     return bool(len(result))
    #
    #
    # def add_admin(self,user_id,name):
    #     action="INSERT OR IGNORE INTO admins(id,Name) VALUES(?,?)"
    #     self.cur.execute(action,[user_id,name])
    #     self.con.commit()
    #     return "Пользователь успешно добавлен в админы"
    #
    #
    # def set_file_id(self,number,file_id):
    #     data_number = int(number) - 1
    #     action = """SELECT * from Active_Orders"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     Data = Base[data_number]
    #     ide = int(Data[0])
    #     self.con.commit()
    #     action_d = f"""Update Active_Orders set File = ? WHERE id = ?"""
    #     self.cur.execute(action_d,[file_id,ide])
    #     self.con.commit()
    #
    # def check_admin_user(self, user_id):
    #     query = 'SELECT id FROM admins WHERE id = ? '
    #     result = self.cur.execute(query, [user_id]).fetchall()
    #     return bool(len(result))
    #
    #
    # def set_invoice_id(self,id,invoice):
    #     action = """Update Active_Orders set invoice_id = ? WHERE id = ?"""
    #     self.cur.execute(action,[invoice,id])
    #     self.con.commit()
    #
    #
    # def set_progress(self,id,prog):
    #     action = """Update Active_Orders set Progress = ? WHERE id = ?"""
    #     self.cur.execute(action,[f'{prog}%',id])
    #     self.con.commit()
    #
    #
    # def get_invoice_id(self,id):
    #     action = "SELECT invoice_id FROM Active_Orders WHERE id = ?"
    #     data=self.cur.execute(action,[id]).fetchone()
    #     self.con.commit()
    #     return data[0]
    #
    #
    # def get_progress(self,id):
    #     action = "SELECT Progress FROM Active_Orders WHERE id = ?"
    #     data = self.cur.execute(action, [id]).fetchone()
    #     self.con.commit()
    #     return data[0]
    #
    #
    # def Edit_new_order(self,ID,value,set):
    #         action = f"""Update New_Orders set {set} = ? WHERE id = ?"""
    #         self.cur.execute(action, [value, ID])
    #         self.con.commit()
    #
    #
    # def get_base_orders(self, number):
    #     data_number = int(number) - 1
    #     action = """SELECT * from Base_Orders"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     Data = Base[data_number]
    #     return Data
    #
    #
    # def get_text_base_orders(self,number):
    #     try:
    #         data_number=int(number)-1
    #         action = """SELECT * from Base_Orders"""
    #         self.cur.execute(action)
    #         Base=self.cur.fetchall()
    #         Data = Base[data_number]
    #         return f"""№{number}\nID:{Data[0]}\nОписание:{Data[1]}\nДата:{Data[2]}\nЦена:{Data[3]}\nИтог:{Data[4]}\nСсылка для связи:{Data[7]}"""
    #     except:
    #         return f"№{number}-В этой ячейке нет заказов."
    #
    #
    # def get_admins_base(self):
    #     action="""SELECT * from admins"""
    #     self.cur.execute(action)
    #     Base = self.cur.fetchall()
    #     return Base
    #
    #
    # def delete_admin(self,ID):
    #     action = """DELETE from admins where id = ?"""
    #     self.cur.execute(action, [ID])
    #     self.con.commit()
