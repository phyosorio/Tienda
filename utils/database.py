# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 00:37:23 2020

@author: phyos
"""


import time
from database_conection import DatabaseConection

def create_table():
    with DatabaseConection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS items(idItem INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, cost FLOAT, UNIQUE(name))')
        cursor.execute('CREATE TABLE IF NOT EXISTS sales(idSales INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date DATETIME, idTicket INT NOT NULL, total FLOAT, FOREIGN KEY (idTicket) REFERENCES tickets(idTicket))')
        cursor.execute('CREATE TABLE IF NOT EXISTS tickets(idTicket INT NOT NULL,idItem INT, qty FLOAT, subtotal FLOAT)')
create_table()

    

def add_product():
    nameItem = input("Producto: ").capitalize()
    costItem = input("Costo por kg: ")
    with DatabaseConection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO items (name,cost) VALUES(?,?)',(nameItem,costItem))
    


def new_ticket():
    t_items = []
    t_qty = []
    t_subt = []
    with DatabaseConection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM items')
        items = [{'idItem':row[0], 'name':row[1], 'cost':row[2]} for row in cursor.fetchall()]
    articles = 0
    if articles ==0:
        with DatabaseConection('data.db') as connection:
            cursor = connection.cursor()
            try:
                cursor.execute('SELECT idTicket FROM tickets ORDER BY idTicket DESC LIMIT 1')
                tmp = cursor.fetchone()[0]
                idticket = tmp+1
            except:
                idticket = 1
        hour =time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Fecha:{hour}\n\n\t Ticket: {idticket}")
    USER_CHOISE = input("Inserte el ID del producto para agregar un nuevo producto o 'q' para finalizar: ")
    
    while USER_CHOISE != 'q':
        try:
            
            
            
            itm = next(item for item in items if item["idItem"] == int(USER_CHOISE))
            
            t_items.append(itm["idItem"])
            qty = float(input(f"Producto: {itm['name']}, Cantidad: "))
            t_qty.append(qty)
            
            t_subt.append(qty*itm["cost"])
            articles +=1
            print(f"Precio por kg ${itm['cost']}, precio por cantidad: ${qty*itm['cost']}")
            print(f"Numero de articulos: {articles}")
            USER_CHOISE = input("Inserte el ID del producto para agregar un nuevo producto o 'q' para finalizar: ")
        except:
            USER_CHOISE = input("El producto seleccionado no existe, intente de nuevo: Inserte el ID del producto para agregar un nuevo producto o 'q' para finalizar: ")
        
    idticket = [idticket for n in t_items]
    with DatabaseConection('data.db') as connection:
        cursor = connection.cursor()
        instruccion = "INSERT INTO tickets (idTicket,idItem, qty,subtotal) VALUES (?,?,?,?)"
        a = list(zip(idticket, t_items, t_qty, t_subt))
        cursor.executemany(instruccion,a)
    if articles>0:
        print(f"Numero de articulos: {articles}, total: ${sum(t_subt)}")
        new_sale(idticket[0],sum(t_subt), hour)

def new_sale(idticket, total, hour):
    with DatabaseConection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO sales (date, idTicket, total) VALUES(?,?,?)', (hour ,idticket,total))
        


new_ticket()

#agregar producto
#eliminar producto
#modificar producto
#crear ticket
#agregar elementos al ticket