import itertools
from collections import Counter
import streamlit as st


# ================================================
# 設定
# ================================================

TARGET = 1190
OPERATIONS = [300, 120, -400, -250]


# ================================================
# 搜尋最少步數組合
# ================================================

def find_min_steps_combinations(start, max_steps=20):
    for steps in range(1, max_steps + 1):
        found = []

        for ops in itertools.product(OPERATIONS, repeat=steps):
            if start + sum(ops) == TARGET:
                found.append(ops)

        if found:
            return found

    return []


# ================================================
# 壓縮組合
# ================================================

def compress_combinations(combos):
    unique = {}

    for combo in combos:
        count = Counter(combo)

        for op in OPERATIONS:
            count[op] = count.get(op, 0)

        key = tuple(count[op] for op in OPERATIONS)

        unique[key] = count

    return list(unique.values())


# ================================================
# 生成排列組合
# ================================================

def generate_permutations(count):
    ops_list = []

    for op in OPERATIONS:
        ops_list += [op] * count[op]

    return set(itertools.permutations(ops_list))


# ================================================
# 顯示單一排列
# ================================================

def format_permutation(perm, start_val):
    total = start_val
    steps_str = f"{total}"

    for step in perm:
        total += step
        steps_str += f" {'+' if step >= 0 else ''}{step} = {total}"

    return steps_str


# ================================================
# Streamlit UI
# ================================================

st.set_page_config(
    page_title="GIGAMAX",
    page_icon="🔢",
    layout="wide"
)

st.title("最少步數組合計算器")

st.write(f"目標值：**{TARGET}**")


# ================================================
# 輸入區
# ================================================

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    start_val = st.number_input(
        "起始值 X",
        value=50,
        step=1
    )

with col2:
    max_steps = st.number_input(
        "最大步數",
        value=12,
        min_value=1,
        max_value=20,
        step=1
    )

with col3:
    st.write("")
    st.write("")

    calculate_button = st.button(
        "計算",
        type="primary",
        use_container_width=True
    )


# ================================================
# 計算
# ================================================

if calculate_button:

    with st.spinner("計算中..."):

        combos = find_min_steps_combinations(
            int(start_val),
            int(max_steps)
        )

    if not combos:

        st.warning("沒有找到任何組合")

    else:

        compressed = compress_combinations(combos)

        # 計算每個壓縮組合的排列數
        perm_counts = []

        for count in compressed:
            permutation_count = len(
                generate_permutations(count)
            )

            perm_counts.append(
                (count, permutation_count)
            )

        # 找出最大排列數
        max_perm = max(
            perm_counts,
            key=lambda x: x[1]
        )[1]

        # 只保留排列數最多的組合
        filtered = [
            count
            for count, n in perm_counts
            if n == max_perm
        ]

        # ========================================
        # 顯示結果摘要
        # ========================================

        st.success(
            f"找到最少步數組合，"
            f"排列數最多的壓縮結果：{len(filtered)} 筆"
        )

        st.write(
            f"最少步數："
            f"**{sum(filtered[0][op] for op in OPERATIONS)}**"
        )

        st.write(
            f"最多排列數：**{max_perm}**"
        )

        st.divider()

        # ========================================
        # 顯示組合
        # ========================================

        for i, count in enumerate(filtered, 1):

            steps = sum(
                count[op]
                for op in OPERATIONS
            )

            line = (
                f"組合 {i}: "
                + ", ".join(
                    [
                        f"{'+' if op > 0 else ''}"
                        f"{op} x {count[op]}"
                        for op in OPERATIONS
                    ]
                )
                + f" （步數：{steps}）"
            )

            st.subheader(
                f"組合 {i}"
            )

            st.write(line)

            permutation_count = len(
                generate_permutations(count)
            )

            st.write(
                f"排列總數：**{permutation_count}**"
            )

            # ====================================
            # 展開排列
            # ====================================

            with st.expander(
                f"展開排列 {i}"
            ):

                perms = generate_permutations(count)

                for j, perm in enumerate(perms, 1):

                    result = format_permutation(
                        perm,
                        int(start_val)
                    )

                    st.write(
                        f"排列 {j}: {result}"
                    )
