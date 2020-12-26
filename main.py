import requests
import time
from math import fabs
import tkinter as tk


class GUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Log Text
        self.log_frame = tk.LabelFrame(parent, text="Output", padx=5, pady=5)
        self.log_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)
        # Config Output
        self.log_text = tk.Text(self.log_frame, bd=0, width=100, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # Button Grid
        self.button_grid = tk.Frame(parent)
        self.button_grid.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # Button Config
        self.start_button = tk.Button(self.button_grid, text="Start", command=lambda: print("Running"))
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)


def min_price_fetcher(url_name):
    r = requests.get("https://api.warframe.market/v1/items/{}/orders".format(url_name))
    r_json = r.json()
    orders = r_json["payload"]["orders"]
    min = 999
    for order in orders:
        if order["order_type"] == "sell" and order["user"]["status"] == "ingame":
            if order['platinum'] < min:
                min = order['platinum']
    return min

 


def main():
    root = tk.Tk()
    root.title = "Warframe Market Parser"
    GUI(root).grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    root.mainloop()
    ck = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiI4RW42dnVNSjExenFxQXRZQWhDeURkRmZGSXlpSjVmRSIsImV4cCI6MTYxMzY4Mjg3MywiaWF0IjoxNjA4NDk4ODczLCJpc3MiOiJqd3QiLCJhdWQiOiJqd3QiLCJhdXRoX3R5cGUiOiJjb29raWUiLCJjc3JmX3Rva2VuIjoiYTQ3YzU5Njg0YmM1OGNhYmZkNmU0ZWJlYjAxMTUxNjk0MmY1ODIzZCIsInNlY3VyZSI6dHJ1ZSwibG9naW5fdWEiOiJiJ01vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS84Ny4wLjQyODAuODggU2FmYXJpLzUzNy4zNiciLCJsb2dpbl9pcCI6ImInMjYwMDoxNzAwOjYwNjA6NDA3MDpmMDUwOmE2YWU6YmIxYzphMGJiJyIsImp3dF9pZGVudGl0eSI6IlVna3paVHU5ejY5VWJVd2xpT1RWMTJPNGRtdzZLMFlQIn0.-V4iDOX2T9tcLLGhqhBEdT8o3L-BuD28HCVjdzXF16E"
    cookies = dict(JWT=ck)
    r = requests.get("https://api.warframe.market/v1/profile/notb0b/orders", cookies=cookies)
    r_json = r.json()
    my_sell_orders = r_json["payload"]["sell_orders"]
    with open("prices.csv", "w") as f:
        f.write("item name, my sell price, current low\n")
        for order in my_sell_orders:
            item_low_price = min_price_fetcher(order["item"]["url_name"])
            absolute_difference = fabs(order["platinum"] - item_low_price)
            if absolute_difference > 5.0:
                f.write(order["item"]["url_name"] + "," + str(order["platinum"]) + "," + str(
                    item_low_price) + ",price difference of " + str(absolute_difference) + "\n")
            else:
                f.write(order["item"]["url_name"] + "," + str(order["platinum"]) + "," + str(item_low_price) + "\n")
            time.sleep(.33)


if __name__ == "__main__":
    main()
