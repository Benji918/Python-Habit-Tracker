import requests
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import webbrowser
from tkcalendar import *
import os


class Pixela:
    def __init__(self, username, token):
        self.graph = None
        self.graph_id = 'testgraph001'
        self.username = username
        self.token = token
        self.header = {"X-USER-TOKEN": self.token}
        self.url = ' https://pixe.la/v1/users'
        # self.today = self.get_today()
        self.create_user()
        self.create_graph(graph_name='ojfdofjojf')

        # GUI
        self.window = Tk()
        self.window.title('Coding Habit Tracker')
        self.window.resizable(width=False, height=False)
        self.window.config(pady=20, padx=20)
        URL = f'https://pixe.la/v1/users/{self.username}/graphs/{self.graph_id}.html'
        TODAY = datetime.today()

        def open_browser():
            webbrowser.open(url=URL, new=1)

        # elements
        self.cal = Calendar(self.window, selectmode="day", year=TODAY.year, month=TODAY.month, day=TODAY.day)
        self.cal.config(date_pattern="yyyyMMdd")
        self.date = self.cal.get_date()
        self.cal.config(date_pattern="yyyy/MM/dd")
        # print(self.date)
        self.cal.grid(row=0, column=0, columnspan=4)

        units = Label(text="Hours/Day:")
        units.grid(row=1, column=0, columnspan=2, pady=10, sticky="e")

        self.user_in = Entry(width=10)
        self.user_in.grid(row=1, column=2, sticky="w")

        self.add = Button(text="Add", command=self.post_pixel)
        self.add.grid(row=2, column=0, pady=10, )

        self.update = Button(text="Update", command=self.update_pixel)
        self.update.grid(row=2, column=1, pady=10, sticky="w")

        self.delete = Button(text="Delete", command=self.delete_pixel)
        self.delete.grid(row=2, column=2, pady=10, sticky="w")

        link = Button(text="Show\nJourney", command=open_browser)
        link.grid(row=2, column=3)

        self.window.mainloop()

    def create_user(self):
        url = self.url
        user_param = {
            'token': self.token,
            'username': self.username,
            'agreeTermsOfService': 'yes',
            'notMinor': 'yes'
        }

        response = requests.post(url=url, json=user_param, headers=self.header)
        if response.status_code == 200:
            messagebox.showinfo(title='User info', message='User Successfully Created')
            return True
        else:
            print(response.text)

    #
    # def get_today(self) -> str:
    #     """
    #     Grab today as a string in yyyyMMdd format
    #     :return: today.strftime('%Y%m%d')
    #     """
    #     today = datetime.today()
    #     return today.strftime('%Y%m%d')

    def create_graph(self, graph_name, unit='Hours', type_format='float', color='sora'):
        create_graph_url = f'{self.url}/{self.username}/graphs'
        self.graph = graph_name
        graph_config = {
            "id": self.graph_id,
            "name": self.graph,
            "unit": unit,
            "type": type_format,
            "color": color,
        }

        response = requests.post(url=create_graph_url, json=graph_config, headers=self.header)
        if response.status_code == 200:
            messagebox.showinfo(title='Graph info', message='Graph Successfully Created')
            return True
        else:
            print(response.text)

    def post_pixel(self):
        """
           Given a quantity of units
           Post a that quantity of pixels to the graph
        """
        # if date is None:
        #     date = self.today

        url = f'{self.url}/{self.username}/graphs/{self.graph_id}'
        post_config = {
            'date': self.date,
            'quantity': self.user_in.get()
        }
        response = requests.post(url=url, json=post_config, headers=self.header)
        if response.status_code == 200:
            messagebox.showinfo(title='Data info', message='Data Successfully Sent')
            return True
        else:
            print(response.text)

    def update_pixel(self):
        """
           Given a date in yyyyMMdd format and a quantity
           Update that date's pixel for that many quantities
        """
        # if date is None:
        #     date = self.today

        url = f'{self.url}/{self.username}/graphs/{self.graph_id}/{self.date}'

        update_config = {
            'quantity': self.user_in.get()
        }

        response = requests.put(url=url, json=update_config, headers=self.header)
        if response.status_code == 200:
            messagebox.showinfo(title='Update info', message='Data Successfully Updated')
            return True
        else:
            print(response.text)

    def delete_pixel(self):
        """
           Given a date
           Delete the pixel from that date
        """
        # if date is None:
        #     date = self.today

        url = f'{self.url}/{self.username}/graphs/{self.graph_id}/{self.date}'

        response = requests.delete(url=url, headers=self.header)
        if response.status_code == 200:
            messagebox.showinfo(title='User info', message='Data Successfully Deleted')
            return True
        else:
            print(response.text)

    def delete_user(self):

        url = f'{self.url}/{self.username}'
        response = requests.delete(url=url, headers=self.header)
        if response.status_code == 200:
            print('User Deleted!!!')
            return True
        else:
            print(response.text)


pix = Pixela(username=os.environ['NEW_USERNAME'], token=os.environ['NEW_TOKEN'])
