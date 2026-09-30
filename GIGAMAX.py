import itertools
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox

TARGET = 1190
OPERATIONS = [300, 120, -400, -250]


# ===== 搜尋最少步數組合 =====
def find_min_steps_combinations(start, max_steps=20):
    for steps in range(1, max_steps + 1):
        found = []
        for ops in itertools.product(OPERATIONS, repeat=steps):
            if start + sum(ops) == TARGET:
                found.append(ops)
        if found:
            return found
    return []


# ===== 壓縮組合 =====
def compress_combinations(combos):
    unique = {}
    for combo in combos:
        count = Counter(combo)
        for op in OPERATIONS:
            count[op] = count.get(op, 0)
        key = tuple(count[op] for op in OPERATIONS)
        unique[key] = count
    return list(unique.values())


# ===== 生成排列組合 =====
def generate_permutations(count):
    ops_list = []
    for op in OPERATIONS:
        ops_list += [op] * count[op]
    # 用 permutations 直接建立 set
    return set(itertools.permutations(ops_list))


# ===== Text 輸出 =====
def append_text(msg):
    text_output.insert(tk.END, msg + "\n")
    text_output.see(tk.END)


# ===== 展開排列 =====
def show_permutations(count, start_val):
    perms = generate_permutations(count)

    append_text("=" * 60)
    append_text(f"起始值 X = {start_val}")
    append_text(f"排列總數：{len(perms)}\n")

    for i, perm in enumerate(perms, 1):
        total = start_val
        steps_str = f"{total}"
        for step in perm:
            total += step
            steps_str += f" {'+' if step >= 0 else ''}{step} = {total}"
        append_text(f"排列 {i}: {steps_str}")

    append_text("=" * 60 + "\n")


# ===== 顯示壓縮結果 =====
def show_compressed(filtered, start_val):
    # 先清空舊按鈕
    for widget in frame_buttons.winfo_children():
        widget.destroy()

    for i, count in enumerate(filtered, 1):
        steps = sum(count[op] for op in OPERATIONS)
        line = (
            f"組合 {i}: "
            + ", ".join(
                [f"{'+' if op>0 else ''}{op} x {count[op]}" for op in OPERATIONS]
            )
            + f" （步數：{steps}）"
        )
        append_text(line)

        # 注意 lambda 綁定變數：必須用 default 參數避免 closure bug
        btn = ttk.Button(
            frame_buttons,
            text=f"展開排列 {i}",
            command=lambda c=count: show_permutations(c, start_val),
        )
        btn.pack(anchor="w", pady=3)


# ===== 計算按鈕 =====
def on_calculate():
    text_output.delete(1.0, tk.END)

    append_text(f"【目標值：{TARGET}】")
    append_text("")

    try:
        start_val = int(entry_start.get())
        max_steps = int(entry_max_steps.get())
    except ValueError:
        messagebox.showerror("錯誤", "請輸入整數！")
        return

    combos = find_min_steps_combinations(start_val, max_steps)
    if not combos:
        append_text("沒有找到任何組合")
        return

    compressed = compress_combinations(combos)
    perm_counts = [(count, len(generate_permutations(count))) for count in compressed]
    max_perm = max(perm_counts, key=lambda x: x[1])[1]
    filtered = [count for count, n in perm_counts if n == max_perm]

    append_text(f"找到最少步數組合，排列數最多的壓縮結果：{len(filtered)} 筆\n")
    show_compressed(filtered, start_val)


# ================================================
#                 Tkinter GUI
# ================================================
root = tk.Tk()
root.title("最少步數組合計算器")
root.geometry("900x650")


# ===== 上方輸入區 =====
frame_top = ttk.Frame(root)
frame_top.pack(pady=10)

ttk.Label(frame_top, text="起始值 X:").grid(row=0, column=0, padx=5)
entry_start = ttk.Entry(frame_top)
entry_start.insert(0, "50")
entry_start.grid(row=0, column=1, padx=5)

ttk.Label(frame_top, text="最大步數:").grid(row=0, column=2, padx=5)
entry_max_steps = ttk.Entry(frame_top)
entry_max_steps.insert(0, "12")
entry_max_steps.grid(row=0, column=3, padx=5)

ttk.Button(frame_top, text="計算", command=on_calculate).grid(
    row=0, column=4, padx=10
)

# ===== Text 輸出區 =====
frame_output = ttk.Frame(root)
frame_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

text_output = tk.Text(frame_output, wrap=tk.WORD, height=20)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll = ttk.Scrollbar(frame_output, command=text_output.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text_output.config(yscrollcommand=scroll.set)

# ===== 排列按鈕區 =====
frame_buttons = ttk.Frame(root)
frame_buttons.pack(anchor="w", padx=10, pady=10)

root.mainloop()
