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
#                     Streamlit 頁面設定
# ============================================================

st.set_page_config(
    page_title="GIGAMAX 最少步數組合計算器",
    page_icon="🔢",
    layout="wide"
)


# ============================================================
#                     搜尋最少步數組合
# ============================================================

def find_min_steps_combinations(start, target, max_steps=20):

    for steps in range(1, max_steps + 1):

        found = []

        for ops in itertools.product(OPERATIONS, repeat=steps):

            if start + sum(ops) == target:
                found.append(ops)

        if found:
            return found

    return []


# ============================================================
#                     壓縮組合
# ============================================================

def compress_combinations(combos, enable_limit=True):

    unique = {}

    for combo in combos:

        count = Counter(combo)

        for op in OPERATIONS:
            count[op] = count.get(op, 0)

        # ----------------------------------------------------
        # 限制條件
        #
        # (-400 數量) + (-250 數量)
        # <=
        # (+120 數量)
        #
        # enable_limit = True  → 啟用限制
        # enable_limit = False → 不啟用限制
        # ----------------------------------------------------

        if enable_limit:

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

    # 多重集合排列數：
    #
    # n!
    # -------------------------
    # a! × b! × c! × d!
    #

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
    max_steps,
    enable_limit
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
        combos,
        enable_limit
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
        for count, permutation_count in perm_counts
        if permutation_count == max_perm
    ]

    return filtered


# ============================================================
#                     Streamlit UI
# ============================================================

st.title("🔢 GIGAMAX 最少步數組合計算器")

st.markdown(
    "計算從起始值 X 到指定目標值所需的最少操作步數。"
)


# ============================================================
#                     輸入區
# ============================================================

col1, col2, col3 = st.columns(3)


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


with col3:

    enable_limit = st.checkbox(
        "啟用限制條件",
        value=True
    )


# ============================================================
#                     顯示目前設定
# ============================================================

st.divider()

st.write("### ⚙️ 目前設定")

st.write(
    f"**起始值 X：** {start_val}"
)

st.write(
    f"**操作：** {OPERATIONS}"
)

st.write(
    f"**最大搜尋步數：** {max_steps}"
)


if enable_limit:

    st.success(
        "已啟用限制：(-400 數量 + -250 數量) <= (+120 數量)"
    )

else:

    st.warning(
        "未啟用限制：不檢查 (-400 數量 + -250 數量) <= (+120 數量)"
    )


# ============================================================
#                     計算按鈕
# ============================================================

if st.button(
    "🚀 開始計算",
    type="primary",
    use_container_width=True
):

    st.divider()

    st.subheader(
        "📊 GIGAMAX 最少步數組合計算結果"
    )

    # --------------------------------------------------------
    # 逐一計算目標值
    # --------------------------------------------------------

    for target in TARGETS:

        st.markdown(
            f"## 🎯 目標值：{target}"
        )

        result = calculate_target(
            start_val,
            target,
            max_steps,
            enable_limit
        )

        # ----------------------------------------------------
        # 沒有符合條件的組合
        # ----------------------------------------------------

        if not result:

            st.warning(
                "沒有找到符合條件的組合。"
            )

            continue

        # ----------------------------------------------------
        # 顯示結果
        #
        # 目前維持原本程式邏輯：
        # 如果有多筆相同排列數，只顯示第一筆
        # ----------------------------------------------------

        st.success(
            "符合條件：1 筆"
        )

        count = result[0][0]

        steps = sum(
            count[op]
            for op in OPERATIONS
        )

        line = ", ".join(
            [
                f"{'+' if op > 0 else ''}{op} × {count[op]}"
                for op in OPERATIONS
            ]
        )

        st.write(
            f"**組合 1：** {line}"
        )

        st.write(
            f"**步數：** {steps}"
        )

        st.write(
            f"**排列數：** {result[0][1]:,}"
        )

        # ----------------------------------------------------
        # 顯示詳細數量
        # ----------------------------------------------------

        with st.expander("查看詳細組合"):

            for op in OPERATIONS:

                st.write(
                    f"{'+' if op > 0 else ''}{op}："
                    f"{count[op]} 次"
                )

        st.divider()


# ============================================================
#                     頁面底部說明
# ============================================================

with st.expander("📖 使用說明"):

    st.markdown(
        """
### 操作

- `+300`
- `+120`
- `-400`
- `-250`

### 限制條件

啟用時：

`(-400 次數 + -250 次數) <= (+120 次數)`

例如：

| +300 | +120 | -400 | -250 | 是否符合 |
|---:|---:|---:|---:|:---:|
| 2 | 3 | 1 | 1 | ✅ |
| 2 | 2 | 1 | 1 | ❌ |
| 1 | 5 | 2 | 1 | ✅ |
| 3 | 1 | 1 | 1 | ❌ |

停用限制後，以上所有組合都可以進一步進行排列數比較。
"""
    )
