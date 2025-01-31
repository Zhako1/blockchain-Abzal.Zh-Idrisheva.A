import tkinter as tk
from tkinter import messagebox
from blockchain import Blockchain
from transaction import Transaction

class GUI:
    def __init__(self, root):
        self.root = root
        self.blockchain = Blockchain()
        self.add_transaction_frame()
        self.create_scrollable_frame()
        self.display_blocks()

    def create_scrollable_frame(self):
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def add_transaction_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Отправитель:").grid(row=0, column=0)
        self.sender_entry = tk.Entry(frame)
        self.sender_entry.grid(row=0, column=1)

        tk.Label(frame, text="Получатель:").grid(row=1, column=0)
        self.recipient_entry = tk.Entry(frame)
        self.recipient_entry.grid(row=1, column=1)

        tk.Label(frame, text="Сумма:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=2, column=1)

        tk.Label(frame, text="Комиссия:").grid(row=3, column=0)
        self.fee_entry = tk.Entry(frame)
        self.fee_entry.grid(row=3, column=1)

        tk.Button(frame, text="Добавить транзакцию", command=self.add_transaction).grid(row=4, columnspan=2)

    def add_transaction(self):
        try:
            sender = self.sender_entry.get()
            recipient = self.recipient_entry.get()
            amount = float(self.amount_entry.get())
            fee = float(self.fee_entry.get())
            transaction = Transaction(sender, recipient, amount, fee)
            if self.blockchain.add_block(transaction):
                self.display_blocks()
                self.clear_entries()
            else:
                messagebox.showerror("Ошибка", "Недостаточно средств для транзакции.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения для суммы и комиссии.")

    def clear_entries(self):
        self.sender_entry.delete(0, tk.END)
        self.recipient_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.fee_entry.delete(0, tk.END)

    def display_blocks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for block in self.blockchain.chain:
            frame = tk.Frame(self.scrollable_frame, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(frame, text=f"Блок {self.blockchain.chain.index(block)}", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(frame, text=f"Уақыт таңбасы: {block.timestamp}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Алдыңғы блоктың хэші: {block.previous_hash}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Меркле түбір: {block.merkle_root}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Блоктың өз хэші: {block.hash}", font=("Arial", 10)).pack(anchor="w")
            for tx in block.transactions:
                tk.Label(frame, text=f"Транзакция: {tx.transaction_hash}, Отправитель: {tx.sender}, Получатель: {tx.recipient}, Сумма: {tx.amount}, Комиссия: {tx .fee}", font=("Arial", 10)).pack(anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
