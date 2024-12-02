from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor
from docx import Document
import queue
import sv_ttk
import text_parse as tp
import abs_sum as abs
import docx_parse as docs
import pdf_parse as pdfs
import os

class MainWindow:

    standard_font_tuple = ("Malgun Gothic", 12)
    label_font_tuple = ("SunValleyBodyFont", 12)

    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.create_widgets()
        self.summary_settings = {
            "summary_length": IntVar(value=50)

        }

        abs.Abstractive().load_model_and_tokenizer()

    def open_file(self):
        file = filedialog.askopenfile(
            filetypes= [('.docx', '*.docx'),
                        ('.pdf','*.pdf'),
                        ('.txt','*.txt')], 
            mode='r'
        )

        was_read = False
        if file and file.readable():
            try:
                split = os.path.splitext(file.name)

                if split[1] == '.docx':
                    words = docs.WordDocuments(file.name).get_all_text()

                elif split[1] == '.pdf':
                    words = pdfs.Pdfs(file.name).get_all_text()

                else:
                    words = file.read()

                was_read = True
                self.text_paste.delete(1.0, END)
                self.text_paste.insert(1.0, words)

            except Exception as e:
                raise Exception(f"Error reading file: {e}")
            
            finally:
                file.close()
  
        return was_read    
        
    def start_summary_thread(self):
        self.summary_button.config(state='disabled')
        self.executor.submit(self.run_model)
        self.check_queue()

    def run_model(self):
        try:
            extractive = tp.Texts(self.text_paste.get(1.0,'end-1c')).run_extractive_summarization()        
            abstractive = abs.Abstractive(extractive).run_abstractive_summarization(
                    summary_length=self.summary_settings["summary_length"].get(),
                    profiling=False
                )
            self.queue.put(abstractive)
        except Exception as e:
            self.queue.put(f"Error during summarization: {e}")
    
    def check_queue(self):
        try:
            result = self.queue.get_nowait()

            summary = StringVar()        
            summary.set(result)

            self.text_summary['state'] = 'normal'
            self.text_summary.delete(1.0, END)      
            self.text_summary.insert(1.0, summary.get())
            self.text_summary['state'] = 'disabled'

            self.summary_button.config(state='normal')

        except queue.Empty:
            self.root.after(400, self.check_queue)

    def download_summary(self):
        try:
            self.text_summary['state'] = 'normal'
            summary = self.text_summary.get(1.0, END).strip()
            self.text_summary['state'] = 'disabled'

            file_path = filedialog.asksaveasfilename(
                title='Summarie Summary',
                defaultextension='.docx',
                filetypes=(('Word files', '*docx'),
                        ('Text files', '*.txt'),
                        ('All files', '*.*'))
            )

            if file_path:
                try:
                    if file_path.endswith('.docx'):
                        doc = Document()
                        doc.add_paragraph(summary)
                        doc.save(file_path)
                    else:
                        with open(file_path,'w', encoding='utf-8') as file:
                            file.write(summary)
                    
                    messagebox.showinfo("Success", f"Summary saved to {file_path}")
                
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file:\n{e}")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def summary_settings_popup(self):

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()

        summary_settings_window = Toplevel(self.root)
        summary_settings_window.title("Summary Settings")
        summary_settings_window.geometry("300x400")
        summary_settings_window.geometry("+%d+%d" %(root_x+900,root_y+200))
        summary_settings_window.wm_transient(self.root)

        # numeric length entry
        ttk.Label(summary_settings_window, text="Summary Length:").grid(row=2, column=0,
                                                                        padx=10, pady=10)
        numeric_entry = Entry(summary_settings_window, width=10,
                              textvariable=self.summary_settings["summary_length"])
        numeric_entry.grid(row=2, column=1)

        numeric_entry.config(validate="key", validatecommand=(self.validate_numeric, '%P'))

        # summary settings save button
        summary_save_button = ttk.Button(summary_settings_window, text="Save Summary Settings",command=lambda: self.save_summary_settings(summary_settings_window))
        summary_save_button.grid(row=5, column=0, padx=10, pady=10)
    
    def validate_numeric(self, value):
        valid = False

        if value == "" or value.isdigit():
            valid = True  

        return valid
    
    def save_summary_settings(self, summary_settings_window):
        summary_settings_window.destroy()

    def create_widgets(self):
        sv_ttk.set_theme("dark")
        self.root.title("Summarie")
        self.root.geometry("900x600")

        content = Frame(self.root)
        frame = ttk.Frame(content, borderwidth=50, relief="flat")
        content.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.grid(column=0, row=0, columnspan=10, rowspan=10,
                   sticky=(N, S, E, W))
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)     
        content.grid_columnconfigure(5, weight=1)
        content.grid_rowconfigure(2, weight=1)
        
        # frame for buttons
        button_frame = ttk.Frame(content)
        button_frame.grid(column=10, row=0, rowspan=10, sticky=(N, E, W,),
                          padx=5, pady=5)
        
        # file upload button
        file_button = ttk.Button(button_frame, text='Select File',
                                 command=self.open_file)
        file_button.grid(column=0, row=2, sticky=(N,E,W),
                         pady=5, padx=5)
        
        # summarize button
        self.summary_button = ttk.Button(button_frame,
                                    text='Summarize',
                                    command = self.start_summary_thread
                                    )
        self.summary_button.grid(column=0, row=3, sticky=(N,E,W), 
                            pady=5, padx=5)
        
        # summary save button
        summary_save_button = ttk.Button(button_frame, text='Save Summary',
                                         command = self.download_summary)
        summary_save_button.grid(column=0, row=4,sticky=(N,E,W),
                                 pady=5, padx=5)
        
        # settings button
        summary_settings_button = ttk.Button(button_frame, text='Summary Settings',
                                     command=self.summary_settings_popup)
        summary_settings_button.grid(column=0, row=5,sticky=(N,E,W),
                                     pady=5, padx=5)

        # empty labels
        blank_label = ttk.Label(content)
        blank_label_1 = ttk.Label(content)
        blank_label.grid(column=0, row=0, columnspan=10)
        blank_label_1.grid(column=0, row=10, columnspan=10)

        # text widget labels
        paste_label = ttk.Label(content, text='Enter your text here',
                                font=self.label_font_tuple)
        paste_label.grid(column=0, row=1)

        summary_label = ttk.Label(content, text="You'll see your summary here",
                                  font=self.label_font_tuple)
        summary_label.grid(column=5, row=1)
        
        # paste text widget
        self.text_paste = Text(content, wrap="word", padx=5, pady=5)
        self.text_paste.configure(font=self.standard_font_tuple)

        yscroll_paste = ttk.Scrollbar(content, orient='vertical',
                                command=self.text_paste.yview)
        yscroll_paste.grid(column=4, row=2, rowspan=8, sticky='ns')
        
        self.text_paste['yscrollcommand'] = yscroll_paste.set
        self.text_paste.grid(column=0, row=2, columnspan=4, rowspan=8,
                             sticky='nwes', padx=(5,0), pady=5)

        # summary text widget
        self.text_summary = Text(content, wrap="word", padx=5, pady=5)
        self.text_summary.configure(font=self.standard_font_tuple)

        yscroll_summary = ttk.Scrollbar(content, orient='vertical',
                                        command=self.text_summary.yview)
        yscroll_summary.grid(column=9, row=2, rowspan=8, sticky='ns')

        self.text_summary['yscrollcommand'] = yscroll_summary.set
        self.text_summary.grid(column=5, row=2, columnspan=4, rowspan=8,
                               sticky='nwes', padx=(5,0), pady=5)
        self.text_summary['state'] = 'disabled'
    
if __name__ == '__main__':
    root = Tk()
    MainWindow(root)
    root.mainloop()