import streamlit as st
from dotenv import load_dotenv
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# 页面配置
st.set_page_config(
    page_title="我的AI助手 - 大黄",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是名为大黄的AI助手，友好且乐于助人，能回答各类问题"}
    ]
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
    st.session_state.api_key = ""

# 侧边栏设计
with st.sidebar:
    st.image("jiqi.webp", caption="大黄", use_container_width=True)  # 替换为你的头像URL
    st.title("✨ 系统设置")
    
    # API密钥输入
    st.subheader("🔑 API密钥管理")
    api_key = st.text_input(
        "请输入OpenAI API密钥：",
        type="password",
        placeholder="sk-xxxxxxxxxxxxxxxxxxxx",
        value=st.session_state.api_key
    )
    if api_key:
        st.session_state.api_key = api_key

    # 系统角色设置
    st.subheader("🎭 角色设定")
    system_role = st.text_area(
        "设置AI角色（支持Markdown）：",
        value="你是友好的AI助手大黄，能提供专业且易懂的回答",
        height=150
    )
    if st.button("更新角色设定"):
        st.session_state.messages[0]["content"] = system_role

    # 侧边栏主题切换部分
    st.subheader("🎨 界面主题")
    theme = st.radio("选择主题：", ["light", "dark", "blue"], index=0)

    # 定义各主题的CSS
    themes = {
        "light": """
        <style>
        body {background-color: white; color: #333;}
        .stChatMessage {max-width: 80%; margin-left: auto; margin-right: auto;}
        </style>
        """,
        "dark": """
        <style>
        body {background-color: #1f1f1f; color: white;}
        .stChatMessage {max-width: 80%; margin-left: auto; margin-right: auto;}
        </style>
        """,
        "blue": """
        <style>
        body {background-color: #e3f2fd; color: #000;}
        .stChatMessage {max-width: 80%; margin-left: auto; margin-right: auto;}
        </style>
        """
    }

    # 应用主题CSS
    st.markdown(themes[theme], unsafe_allow_html=True)
    
    # 功能按钮
    add_vertical_space(2)
    if st.button("🗑️ 清空对话历史"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.memory.clear()
    if st.button("🚀 重新初始化"):
        st.session_state.clear()
        st.experimental_rerun()
    
    # 版权信息
    add_vertical_space(3)
    st.markdown("""
        <div style="text-align: center;">
            <hr style="border: 1px solid #ddd;">
            <p>版本 v1.2.0</p>
            <p>Powered by LangChain 🦜 + OpenAI 🌐</p>
        </div>
        """, unsafe_allow_html=True)

# 主界面布局
st.title("🤖 我的AI助手 - 大黄")
colored_header(label="", description="欢迎提问，我会尽力为你解答！", color_name="blue-70")

# 显示对话历史
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue  # 不显示系统角色
    st.chat_message(msg["role"]).write(msg["content"])

# 用户输入框
user_input = st.chat_input("请输入问题（支持Markdown格式）：你好，请问如何使用AI工具？")

if user_input:
    # 检查API密钥
    if not st.session_state.api_key:
        st.warning("⚠️ 请先在侧边栏输入API密钥", icon="⚠️")
        st.stop()
    
    # 显示用户消息
    st.chat_message("human").write(user_input)
    st.session_state.messages.append({"role": "human", "content": user_input})
    
    # 生成AI回复
    with st.spinner("AI正在思考... 请稍候"):
        model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=st.session_state.api_key,
            base_url="https://twapi.openai-hk.com/v1",
            temperature=0.7
        )
        chain = ConversationChain(
            llm=model,
            memory=st.session_state.memory,
            verbose=True
        )
        response = chain.predict(input=user_input)
        
        # 显示AI回复
        st.chat_message("ai").write(response)
        st.session_state.messages.append({"role": "ai", "content": response})

# 底部提示
st.markdown("""
    <div style="text-align: right; color: #666; margin-top: 2rem;">
        提示：输入 <code>/help</code> 查看功能列表
    </div>
    """, unsafe_allow_html=True)