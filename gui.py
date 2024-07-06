import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import struc as analyzer

class StructuralAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Structural Analyzer")

        self.nodes = []
        self.members = []
        self.supports = []
        self.loads = []

        self.current_node_id = 1

        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        self.node_frame = ttk.LabelFrame(self.root, text="Nodes")
        self.node_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.node_frame, text="X Position:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.node_frame, text="Y Position:").grid(row=1, column=0, padx=5, pady=5)

        self.x_entry = ttk.Entry(self.node_frame)
        self.x_entry.grid(row=0, column=1, padx=5, pady=5)
        self.y_entry = ttk.Entry(self.node_frame)
        self.y_entry.grid(row=1, column=1, padx=5, pady=5)

        self.save_node_button = ttk.Button(self.node_frame, text="Save Node", command=self.save_node)
        self.save_node_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.member_frame = ttk.LabelFrame(self.root, text="Members")
        self.member_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.member_frame, text="Start Node ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.member_frame, text="End Node ID:").grid(row=1, column=0, padx=5, pady=5)

        self.start_node_combobox = ttk.Combobox(self.member_frame, values=[])
        self.start_node_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.end_node_combobox = ttk.Combobox(self.member_frame, values=[])
        self.end_node_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.save_member_button = ttk.Button(self.member_frame, text="Save Member", command=self.save_member)
        self.save_member_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.support_frame = ttk.LabelFrame(self.root, text="Supports")
        self.support_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.support_frame, text="Node ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.support_frame, text="UX Fixed:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.support_frame, text="UY Fixed:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(self.support_frame, text="RZ Fixed:").grid(row=3, column=0, padx=5, pady=5)

        self.support_node_combobox = ttk.Combobox(self.support_frame, values=[])
        self.support_node_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.ux_fixed = tk.IntVar()
        self.uy_fixed = tk.IntVar()
        self.rz_fixed = tk.IntVar()

        ttk.Checkbutton(self.support_frame, variable=self.ux_fixed).grid(row=1, column=1, padx=5, pady=5)
        ttk.Checkbutton(self.support_frame, variable=self.uy_fixed).grid(row=2, column=1, padx=5, pady=5)
        ttk.Checkbutton(self.support_frame, variable=self.rz_fixed).grid(row=3, column=1, padx=5, pady=5)

        self.save_support_button = ttk.Button(self.support_frame, text="Save Support", command=self.save_support)
        self.save_support_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.load_frame = ttk.LabelFrame(self.root, text="Loads")
        self.load_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(self.load_frame, text="Node ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.load_frame, text="FX:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.load_frame, text="FY:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(self.load_frame, text="MZ:").grid(row=3, column=0, padx=5, pady=5)

        self.load_node_combobox = ttk.Combobox(self.load_frame, values=[])
        self.load_node_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.fx_entry = ttk.Entry(self.load_frame)
        self.fx_entry.grid(row=1, column=1, padx=5, pady=5)
        self.fy_entry = ttk.Entry(self.load_frame)
        self.fy_entry.grid(row=2, column=1, padx=5, pady=5)
        self.mz_entry = ttk.Entry(self.load_frame)
        self.mz_entry.grid(row=3, column=1, padx=5, pady=5)

        self.save_load_button = ttk.Button(self.load_frame, text="Save Load", command=self.save_load)
        self.save_load_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.analyze_button = ttk.Button(self.root, text="Analyze Structure", command=self.analyze_structure)
        self.analyze_button.grid(row=4, column=0, padx=10, pady=10)

        self.canvas_frame = ttk.LabelFrame(self.root, text="Structure Visualization")
        self.canvas_frame.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

    def create_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        self.ax.set_title("Structural Model")
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")

        for node in self.nodes:
            self.ax.plot(node[1], node[2], 'bo')
            self.ax.text(node[1], node[2], str(node[0]), fontsize=12, ha='right')

        for member in self.members:
            start_node = next(node for node in self.nodes if node[0] == member[0])
            end_node = next(node for node in self.nodes if node[0] == member[1])
            self.ax.plot([start_node[1], end_node[1]], [start_node[2], end_node[2]], 'k-')

        self.canvas.draw()

    def save_node(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            self.nodes.append((self.current_node_id, x, y))
            self.current_node_id += 1

            self.update_node_comboboxes()
            self.update_plot()

            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid node coordinates")

    def update_node_comboboxes(self):
        node_ids = [node[0] for node in self.nodes]
        self.start_node_combobox['values'] = node_ids
        self.end_node_combobox['values'] = node_ids
        self.support_node_combobox['values'] = node_ids
        self.load_node_combobox['values'] = node_ids

    def save_member(self):
        try:
            start_node_id = int(self.start_node_combobox.get())
            end_node_id = int(self.end_node_combobox.get())
            self.members.append((start_node_id, end_node_id))
            self.update_plot()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid member data")

    def save_support(self):
        try:
            node_id = int(self.support_node_combobox.get())
            ux = self.ux_fixed.get()
            uy = self.uy_fixed.get()
            rz = self.rz_fixed.get()
            self.supports.append((node_id, ux, uy, rz))
        except ValueError:
            messagebox.showerror("Input Error", "Invalid support data")

    def save_load(self):
        try:
            node_id = int(self.load_node_combobox.get())
            fx = float(self.fx_entry.get())
            fy = float(self.fy_entry.get())
            mz = float(self.mz_entry.get())
            self.loads.append((node_id, fx, fy, mz))

            self.fx_entry.delete(0, tk.END)
            self.fy_entry.delete(0, tk.END)
            self.mz_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid load data")

    def analyze_structure(self):
        try:
            n = len(self.nodes)
            m = len(self.members)

            XY_values = [coord for node in self.nodes for coord in node[1:]]
            NC_values = [member for member in self.members]
            BC_values = [support for support in self.supports]
            FEXT_values = [load for load in self.loads]

            results = analyzer.run_analysis(n, m, XY_values, NC_values, BC_values, FEXT_values)
            messagebox.showinfo("Analysis Results", results)
        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = StructuralAnalyzerApp(root)
    root.mainloop()