#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import datetime
import matplotlib.pyplot as plt
from getpass import getpass
import numpy as np

class appDivisas():
    #Variables para toda la clase
    email=""
    operation=""
    delivery_money=""
    delivery_currency=""
    received_money=""
    received_currency=""

    #Constructor: entra cuando llamas a una clase
    def __init__(self):
        """
        Lectura de los usuarios
        """
        csvFile = open('users.csv')  # Abrir archivo csv
        user_data = csv.reader(csvFile)  # Leer todos los registros
        next(user_data)

        self.list_user = [[]]
        for reg in user_data:
            self.list_user.append([reg[0], reg[1]])
        self.list_user.remove([])
        csvFile.close()  # Cerrar archivo
        """
        Lectura de las divisas
        """
        csvFile = open('divisas.csv')  # Abrir archivo csv
        divisas_data = csv.reader(csvFile)  # Leer todos los registros
        next(divisas_data)
        self.list_divisas = [[]]
        for reg in divisas_data:
            self.list_divisas.append([reg[0], reg[1], reg[2], reg[3], reg[4]])
        self.list_divisas.remove([])
        csvFile.close()  # Cerrar archivo
        del csvFile  # Borrar objeto

    def accesoCliente(self):
        stateAccess = False
        while not stateAccess:
            self.email = input("Email: ")
            pwd = getpass("Password: ")
            for item in self.list_user:
                if(item[0]==self.email and item[1]==pwd):
                    print("Correct access.")
                    return True
                else:
                    print("User doesn't exit, try again.")

    def mainProgram(self):
        success = False
        while not success:
            print("\n\n\n\nWelcome to ITESO bank")
            print("1. - Foreign currency exchange")
            print("2. - Currency exchange graph")
            print("3. - Exit")
            option = input("Choose an option(number): ")# Cadena de texto

            try:
                int(option)
                if(option=="1"):
                    self.getExchange()
                    self.get_ticket()
                elif(option=="2"):
                    self.getGraph()
                elif(option=="3"):
                    success = True
                else:
                    print("Option doesn't exist. Try again.")
            except Exception:
                print("Option isn't number. Try again.")

    def getGraph(self):
        names = []
        valuesBuy = []
        valuesSell = []

        for items in self.list_divisas:
            names.append(items[0])
            valuesBuy.append(int(items[3]))
            valuesSell.append(int(items[4]))

        n_groups = 4

        fig, ax = plt.subplots()

        index = np.arange(n_groups)
        bar_width = 0.35

        opacity = 0.9

        rects1 = ax.bar(index, valuesBuy, bar_width,
                        alpha=opacity, color='g',
                        label='Buy')

        rects2 = ax.bar(index + bar_width, valuesSell, bar_width,
                        alpha=opacity, color='r',
                        label='Sell')

        ax.set_xlabel('Currency')
        ax.set_ylabel('Sales')
        ax.set_title('Sales of currency')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(names)
        ax.legend()

        plt.show()


    def getExchange(self):
        success = False
        while not success:
            count = 1
            print("\n\n\n\nWelcome to ITESO bank")
            print("Currency market:")
            print("Currency \t\tBuy\tSell")
            for items in self.list_divisas:
                print("{}. {}: \t\t{}\t{}".format(count,items[0],items[1],items[2]))
                count+=1
            print("Current currency: 5 - peso")
            self.operation = input("What operation do you want to do(buy/sell)?")
            if(self.operation.lower()=="buy"):
                self.received_currency = "Peso (mxn)"
                indice = input("What currency do you want(menu number):")
                self.delivery_currency = str(self.list_divisas[int(indice)-1][0])
                self.delivery_money = input("How much do you want to have:")
                self.received_money = float(self.list_divisas[int(indice)-1][1])*int(self.delivery_money)
                print("Total: " + str(self.received_money))
                new = int(self.list_divisas[int(indice)-1][3])+int(self.delivery_money)
                self.list_divisas[int(indice) - 1][3] = str(new)
                success = True
                self.update_files()
            elif(self.operation.lower()=="sell"):
                self.delivery_currency = "Peso (mxn)"
                indice = input("What currency do you have(menu number):")
                self.received_currency = str(self.list_divisas[int(indice)-1][0])
                self.received_money = input("How much do you want to exchange:")
                self.delivery_money = float(self.list_divisas[int(indice)-1][2])*int(self.received_money)
                print("Total: " + str(self.delivery_money))
                new = int(self.list_divisas[int(indice)-1][4])+int(self.received_money)
                self.list_divisas[int(indice) - 1][4] = str(new)
                success = True
                self.update_files()
            else:
                print("Doesn't exist this operation. Try again")
        print("Success. Print ticket.")

    def update_files(self):
        csvsalida = open('divisas.csv', 'w', newline='')
        salida = csv.writer(csvsalida)
        salida.writerow(['Divisas', 'Compra', 'Venta', 'no. compra', 'no. venta'])
        for items in self.list_divisas:
            salida.writerow([items[0], items[1], items[2], items[3], items[4]])
        del salida
        csvsalida.close()

    def get_ticket(self):
        file = open("ticket.txt", "w")
        file.write("ITESO bank\n\n")
        file.write("Cliente: {}\n".format(self.email))
        file.write("Operation: {}\n\n".format(self.operation))
        if(self.operation.lower()=="sell"):
            file.write("Received: {}\n".format(self.received_money))
            file.write("Currency: {}\n".format(self.received_currency))
            file.write("Delivery: {}\n".format(self.delivery_money))
            file.write("Currency: {}\n\n".format(self.delivery_currency))
        elif(self.operation.lower()=="buy"):
            file.write("Delivery: {}\n".format(self.delivery_money))
            file.write("Currency: {}\n".format(self.delivery_currency))
            file.write("Received: {}\n".format(self.received_money))
            file.write("Currency: {}\n\n".format(self.received_currency))
        file.write("Date: {}\n".format(datetime.datetime.now().strftime("%x")))
        file.write("Hour: {}".format(datetime.datetime.now().strftime("%X")))
        file.close()




