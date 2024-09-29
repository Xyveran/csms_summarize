from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
#from tkinter.ttk import *

class Main:



    def validate_file():

        return True

    def open_file(self):
        file = filedialog.askopenfile(filetypes= [('.docx', '*.docx'),
                                                  ('.pdf','*.pdf'),
                                                  ('.txt','*.txt')], 
                                                  mode='r',)
        
        words = file.read()
        file.close()

        self.text_paste.delete(1.0, END)
        self.text_paste.insert(1.0, words)


        file.close
        
        
    def run_model(self):
        # code that would produce a summary string
        summary = StringVar(value="PH Summary Output from model")

        self.text['state'] = 'normal'
        self.text.delete(1.0, END)      
        self.text.insert(1.0, summary.get())
        self.text['state'] = 'disabled'

    def __init__(self, root):
    # creating main window
    
        root.title("PH app name")

        content = Frame(root)
        frame = ttk.Frame(content, borderwidth=50, relief="flat", 
                        width=900, height=600)
        content.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.grid(column=0, row=0, columnspan=10, rowspan=10, 
                sticky=(N, S, E, W))
        

        # file upload button
        file = ttk.Button(content, text='Select File', command=self.open_file)
        file.grid(column=10, row=0, sticky=(N,E,W), 
                pady=5, padx=5)
        
        # summarize button
        summary_button = ttk.Button(content, text='Summarize', 
                                    command=self.run_model)
        summary_button.grid(column=10, row=1, sticky=(N,E,W), 
                pady=5, padx=5)
        
        # paste text widget
        self.text_paste = Text(content, width=40, height=10,wrap="word", 
                        padx=5, pady=5)
        # yscroll = ttk.Scrollbar(content, orient='vertical', command=text.yview)
        # text['yscrollcommand'] = yscroll.set
        self.text_paste.insert('1.0', 'PH user paste')
        self.text_paste.grid(column=0, row=1, columnspan=5, rowspan=10, 
                        sticky='nwes', padx=5, pady=5)
        # yscroll.grid(column=9, row=4, sticky='ns')
        #content.grid_columnconfigure(0, weight=1)
        #content.grid_rowconfigure(0, weight=1)
        # the_text = t.get(1.0, END)

        # summary text widget
        self.text = Text(content, width=40, height=10,wrap="word", 
                    padx=5, pady=5)
        # yscroll = ttk.Scrollbar(content, orient='vertical', command=text.yview)
        # text['yscrollcommand'] = yscroll.set
        self.text.insert('1.0', 'PH summary output')
        self.text.grid(column=5, row=1, columnspan=5, rowspan=10, 
                sticky='nwes', padx=5, pady=5)
        self.text['state'] = 'disabled'
        # yscroll.grid(column=9, row=4, sticky='ns')
        #content.grid_columnconfigure(0, weight=1)
        #content.grid_rowconfigure(0, weight=1)
        # the_text = t.get(1.0, END)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(5, weight=1)
        content.rowconfigure(1, weight=1)
        content.rowconfigure(10, weight=1)


if __name__ == '__main__':
    # run
    root = Tk()
    Main(root)
    root.mainloop()