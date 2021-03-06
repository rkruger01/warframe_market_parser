import configparser
import requests
import time
from math import fabs
import tkinter as tk


class GUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title = "Warframe Market Price Fetcher"
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
        self.start_button = tk.Button(self.button_grid, text="Start", command=lambda: price_comparer(self))
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)


def min_price_fetcher(url_name):
    r = requests.get("https://api.warframe.market/v1/items/{}/statistics".format(url_name))
    r_json = r.json()
    min = r_json["payload"]["statistics_live"]["48hours"][len(r_json["payload"]["statistics_live"]["48hours"]) - 1]["min_price"]
    return min


def price_comparer(gui):
    gui_text_log = gui.log_text
    gui_text_log.delete('1.0', tk.END)
    gui_text_log.config(state=tk.NORMAL)
    gui_text_log.insert(tk.END, "Printing prices to prices.csv\n")
    config = configparser.ConfigParser()
    config.read("config.txt")
    uname = config['Default']['username']
    difference_threshold = config['Default']['threshold']
    ck = config['Default']['cookie']
    cookies = dict(JWT=ck)
    gui_text_log.insert(tk.END, "Fetching orders for {}\n".format(uname))
    gui_text_log.insert(tk.END, "Using price difference threshold of {} platinum\n".format(difference_threshold))
    r = requests.get("https://api.warframe.market/v1/profile/{}/orders".format(uname), cookies=cookies)
    r_json = r.json()
    my_sell_orders = r_json["payload"]["sell_orders"]
    gui_text_log.tag_config("warning", foreground="red")
    with open("prices.csv", "w") as f:
        header = "item name, my sell price, current low\n"
        gui_text_log.insert(tk.END, header)
        f.write(header)
        for order in my_sell_orders:
            item_low_price = min_price_fetcher(order["item"]["url_name"])
            absolute_difference = fabs(order["platinum"] - item_low_price)
            if absolute_difference > float(difference_threshold):
                result_no_price_difference = order["item"]["en"]["item_name"] + ",\t" + str(
                    order["platinum"]) + ",\t" + str(
                    item_low_price) + ",\t"
                price_difference = "price difference of " + str(absolute_difference) + "\n"
                f.write(result_no_price_difference + price_difference)
                gui_text_log.insert(tk.END, result_no_price_difference)
                gui_text_log.insert(tk.END, price_difference, "warning")
            else:
                result = order["item"]["en"]["item_name"] + ",\t" + str(order["platinum"]) + ",\t" + str(
                    item_low_price) + "\n"
                f.write(result)
                gui_text_log.insert(tk.END, result)
            gui.update()
            time.sleep(.33)  # to comply with warframe.market API access frequency guidelines
    gui_text_log.insert(tk.END, "Done\n")
    gui_text_log.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    window_gui = GUI(root)
    window_gui.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    root.mainloop()


if __name__ == "__main__":
    main()
