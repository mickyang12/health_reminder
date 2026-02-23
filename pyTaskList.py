import psutil
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

def fmt_time(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

TARGETS = {"python.exe", "pythonw.exe"}
SELF_PID = os.getpid()

rows = []

for p in psutil.process_iter([
    "pid",
    "name",
    "exe",
    "cmdline",
    "create_time",
    "cpu_percent",
    "memory_info",
    "username",
]):
    try:
        if (
            p.info["name"]
            and p.info["name"].lower() in TARGETS
            and p.info["pid"] != SELF_PID
        ):
            rows.append({
                "pid": p.info["pid"],
                "name": p.info["name"],
                "cmd": " ".join(p.info["cmdline"] or []),
                "user": p.info["username"],
                "cpu": p.info["cpu_percent"],
                "mem": round(p.info["memory_info"].rss / 1024 / 1024, 1),
            })
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

# ---------------- UI ----------------

root = tk.Tk()
root.title("Python Process Killer")
root.geometry("1100x400")

tree = ttk.Treeview(
    root,
    columns=("pid", "name", "user", "cpu", "mem", "cmd"),
    show="headings",
    selectmode="extended",
)

tree.heading("pid", text="PID")
tree.heading("name", text="Process")
tree.heading("user", text="User")
tree.heading("cpu", text="CPU %")
tree.heading("mem", text="RAM (MB)")
tree.heading("cmd", text="Command Line")

tree.column("pid", width=80, anchor="e")
tree.column("name", width=100)
tree.column("user", width=150)
tree.column("cpu", width=80, anchor="e")
tree.column("mem", width=90, anchor="e")
tree.column("cmd", width=600)

for r in rows:
    tree.insert(
        "",
        "end",
        values=(
            r["pid"],
            r["name"],
            r["user"],
            r["cpu"],
            r["mem"],
            r["cmd"],
        ),
    )

tree.pack(fill="both", expand=True, padx=10, pady=10)

def kill_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "請先選取要 kill 的 process")
        return

    pids = [int(tree.item(i)["values"][0]) for i in selected]

    if not messagebox.askyesno(
        "Confirm Kill",
        f"確定要 kill 以下 PID？\n\n{pids}"
    ):
        return

    for pid in pids:
        try:
            psutil.Process(pid).kill()
        except Exception as e:
            messagebox.showerror("Error", f"PID {pid} kill 失敗：{e}")

    messagebox.showinfo("Done", "選取的 process 已處理完成")
    root.destroy()

btn = tk.Button(
    root,
    text="Kill Selected",
    bg="red",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    command=kill_selected,
)

btn.pack(pady=8)

root.mainloop()