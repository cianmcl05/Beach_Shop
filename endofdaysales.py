import tkinter as tk

root = tk.Tk()
root.title("End of Day Sales")
root.geometry("550x330")
root.configure(bg="#fff7a8")

# === Header ===
title = tk.Label(root, text="End of Day\nSales", font=("Helvetica", 16, "bold"),
                 bg="#d9d6f2", padx=20, pady=5, relief="raised", justify="center")
title.place(relx=0.5, y=10, anchor="n")

back_btn = tk.Button(root, text="Back", font=("Helvetica", 11), bg="#b9f1c0", command=root.quit)
back_btn.place(x=10, y=10)

# === Input Labels and Fields ===
tk.Label(root, text="Reg:", bg="#fff7a8", font=("Helvetica", 11)).place(x=60, y=100)
tk.Entry(root, width=25).place(x=150, y=100)

tk.Label(root, text="Credit:", bg="#fff7a8", font=("Helvetica", 11)).place(x=60, y=140)
tk.Entry(root, width=25).place(x=150, y=140)

tk.Label(root, text="Cash in Envelope:", bg="#fff7a8", font=("Helvetica", 11)).place(x=60, y=180)
tk.Entry(root, width=25).place(x=200, y=180)

root.mainloop()
