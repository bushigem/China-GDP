import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import base64
from fpdf import FPDF

# 设置页面配置
st.set_page_config(page_title="中国省份 GDP 可视化与分析", layout="wide")


# 添加背景图函数
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# 调用背景图
add_bg_from_local("C:/Users/33910/Desktop/haokan.jpg")


# 加载 GDP 数据
@st.cache_data
def load_data():
    data = pd.read_csv(
        "D:/pycharm/project/123/streamlit/scripts/china_gdp_all_provinces_10_years.csv",
        encoding="utf-8-sig"
    )

    # 转换 'Year' 列为整数类型
    data["Year"] = pd.to_numeric(data["Year"], errors='coerce').fillna(0).astype(int)
    return data


# 加载数据
data = load_data()

# 侧边栏选项
st.sidebar.header("交互选项")
with st.sidebar.expander("地图选项", expanded=True):
    vis_type = st.selectbox("选择可视化类型", ["柱状图", "热力图", "散点图", "气泡图"])
    show_tooltip = st.checkbox("显示气泡提示", value=True)

# 选择年份
years = sorted(data["Year"].unique())
if len(years) > 1:
    selected_year = st.sidebar.slider("选择年份", min_value=min(years),
                                      max_value=max(years), value=max(years))
elif len(years) == 1:
    selected_year = years[0]
    st.sidebar.info(f"只有一个可用年份：{selected_year}")
else:
    st.sidebar.warning("没有可用的年份数据。")
    selected_year = None

# 省份筛选
selected_provinces = st.sidebar.multiselect("选择省份", data["Province"].unique(),
                                            default=data["Province"].unique())

# 数据筛选
if selected_year is not None:
    filtered_data = data[
        (data["Year"] == selected_year) & (data["Province"].isin(selected_provinces))]
else:
    filtered_data = pd.DataFrame(columns=data.columns)

# 统计分析
if st.sidebar.checkbox("显示统计分析") and not filtered_data.empty:
    mean_gdp = filtered_data["GDP"].mean()
    median_gdp = filtered_data["GDP"].median()
    std_gdp = filtered_data["GDP"].std()
    st.sidebar.write(f"平均 GDP: {mean_gdp:.2f} 亿元")
    st.sidebar.write(f"中位数 GDP: {median_gdp:.2f} 亿元")
    st.sidebar.write(f"标准差: {std_gdp:.2f} 亿元")

# 地图视角
view_state = pdk.ViewState(latitude=35.8617, longitude=104.1954, zoom=4, pitch=50)

# 创建图层
if vis_type == "柱状图" and not filtered_data.empty:
    layer = pdk.Layer(
        "ColumnLayer",
        data=filtered_data,
        get_position=["Longitude", "Latitude"],
        get_elevation="GDP",
        elevation_scale=100,
        radius=30000,
        get_color="[255, 255 - (GDP / 1000), 0]",
        pickable=True,
    )
elif vis_type == "热力图" and not filtered_data.empty:
    layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_data,
        get_position=["Longitude", "Latitude"],
        get_weight="GDP",
        radius_pixels=50,
    )
elif vis_type == "散点图" and not filtered_data.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position=["Longitude", "Latitude"],
        get_color="[255, 0, 0]",
        get_radius=50000,
        pickable=True,
    )
elif vis_type == "气泡图" and not filtered_data.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position=["Longitude", "Latitude"],
        get_radius="GDP",
        get_color="[0, 255, 0]",
        pickable=True,
    )
else:
    layer = None

# 显示地图
if layer:
    tooltip = {"html": "<b>{Province}</b><br/>GDP: {GDP}亿元",
               "style": {"color": "white"}}
    r = pdk.Deck(layers=[layer], initial_view_state=view_state,
                 map_style="mapbox://styles/mapbox/dark-v10",
                 tooltip=tooltip if show_tooltip else None)
    st.pydeck_chart(r)

# 显示数据表格
st.write("### 各省份 GDP 数据表")
st.dataframe(filtered_data)

# 绘制趋势图
if not filtered_data.empty:
    fig = px.line(filtered_data, x="Province", y="GDP", title="GDP 趋势分析",
                  markers=True)
    st.plotly_chart(fig)


# PDF 报告导出功能
def create_pdf():
    if not filtered_data.empty:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="中国省份 GDP 报告", ln=True, align="C")
        for index, row in filtered_data.iterrows():
            pdf.cell(200, 10, txt=f"{row['Province']}: {row['GDP']} 亿元", ln=True)
        pdf.output("gdp_report.pdf")


if st.sidebar.button("导出 PDF 报告"):
    create_pdf()
    st.sidebar.success("PDF 报告已生成")

# 用户反馈表单
with st.sidebar.form("feedback_form"):
    feedback = st.text_area("请留下您的建议或意见：")
    submitted = st.form_submit_button("提交反馈")
    if submitted:
        st.sidebar.success("感谢您的反馈！")

# 数据下载
st.sidebar.download_button(
    label="下载筛选后的数据",
    data=filtered_data.to_csv(index=False).encode('utf-8'),
    file_name='filtered_gdp_data.csv',
    mime='text/csv',
)
