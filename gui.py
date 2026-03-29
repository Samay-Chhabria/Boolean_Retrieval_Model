import tkinter as tk
from tkinter import scrolledtext, messagebox


class SearchInterface:
    """GUI for searching documents using the Boolean query query_processor."""

    def __init__(self, root, query_processor, documents):
        """Initialize the GUI with root window, query_processor, and documents."""
        self.root = root
        self.query_processor = query_processor
        self.documents = documents
        self.setup()

    def setup(self):
        """Set up the GUI components."""
        self.root.title("Boolean Retrieval System")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f0f0f0")

        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Boolean Retrieval System - Trump Speeches",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=15)

        # Input section
        input_section = tk.Frame(self.root, bg="#ecf0f1", padx=15, pady=15)
        input_section.pack(fill=tk.X)

        tk.Label(
            input_section,
            text="Enter Query:",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1"
        ).pack(anchor=tk.W, pady=(0, 5))

        # Search box
        search_box = tk.Frame(input_section)
        search_box.pack(fill=tk.X, pady=5)

        self.query_input = tk.Entry(search_box, font=("Arial", 11), width=100)
        self.query_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.query_input.bind("<Return>", lambda e: self.search())

        tk.Button(
            search_box, text="Search", font=("Arial", 11, "bold"),
            bg="#3498db", fg="white", command=self.search, padx=20
        ).pack(side=tk.LEFT)

        # Help
        help_msg = (
            "Examples: running | not hammer | actions AND wanted | united OR plane | "
            '"united states" | (near OR box) AND big | after years /1'
        )
        tk.Label(
            input_section, text=help_msg, font=("Arial", 9), bg="#ecf0f1",
            fg="#7f8c8d", wraplength=1000, justify=tk.LEFT
        ).pack(anchor=tk.W, pady=(5, 0))

        # Results section
        results_frame = tk.LabelFrame(
            self.root, text="Search Results", font=("Arial", 12, "bold"),
            padx=15, pady=15, bg="white"
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.status = tk.Label(results_frame, text="Ready", font=("Arial", 10), fg="#27ae60", bg="white")
        self.status.pack(anchor=tk.W, pady=(0, 10))

        self.output = scrolledtext.ScrolledText(
            results_frame, font=("Courier", 10), bg="#ffffff", fg="#2c3e50", height=24
        )
        self.output.pack(fill=tk.BOTH, expand=True)

        # Footer
        footer = tk.Frame(self.root, bg="#34495e", height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(
            footer,
            text=f"Documents: {len(self.documents)} | Operators: AND, OR, NOT | Proximity: term1 term2 /k",
            font=("Arial", 9), bg="#34495e", fg="white"
        ).pack(pady=10)

    def search(self):

        query = self.query_input.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a query.")
            return

        try:
            results = self.query_processor.process(query)
            self.show_results(query, results)
        except Exception as e:
            messagebox.showerror("Query Error", f"Error: {str(e)}")

    def show_results(self, query, doc_ids):

        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)

        self.output.insert(tk.END, f"Query: {query}\n")
        # 110-character visual separator for better readability in results display
        self.output.insert(tk.END, "=" * 110 + "\n\n")

        if not doc_ids:
            self.output.insert(tk.END, "No documents found.\n")
            self.status.config(text="No results found")
            self.output.config(state=tk.DISABLED)
            return

        # Sort document IDs numerically (convert from string to int for proper ordering)
        sorted_ids = sorted(list(doc_ids), key=lambda x: int(x))
        self.output.insert(tk.END, f"Found {len(sorted_ids)} document(s):\n\n")

        for doc_id in sorted_ids:
            filename = self.documents.get(int(doc_id), f"Unknown (ID: {doc_id})")
            self.output.insert(tk.END, f"  [{doc_id:2d}] {filename}\n")

        self.output.insert(tk.END, "\n" + "=" * 110 + "\n")
        self.output.insert(tk.END, f"Document IDs: {sorted_ids}\n")

        self.status.config(text=f"[OK] {len(sorted_ids)} document(s) found")
        self.output.config(state=tk.DISABLED)