import tkinter as tk, asyncio, threading
from ARCScraping import ARCScraping
from tkinter import filedialog
import os

class WebScraperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Virginia Tech Applied Research Corpartion: Web Scraper")
        
        # Create input file selection button
        self.input_label = tk.Label(self.master, text="Input File:")
        self.input_label.pack()
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.master, textvariable=self.input_var)
        self.input_entry.pack()
        self.input_button = tk.Button(self.master, text="Select File", command=self.select_input_file)
        self.input_button.pack()
        
        # Create process button
        self.process_button = tk.Button(self.master, text="Process", command=self.process_thread)
        self.process_button.pack()
    
        #Running label
        self.running_label = tk.Label(self.master, text="Not Running.", borderwidth=2, relief="groove")
        self.running_label.pack()


    def select_input_file(self):
        input_path = tk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if input_path:
            self.input_path = input_path
            self.input_var.set(self.input_path)
    

    '''
    Prevents thread from freezing in background.
    '''
    def process_thread(self):
        self.running_label.config(text="Running...")
        self.process_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.process_async)
        thread.start()


    def reset_running_label(self):
        # update the label text with the result
        self.running_label.config(text="Done running!")

        # re-enable the button
        self.process_button.config(state=tk.NORMAL)


    def process_async(self):
        loop = asyncio.get_event_loop()
        print("here")
        task = loop.create_task(self.process_csv())
        loop.run_forever(task)
        print("after")
        self.master.after(0, lambda: self.update_gui())


    async def process_csv(self):
        print("Starting the Scraper...")
        arc = ARCScraping(self.input_path)
        await arc.run()


def main():
    root = tk.Tk()
    root.geometry("400x200")
    print("Here")

    icon = tk.PhotoImage(file="data/VTARClogo.png")
    # set the icon of the window to the photo image
    root.iconphoto(True, icon)

    app = WebScraperGUI(root)
    root.mainloop()

asyncio.run(main())