import tkinter as tk
from blockchain import Blockchain

class BlockchainGUI:
    def __init__(self):
        self.blockchain = Blockchain()
        self.blockchain.add_block("Генезис блогы")
        self.blockchain.add_block("Блок 1 деректері")
        self.blockchain.add_block("Блок 2 деректері")

        self.root = tk.Tk()
        self.root.title("Блокты Зерттеуші")

        self.display_blocks()

    def display_blocks(self):
        for block in self.blockchain.chain:
            frame = tk.Frame(self.root, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(frame, text=f"Блок {self.blockchain.chain.index(block)}", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(frame, text=f"Уақыт таңбасы: {block.timestamp}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Алдыңғы блоктың хэші: {block.previous_hash}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Блоктың өз хэші: {block.hash}", font=("Arial", 10)).pack(anchor="w")
            tk.Label(frame, text=f"Деректер: {block.data}", font=("Arial", 10)).pack(anchor="w")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = BlockchainGUI()
    gui.run()
