import itertools
import math
from collections import Counter

import streamlit as st


# ============================================================
#                     基本設定
# ============================================================

TARGETS = [1190, 1180, 1170, 1160]

OPERATIONS = [300, 120, -400, -250]


# ============================================================
#                     搜尋最少步數組合
# ============================================================

def find_min_steps_combinations(start, target, max_steps=20):

    for steps in range(1, max_steps + 1):

        found = []

        for ops in itertools.product(
            OPERATIONS,
            repeat=steps
        ):

            if start + sum(ops) == target:
                found.append(ops)

        if found:
            return found

    return []


# ============================================================
#                     壓縮組合
# ============================================================

def compress_combinations(combos):

    unique = {}

    for combo in combos:

        count = Counter(combo)

        for op in OPERATIONS:
            count[op] = count.get(op, 0)

        # ----------------------------------------------------
        # 限制條件：
        #
        # (-400 數量) + (-250 數量)
        # <=
        # (+120 數量)
        # ----------------------------------------------------

        if count[-400] + count[-250] > count[120]:
            continue

        key = tuple(
            count[op]
            for op in OPERATIONS
        )

        unique[key] = count

    return list(unique.values())


# ============================================================
#                     計算排列數
# ============================================================

def count_permutations(count):

    total_steps = sum(
        count[op]
        for op in OPERATIONS
    )

    # --------------------------------------------------------
    # 多重集合排列數：
    #
    # n!
    # -------------------------
    # a! × b! × c! × d!
    # --------------------------------------------------------

    result = math.factorial(total_steps)

    for op in OPERATIONS:

        result //= math.factorial(
            count[op]
        )

    return result


# ============================================================
#                     單一目標值計算
# ============================================================

def calculate_target(
    start_val,
    target,
    max_steps
):

    # --------------------------------------------------------
    # 找到「絕對最少步數」的所有組合
    # --------------------------------------------------------

    combos = find_min_steps_combinations(
        start_val,
        target,
        max_steps
    )

    if not combos:
        return None

    # --------------------------------------------------------
    # 套用限制條件
    # --------------------------------------------------------

    compressed = compress_combinations(
        combos
    )

    if not compressed:
        return None

    # --------------------------------------------------------
    # 計算每個組合的排列數
    # --------------------------------------------------------

    perm_counts = []

    for count in compressed:

        permutation_count = count_permutations(
            count
        )

        perm_counts.append(
            (
                count,
                permutation_count
            )
        )

    # --------------------------------------------------------
    # 找出排列數最多的組合
    # --------------------------------------------------------

    max_perm = max(
        perm_counts,
        key=lambda x: x[1]
    )[1]

    filtered = [
        (
            count,
            permutation_count
        )
        for count, permutation_count
        in perm_counts
        if permutation_count == max_perm
    ]

    return filtered


# ============================================================
#                     Streamlit 設定
# ============================================================

st.set_page_config(
    page_title="GIGAMAX",
    page_icon="🔢",
    layout="wide"
)


# ============================================================
#                     標題
# ============================================================

st.title(
    "GIGAMAX 最少步數組合計算器"
)

st.write(
    "尋找從起始值 X 到指定目標值的最少步數組合。"
)


# ============================================================
#                     基本資訊
# ============================================================

st.info(
    "目標值：1190 / 1180 / 1170 / 1160"
)

st.write(
    "操作："
    "`+300`、`+120`、`-400`、`-250`"
)

st.write(
    "限制："
    "`(-400 數量 + -250 數量) <= (+120 數量)`"
)


# ============================================================
#                     輸入區
# ============================================================

col1, col2 = st.columns(2)


with col1:

    start_val = st.number_input(
        "起始值 X",
        value=50,
        step=1
    )


with col2:

    max_steps = st.number_input(
        "最大搜尋步數",
        value=12,
        min_value=1,
        max_value=20,
        step=1
    )


# ============================================================
#                     計算按鈕
# ============================================================

calculate_button = st.button(
    "開始計算",
    type="primary",
    use_container_width=True
)


# ============================================================
#                     開始計算
# ============================================================

if calculate_button:

    start_val = int(start_val)
    max_steps = int(max_steps)

    st.divider()

    st.subheader(
        "計算條件"
    )

    st.write(
        f"起始值 X：**{start_val}**"
    )

    st.write(
        f"最大搜尋步數：**{max_steps}**"
    )

    st.write(
        "限制："
        "**(-400 數量 + -250 數量) <= (+120 數量)**"
    )

    st.divider()

    # ========================================================
    #                   逐一計算目標值
    # ========================================================

    for target in TARGETS:

        st.header(
            f"目標值：{target}"
        )

        with st.spinner(
            f"正在計算目標值 {target}..."
        ):

            result = calculate_target(
                start_val,
                target,
                max_steps
            )

        # ----------------------------------------------------
        # 沒有符合條件
        # ----------------------------------------------------

        if not result:

            st.warning(
                "沒有找到符合條件的組合。"
            )

            continue

        # ----------------------------------------------------
        # 顯示結果
        #
        # 目前按照你的原程式：
        # 如果有多筆相同排列數，
        # 只顯示第一筆。
        # ----------------------------------------------------

        st.success(
            "找到符合條件的組合。"
        )

        count = result[0][0]

        permutation_count = result[0][1]

        steps = sum(
            count[op]
            for op in OPERATIONS
        )

        # ----------------------------------------------------
        # 組合內容
        # ----------------------------------------------------

        combination_text = ", ".join(
            [
                f"{'+' if op > 0 else ''}"
                f"{op} x {count[op]}"
                for op in OPERATIONS
            ]
        )

        st.write(
            f"**組合 1：** "
            f"{combination_text}"
        )

        st.write(
            f"步數：**{steps}**"
        )

        st.write(
            f"排列數：**{permutation_count:,}**"
        )

        # ----------------------------------------------------
        # 顯示完整結果資訊
        # ----------------------------------------------------

        with st.expander(
            "查看詳細資料"
        ):

            st.write(
                f"目標值：{target}"
            )

            st.write(
                f"起始值：{start_val}"
            )

            st.write(
                f"步數：{steps}"
            )

            st.write(
                f"排列總數："
                f"{permutation_count:,}"
            )

            st.write(
                "各操作數量："
            )

            for op in OPERATIONS:

                st.write(
                    f"{'+' if op > 0 else ''}"
                    f"{op}："
                    f"{count[op]} 次"
                )

        st.divider()


# ============================================================
#                     Footer
# ============================================================

st.caption(
    "GIGAMAX"
)
