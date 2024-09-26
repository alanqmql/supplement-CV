import tkinter as tk
from tkinter import messagebox, filedialog, Label
from datetime import datetime
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import os
from PIL import Image, ImageTk
import networkx as nx  
from travel_debt_graph import TravelDebtGraph

matplotlib.use('TkAgg')

class DebtApp:
    def __init__(self, root):
        self.graph = TravelDebtGraph()
        self.data_file = os.path.join(os.path.expanduser("~"), 'debt_data.json')
        self.graph.load_data(self.data_file)
        self.setup_ui(root)

    def setup_ui(self, root):
        self.root = root
        self.root.title("Mickey DebtTracker 美记钱庄 group11")
        self.create_main_frame()
        self.create_add_person_frame()
        self.create_record_debt_frame()
        self.create_second_record_debt_frame()
        self.create_buttons()
        self.create_debt_listbox()
        self.create_image_frame()
        self.create_bottom_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.graph_window = None

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def create_add_person_frame(self):
        self.add_person_frame = tk.Frame(self.main_frame)
        self.add_person_frame.pack(fill="x", pady=5)
        self.add_person_label = tk.Label(self.add_person_frame, text="Add Person:")
        self.add_person_label.pack(side="left")
        self.add_person_entry = tk.Entry(self.add_person_frame)
        self.add_person_entry.pack(side="left", padx=5)
        self.add_person_button = tk.Button(self.add_person_frame, text="Add", command=self.add_person)
        self.add_person_button.pack(side="left")

    def create_record_debt_frame(self):
        self.record_debt_frame = tk.Frame(self.main_frame)
        self.record_debt_frame.pack(fill="x", pady=5)
        self.record_debt_label = tk.Label(self.record_debt_frame, text="Record Debt:")
        self.record_debt_label.pack(side="left")

        self.date_label = tk.Label(self.record_debt_frame, text="Date:")
        self.date_label.pack(side="left")
        self.date_entry = tk.Entry(self.record_debt_frame, width=10)
        self.date_entry.pack(side="left", padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.description_label = tk.Label(self.record_debt_frame, text="Description:")
        self.description_label.pack(side="left")
        self.description_entry = tk.Entry(self.record_debt_frame, width=15)
        self.description_entry.pack(side="left", padx=5)

    def create_second_record_debt_frame(self):
        self.second_row_frame = tk.Frame(self.main_frame)
        self.second_row_frame.pack(fill="x", pady=5)
        
        self.from_person_label = tk.Label(self.second_row_frame, text="Person in debt:")
        self.from_person_label.pack(side="left", padx=(20, 0))
        self.from_persons_text = tk.Text(self.second_row_frame, height=3, width=20)
        self.from_persons_text.pack(side="left", padx=5)

        self.to_person_label = tk.Label(self.second_row_frame, text="Creditor:")
        self.to_person_label.pack(side="left", padx=(20, 0))
        self.to_person_entry = tk.Entry(self.second_row_frame, width=10)
        self.to_person_entry.pack(side="left", padx=5)

        self.amount_label = tk.Label(self.second_row_frame, text="Amount:")
        self.amount_label.pack(side="left", padx=(20, 0))
        self.amount_entry = tk.Entry(self.second_row_frame, width=10)
        self.amount_entry.pack(side="left", padx=5)

        self.split_method = tk.StringVar(value="custom")
        self.split_custom = tk.Radiobutton(self.second_row_frame, text="Custom Split", variable=self.split_method, value="custom", command=self.update_amount_entry)
        self.split_custom.pack(side="left")
        self.split_equal = tk.Radiobutton(self.second_row_frame, text="Equal Split", variable=self.split_method, value="equal", command=self.update_amount_entry)
        self.split_equal.pack(side="left")

        self.record_debt_button = tk.Button(self.second_row_frame, text="Record", command=self.record_debt)
        self.record_debt_button.pack(side="left")

    def create_buttons(self):
        self.view_debts_button = tk.Button(self.main_frame, text="View Debts", command=self.view_debts)
        self.view_debts_button.pack(fill="x", pady=5)

        self.view_net_debts_button = tk.Button(self.main_frame, text="View Net Debts", command=self.view_net_debts)
        self.view_net_debts_button.pack(fill="x", pady=5)

        self.view_records_button = tk.Button(self.main_frame, text="View Records", command=self.view_records)
        self.view_records_button.pack(fill="x", pady=5)

        self.graph_button = tk.Button(self.main_frame, text="Graph", command=self.show_graph)
        self.graph_button.pack(fill="x", pady=5)

        self.upload_button = tk.Button(self.main_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(fill="x", pady=5)

    def create_debt_listbox(self):
        self.debt_listbox = tk.Text(self.main_frame, width=80, height=15)
        self.debt_listbox.pack(pady=5, fill="both", expand=True)

    def create_image_frame(self):
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(pady=5)

    def create_bottom_frame(self):
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(side="bottom", fill="x", pady=5)

        self.undo_record_button = tk.Button(self.bottom_frame, text="Undo Last Record", command=self.undo_last_record)
        self.undo_record_button.pack(side="right", padx=5)

        self.clear_records_button = tk.Button(self.bottom_frame, text="Clear All Records", command=self.clear_all_records)
        self.clear_records_button.pack(side="right", padx=5)

    def update_amount_entry(self):
        if self.split_method.get() == "equal":
            self.amount_entry.config(state="normal")
        else:
            self.amount_entry.config(state="disabled")

    def add_person(self):
        name = self.add_person_entry.get()
        if " " in name:
            messagebox.showwarning("Input Error", "Name cannot contain spaces.")
            return
        if name:
            self.graph.add_person(name)
            messagebox.showinfo("Success", f"Added person: {name}")
            self.add_person_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a name.")

    def record_debt(self):
        date = self.date_entry.get()
        description = self.description_entry.get()
        to_person = self.to_person_entry.get()
        from_persons_data = self.from_persons_text.get("1.0", tk.END).strip().split("\n")
        amount = self.amount_entry.get()

        if " " in to_person:
            messagebox.showwarning("Input Error", "Name cannot contain spaces.")
            return

        if self.split_method.get() == "equal":
            self.handle_equal_split(from_persons_data, to_person, amount, date, description)
        elif self.split_method.get() == "custom":
            self.handle_custom_split(from_persons_data, to_person, date, description)

    def handle_equal_split(self, from_persons_data, to_person, amount, date, description):
        try:
            amount = float(amount)
            if from_persons_data and to_person:
                total_persons = len(from_persons_data) + 1
                individual_amount = amount / total_persons
                for from_person in from_persons_data:
                    if " " in from_person:
                        messagebox.showwarning("Input Error", "Name cannot contain spaces.")
                        return
                    self.graph.record_debt(from_person, to_person, individual_amount, date, description)
                messagebox.showinfo("Success", f"Recorded debt: {', '.join(from_persons_data)} owe {to_person}")
                self.clear_form()
            else:
                messagebox.showwarning("Input Error", "Please enter valid names and amounts.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount.")

    def handle_custom_split(self, from_persons_data, to_person, date, description):
        try:
            if from_persons_data and to_person:
                for from_person_data in from_persons_data:
                    parts = from_person_data.split()
                    if len(parts) != 2:
                        messagebox.showwarning("Input Error", "Please enter name and amount separated by a space.")
                        return
                    from_person, individual_amount = parts
                    individual_amount = float(individual_amount)
                    self.graph.record_debt(from_person, to_person, individual_amount, date, description)
                messagebox.showinfo("Success", f"Recorded debt: {', '.join([fp.split()[0] for fp in from_persons_data])} owe {to_person}")
                self.clear_form()
            else:
                messagebox.showwarning("Input Error", "Please enter valid names and amounts.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount.")

    def clear_form(self):
        self.to_person_entry.delete(0, tk.END)
        self.from_persons_text.delete("1.0", tk.END)
        self.amount_entry.delete(0, tk.END)
        if hasattr(self, 'image_label'):
            self.image_label.destroy()

    def undo_last_record(self):
        if self.graph.records:
            self.graph.undo_last_record()
            messagebox.showinfo("Success", "Last record has been undone.")
        else:
            messagebox.showwarning("Undo Error", "No records to undo.")

    def clear_all_records(self):
        self.graph.clear_records()
        messagebox.showinfo("Success", "All records have been cleared.")
        self.debt_listbox.delete("1.0", tk.END)

    def view_debts(self):
        self.debt_listbox.delete("1.0", tk.END)
        debts = self.graph.view_debts()
        for debt in debts:
            self.debt_listbox.insert(tk.END, debt + "\n")

    def view_net_debts(self):
        self.debt_listbox.delete("1.0", tk.END)
        net_debts = self.graph.calculate_net_debts()
        for person, net_amount in net_debts.items():
            status = "owes" if net_amount < 0 else "is owed"
            self.debt_listbox.insert(tk.END, f"{person} {status} ${abs(net_amount):.2f}\n")

    def view_records(self):
        self.debt_listbox.delete("1.0", tk.END)
        records = self.graph.get_records()
        headers = f"{'Date':<12}{'Description':<20}{'From':<15}{'To':<15}{'Amount':<10}{'Image Path':<30}\n"
        self.debt_listbox.insert(tk.END, headers)
        self.debt_listbox.insert(tk.END, "-" * 100 + "\n")
        for i, record in enumerate(records):
            line = f"{record['date']:<12}{record['description']:<20}{record['from']:<15}{record['to']:<15}{record['amount']:<10.2f}{record['image_url'] if record['image_url'] else '':<30}\n"
            self.debt_listbox.insert(tk.END, line)
            if record['image_url']:
                view_image_button = tk.Button(self.debt_listbox, text="View Image", command=lambda path=record['image_url']: self.view_image(path))
                self.debt_listbox.window_create(tk.END, window=view_image_button)
                self.debt_listbox.insert(tk.END, "\n")

    def view_image(self, image_path):
        image_window = tk.Toplevel(self.root)
        image_window.title("View Image")
        img = Image.open(image_path)

        screen_width = image_window.winfo_screenwidth()
        screen_height = image_window.winfo_screenheight()
        img.thumbnail((screen_width - 100, screen_height - 100))

        img = ImageTk.PhotoImage(img)

        label = Label(image_window, image=img)
        label.image = img
        label.pack()

    def show_graph(self):
        G = self.graph.get_net_debt_graph()
        if not self.graph.cached_layout:
            pos = nx.spring_layout(G, k=2, iterations=200)
            self.graph.cached_layout = pos
        else:
            pos = self.graph.cached_layout
        edge_labels = nx.get_edge_attributes(G, 'weight')
        formatted_edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}

        colors = [plt.cm.tab20(i / len(G.nodes)) for i in range(len(G.nodes))]
        random.shuffle(colors)

        if self.graph_window is None or not tk.Toplevel.winfo_exists(self.graph_window):
            self.graph_window = tk.Toplevel(self.root)
            self.graph_window.title("Debt Graph")
            self.fig, self.ax = plt.subplots(figsize=(12, 8))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_window)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        else:
            self.ax.clear()

        nx.draw(G, pos, with_labels=True, node_size=3000, node_color=colors, font_size=10, font_weight='bold', arrows=True, ax=self.ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, font_size=8, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'), ax=self.ax)
        self.canvas.draw()

    def upload_image(self):
        if not self.graph.records:
            messagebox.showwarning("Upload Error", "Please record a debt before uploading an image.")
            return

        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if image_path:
            image_copy_path = os.path.join("images", os.path.basename(image_path))
            os.makedirs(os.path.dirname(image_copy_path), exist_ok=True)
            try:
                Image.open(image_path).save(image_copy_path)
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save image: {e}")
                return

            img = Image.open(image_copy_path)
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            if hasattr(self, 'image_label'):
                self.image_label.destroy()
            self.image_label = tk.Label(self.image_frame, image=img)
            self.image_label.image = img
            self.image_label.pack(pady=20)
            self.graph.update_record_with_image(len(self.graph.records) - 1, image_copy_path)
            self.graph.save_data(self.data_file)

    def on_closing(self):
        self.graph.save_data(self.data_file)
        self.root.destroy()