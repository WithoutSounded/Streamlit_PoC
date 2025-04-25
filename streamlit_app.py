import streamlit as st
import pandas as pd
import numpy as np
import time

# ==== 全域設定 ====
department_options = ["BI", "QA", "FrontEnd", "BackEnd", "會計", "法務", "運營"]
rank_options = ["一般員工", "主管"]

# ==== 簡單會員系統 ====
if "USERS" not in st.session_state:
    st.session_state.USERS = {
        "admin": {
            "password": "1234",
            "access": ["Dashboard", "分頁 1 - 動畫", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示", "🔧 管理使用者權限"],
            "name": "管理者",
            "emp_id": "0000",
            "department": "BI",
            "rank": "主管"
        },
        "user1": {
            "password": "abc",
            "access": ["Dashboard", "分頁 2 - 滑桿互動"],
            "name": "使用者一",
            "emp_id": "1001",
            "department": "FrontEnd",
            "rank": "一般員工"
        },
        "data": {
            "password": "4567",
            "access": ["Dashboard", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示"],
            "name": "數據人員",
            "emp_id": "1002",
            "department": "BI",
            "rank": "一般員工"
        },
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.title("🔐 請先登入或註冊")
    tab1, tab2 = st.tabs(["登入", "註冊"])

    with tab1:
        username = st.text_input("使用者名稱", key="login_user")
        password = st.text_input("密碼", type="password", key="login_pass")
        if st.button("登入"):
            if username in st.session_state.USERS and st.session_state.USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("登入成功！")
                st.rerun()
            else:
                st.error("登入失敗，請確認帳密")

    with tab2:
        new_user = st.text_input("新帳號名稱", key="reg_user")
        new_pass = st.text_input("設定密碼", type="password", key="reg_pass")
        new_name = st.text_input("姓名", key="reg_name")
        new_emp_id = st.text_input("工號", key="reg_emp_id")
        new_dept = st.selectbox("部門", department_options, key="reg_dept")
        new_rank = st.selectbox("職等", rank_options, key="reg_rank")
        new_role = st.selectbox("選擇角色模板 (權限)", ["admin", "data", "user1"], key="reg_role")
        if st.button("註冊"):
            if new_user in st.session_state.USERS:
                st.warning("使用者名稱已存在！")
            else:
                access = {
                    "admin": ["Dashboard", "分頁 1 - 動畫", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示", "🔧 管理使用者權限"],
                    "data": ["Dashboard", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示"],
                    "user1": ["Dashboard", "分頁 2 - 滑桿互動"],
                }[new_role]
                st.session_state.USERS[new_user] = {
                    "password": new_pass,
                    "access": access,
                    "name": new_name,
                    "emp_id": new_emp_id,
                    "department": new_dept,
                    "rank": new_rank
                }
                st.success("註冊成功，請登入！")
                st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# ==== 主系統 ====
if not st.session_state.logged_in:
    login()
else:
    username = st.session_state.username
    st.sidebar.title(f"👤 你好，{username}")
    if st.sidebar.button("登出"):
        logout()

    # 取得該使用者的可用頁面
    available_pages = st.session_state.USERS[username]["access"]

    # Sidebar navigation
    st.sidebar.title("📂 分頁選單")
    page = st.sidebar.radio("請選擇頁面：", available_pages)

    # Dashboard 歡迎頁
    if page == "Dashboard":
        st.title(f"🎉 歡迎來到 PlayOne Dashboard，{username}")
        user_data = st.session_state.USERS[username]
        st.markdown(f"**姓名**：{user_data['name']}")
        st.markdown(f"**工號**：{user_data['emp_id']}")
        st.markdown(f"**部門**：{user_data['department']}")
        st.markdown(f"**職等**：{user_data['rank']}")
        st.write("你可以使用以下功能：")
        for p in available_pages:
            if p != "Dashboard":
                st.markdown(f"✅ {p}")

    # Page 1: 動畫
    elif page == "分頁 1 - 動畫":
        st.title("🚀 動畫展示")
        if st.button("開始動畫"):
            with st.spinner("動畫進行中..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)
                    progress.progress(i + 1)
                st.success("完成啦！")

    # Page 2: 滑桿互動
    elif page == "分頁 2 - 滑桿互動":
        st.title("🎚️ x 與 x²")
        x = st.slider("請選擇 x：", 0, 100, 10)
        st.write(f"x = {x}")
        st.write(f"x² = {x**2}")

    # Page 3: DataFrame 標示
    elif page == "分頁 3 - DataFrame 標示":
        st.title("📊 標示超過門檻值的資料格")
        df = pd.DataFrame(np.random.randn(10, 5) * 10 + 50, columns=[f"欄{i+1}" for i in range(5)])
        threshold = st.slider("設定門檻值：", 50, 100, 80)

        def highlight(x):
            return np.where(x > threshold, "background-color: yellow", "")

        st.dataframe(df.style.apply(highlight, axis=None))

    # Admin: 使用者權限管理頁
    elif page == "🔧 管理使用者權限":
        st.title("🔧 管理使用者權限")
        for user, data in st.session_state.USERS.items():
            if user == "admin":
                continue  # 不修改 admin 自己
            with st.expander(f"👤 {user}"):
                new_access = st.multiselect(
                    "可使用的頁面：",
                    ["Dashboard", "分頁 1 - 動畫", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示", "🔧 管理使用者權限"],
                    default=data["access"],
                    key=f"access_{user}"
                )
                new_name = st.text_input("姓名", value=data.get("name", ""), key=f"name_{user}")
                new_emp = st.text_input("工號", value=data.get("emp_id", ""), key=f"emp_{user}")
                new_dept = st.selectbox("部門", department_options, index=department_options.index(data.get("department", department_options[0])), key=f"dept_{user}")
                new_rank = st.selectbox("職等", rank_options, index=rank_options.index(data.get("rank", rank_options[0])), key=f"rank_{user}")

                if st.button(f"更新 {user} 資料", key=f"btn_{user}"):
                    st.session_state.USERS[user]["access"] = new_access
                    st.session_state.USERS[user]["name"] = new_name
                    st.session_state.USERS[user]["emp_id"] = new_emp
                    st.session_state.USERS[user]["department"] = new_dept
                    st.session_state.USERS[user]["rank"] = new_rank
                    st.success(f"{user} 資料已更新 ✅")

