import streamlit as st
import pandas as pd
import numpy as np
import time

# ==== 開發模式（自動登入 + 預設頁面） ====
DEV_MODE = False
if DEV_MODE:
    st.session_state.logged_in = True
    st.session_state.username = "admin"
    # st.session_state.current_page = "🔧 管理使用者權限"
    st.session_state.current_page = "分頁 1 - 動畫"


# ==== 全域設定 ====
department_options = ["BI", "QA", "FrontEnd", "BackEnd", "會計", "法務", "運營", "其他"]
rank_options = ["一般員工", "主管"]

# ==== 簡單會員系統 ====
if "USERS" not in st.session_state:
    st.session_state.USERS = {
        "admin": {
            "password": "admin",
            "access": ["Dashboard", "分頁 1 - 動畫", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示", "🔧 管理使用者權限"],
            "name": "管理者",
            "emp_id": "0000",
            "department": "其他",
            "rank": "主管"
        },
        "user1": {
            "password": "user1",
            "access": ["Dashboard", "分頁 2 - 滑桿互動"],
            "name": "使用者一",
            "emp_id": "0001",
            "department": "會計",
            "rank": "一般員工"
        },
        "user2": {
            "password": "user2",
            "access": ["Dashboard", "分頁 2 - 滑桿互動"],
            "name": "使用者一",
            "emp_id": "0002",
            "department": "會計",
            "rank": "一般員工"
        },
        "data": {
            "password": "data",
            "access": ["Dashboard", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示"],
            "name": "數據人員",
            "emp_id": "0003",
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
        new_user = st.text_input("使用者名稱", key="reg_user")
        new_pass = st.text_input("設定密碼", type="password", key="reg_pass")
        new_name = st.text_input("姓名", key="reg_name")
        new_emp = st.text_input("工號", key="reg_emp")
        new_dept = st.selectbox("部門", department_options, key="reg_dept")
        new_rank = st.selectbox("職等", rank_options, key="reg_rank")
        default_access = ["Dashboard", "分頁 2 - 滑桿互動"]
        if st.button("註冊"):
            if new_user in st.session_state.USERS:
                st.warning("使用者名稱已存在！")
            else:
                st.session_state.USERS[new_user] = {
                    "password": new_pass,
                    "access": default_access,
                    "name": new_name,
                    "emp_id": new_emp,
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

if __name__ == '__main__':
    if not st.session_state.logged_in:
        login()
    else:
        username = st.session_state.username
        st.sidebar.title(f"👤 你好，{username}")
        if st.sidebar.button("登出"):
            logout()

        available_pages = st.session_state.USERS[username]["access"]

        st.sidebar.title("📂 分頁選單")
        # page = st.sidebar.radio("請選擇頁面：", available_pages)

        page = st.sidebar.radio(
            "請選擇頁面：",
            available_pages,
            index=available_pages.index(st.session_state.get("current_page", available_pages[0]))
        )
        st.session_state.current_page = page


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

            st.subheader("📊 各部門使用者統計")
            dept_counts = {}
            for u, info in st.session_state.USERS.items():
                dept = info.get("department", "未設定")
                dept_counts[dept] = dept_counts.get(dept, 0) + 1

            dept_df = pd.DataFrame({
                "部門": list(dept_counts.keys()),
                "人數": list(dept_counts.values())
            })
            st.dataframe(dept_df, use_container_width=True)

        elif page == "🔧 管理使用者權限":
            st.title("🔧 管理使用者權限")

            with st.expander("➕ 新增使用者"):
                new_user = st.text_input("使用者名稱", key="admin_add_user")
                new_pass = st.text_input("密碼", type="password", key="admin_add_pass")
                new_name = st.text_input("姓名", key="admin_add_name")
                new_emp = st.text_input("工號", key="admin_add_emp")
                new_dept = st.selectbox("部門", department_options, key="admin_add_dept")
                new_rank = st.selectbox("職等", rank_options, key="admin_add_rank")
                default_access = ["Dashboard", "分頁 2 - 滑桿互動"]
                if st.button("新增使用者"):
                    if new_user in st.session_state.USERS:
                        st.warning("使用者已存在")
                    else:
                        st.session_state.USERS[new_user] = {
                            "password": new_pass,
                            "access": default_access,
                            "name": new_name,
                            "emp_id": new_emp,
                            "department": new_dept,
                            "rank": new_rank
                        }
                        st.success(f"✅ 成功新增使用者 {new_user}")
                        st.rerun()

            for dept in department_options:
                dept_users = [u for u, d in st.session_state.USERS.items() if d.get("department") == dept and u != "admin"]
                if dept_users:
                    st.subheader(f"🏢 {dept} 部門")
                    for user in dept_users:
                        data = st.session_state.USERS[user]
                        with st.expander(f"👤 {user}", expanded=False):
                            new_access = st.multiselect(
                                "功能權限：",
                                ["Dashboard", "分頁 1 - 動畫", "分頁 2 - 滑桿互動", "分頁 3 - DataFrame 標示", "🔧 管理使用者權限"],
                                default=data["access"], key=f"access_{user}"
                            )
                            new_name = st.text_input("姓名", value=data.get("name", ""), key=f"name_{user}")
                            new_emp = st.text_input("工號", value=data.get("emp_id", ""), key=f"emp_{user}")
                            new_dept = st.selectbox("部門", department_options, index=department_options.index(data.get("department", department_options[0])), key=f"dept_{user}")
                            new_rank = st.selectbox("職等", rank_options, index=rank_options.index(data.get("rank", rank_options[0])), key=f"rank_{user}")
                            if st.button(f"更新 {user} 資料", key=f"btn_{user}"):
                                data["access"] = new_access
                                data["name"] = new_name
                                data["emp_id"] = new_emp
                                data["department"] = new_dept
                                data["rank"] = new_rank
                                st.success(f"✅ {user} 的資料已更新")
                else:
                    st.subheader(f"🏢 {dept} 部門（目前無使用者）")

        elif page == "分頁 1 - 動畫":
            st.title("🚀 動畫展示")
            if st.button("開始動畫"):
                with st.spinner("動畫進行中..."):
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.03)
                        progress.progress(i + 1)
                    st.success("✅ 完成啦！")

        elif page == "分頁 2 - 滑桿互動":
            st.title("🎚️ x 與 x²")
            x = st.slider("請選擇 x：", 0, 100, 10)
            st.write(f"x = {x}")
            st.write(f"x² = {x**2}")
            st.caption("✅ 數值計算完成")

        elif page == "分頁 3 - DataFrame 標示":
            st.title("📊 標示超過門檻值的資料格")
            df = pd.DataFrame(np.random.randn(10, 5) * 10 + 50, columns=[f"欄{i+1}" for i in range(5)])
            threshold = st.slider("設定門檻值：", 50, 100, 80)

            def highlight(x):
                return np.where(x > threshold, "background-color: yellow", "")

            st.dataframe(df.style.apply(highlight, axis=None))
            st.caption("✅ 資料已套用標示規則")
