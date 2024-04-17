import cv2
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import simulation
import sys
import pandas as pd
import util
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
import os
import io
from generator import *
import base64

st.set_page_config(layout="wide")
custom_html = """
<div class="banner">
    <img src="https://raw.githubusercontent.com/znzhao/CS2Terrain/main/fig/plain.png" alt="Banner Image">
</div>
<style>
    .banner {
        width: 160%;
        height: 400px;
        overflow: hidden;
    }
    .banner img {
        width: 75%;
        object-fit: cover;
    }
</style>
"""
st.components.v1.html(custom_html)

# Sidebar content
CHN = st.sidebar.toggle('CHN/中文', value = False)
st.sidebar.header("Terrain Setting Parameters" if not CHN else "地形设置")
expand1 = st.sidebar.expander("Basics" if not CHN else "基础噪声参数")
with expand1:
    seed = st.number_input('Random Seed' if not CHN else "随机种子", value=123)
    ks1 = st.selectbox('Signal Average Kernel Size' if not CHN else "信号平滑卷积核", index = 4, options=[4, 8, 16, 32, 64, 128])
    ksize = (ks1, ks1)
    init_size = st.slider('Initial Terrain Weight' if not CHN else "初始地形权重", min_value = 0.0, max_value = 1.0, value=0.5)
    noise_size = st.slider('Noise Terrain Weight' if not CHN else "噪声地形权重", min_value = 0.0, max_value = 1.0, value=0.5)
    dim =  st.selectbox('Resize Dimension' if not CHN else "缩放精度", index = 1, options=[256, 512, 1024])
    if dim == 1024: st.warning('Warning: a large dimension might slow down the speed!'  if not CHN else "警告：缩放精度过高会导致运行速度降低，请谨慎选择！")
    ks2 = st.selectbox('Reverse Kernel Size' if not CHN else "复原平滑卷积核", index = 4, options=[4, 8, 16, 32, 64, 128, 256, 512,])
    revise_kernel = (ks2-1, ks2-1)
    min_altitude, max_altitude = st.slider('Output Height Range(meter) (Baseline Plain = 500m)' if not CHN else "输出高度范围（米）(基准平原为500米)", 0, 4000, (300, 1200))

if 'intpl_val_outnum' not in st.session_state:
	st.session_state.intpl_val_outnum = 0
      
def increment_counter():
	st.session_state.intpl_val_outnum += 1

def decrement_counter():
    st.session_state.intpl_val_outnum = st.session_state.intpl_val_outnum - 1 if st.session_state.intpl_val_outnum >0 else 0

expand2 = st.sidebar.expander("Detail Richness" if not CHN else "细节丰富度")
with expand2:
    colx, coly = st.columns(2)
    oceanx = colx.number_input('Ocean Altitude(%)' if not CHN else "海洋锚点(%)", value=0.0, min_value=0.0, max_value=100.0, disabled=True)
    oceany = coly.number_input('Ocean Effection(%)' if not CHN else "海洋影响因子(%)", value=10.0, min_value=0.0, max_value=100.0)
    plainx = colx.number_input('Plain Altitude(%)' if not CHN else "平原锚点(%)", value=12.5, min_value=0.0, max_value=100.0)
    plainy = coly.number_input('Plain Effection(%)' if not CHN else "平原影响因子(%)", value=75.0, min_value=0.0, max_value=100.0)
    mountx = colx.number_input('Mount Altitude(%)' if not CHN else "山脉锚点(%)", value=100.0, min_value=0.0, max_value=100.0, disabled=True)
    mounty = coly.number_input('Mount Effection(%)' if not CHN else "山脉影响因子(%)", value=100.0, min_value=0.0, max_value=100.0)
    ocean = (oceanx/100, oceany/100)
    plain = (plainx/100, plainy/100)
    mountain = (mountx/100, mounty/100)
        
    intplx = [ocean[0], plain[0], mountain[0]]
    loudness = [ocean[1], plain[1], mountain[1]]
    if st.session_state.intpl_val_outnum>0:
        keyxs = [str("anchorx"+str(i)) for i in range(st.session_state.intpl_val_outnum)]
        keyys = [str("anchory"+str(i)) for i in range(st.session_state.intpl_val_outnum)]
        valuexs = [colx.number_input('Outside Altitude(%)' if not CHN else '额外锚点(%)', value=10.0, min_value=0.0, max_value=100.0, key = keyxs[i]) for i in range(st.session_state.intpl_val_outnum)]
        valueys = [coly.number_input('Outside Effection(%)' if not CHN else '额外影响因子(%)', value=10.0, min_value=0.0, max_value=100.0, key = keyys[i]) for i in range(st.session_state.intpl_val_outnum)]
        intplx = intplx + [x/100 for x in valuexs]
        loudness = loudness + [y/100 for y in valueys]
    colx.button('Add Anchor' if not CHN else "增加锚点", on_click=increment_counter)
    coly.button('Delete Anchor' if not CHN else "减少锚点", on_click=decrement_counter, disabled=st.session_state.intpl_val_outnum==0)
    sorted_intplx = sorted(intplx)
    sorted_loudness = [loudness[i] for i in sorted(range(len(intplx)), key=lambda x: intplx[x])]
    fadeintplvec = np.vectorize(lambda x: fadeintpl(x, sorted_intplx, sorted_loudness))
    oneline = np.linspace(0.0,1.0,50).tolist()
    curf = fadeintplvec(oneline)
    showdata = pd.DataFrame([curf]).T
    colname = 'Effection' if not CHN else "影响度"
    indname = 'Altitude Percent(%)' if not CHN else "高度百分比"
    showdata.columns = [colname]
    showdata.index = [x *100 for x in oneline]
    showdata.index.name = indname
    
    fig = px.line(showdata, 
                  y = colname,
                  )
    fig.update_layout(autosize=True, height = 400)
    st.plotly_chart(fig, use_container_width=True)

expand3 = st.sidebar.expander("Rain Erosion" if not CHN else "雨水侵蚀作用")
with expand3:
    erosion = st.toggle('Apply Rain Erosion' if not CHN else "施加雨水侵蚀", value = False)
    if erosion: st.warning('Warning: Apply rain erosion might significantly slow down the speed!'  if not CHN else "警告：施加侵蚀作用会导致运行速度显著降低，请谨慎选择")
    full_width = st.number_input('Full Width' if not CHN else "降雨范围", value=200, min_value=0, disabled=not erosion)
    rain_rate10000 = st.number_input('Rain Rate(1/10000)' if not CHN else "降雨量（万分之一）", value=8.0, min_value=0.0, disabled=not erosion)
    rain_rate = rain_rate10000/10000.0
    evaporation_rate10000 = st.number_input('Evaporation Rate(1/10000)' if not CHN else "蒸发速率（万分之一）", value=5.0, min_value=0.0, disabled=not erosion)
    evaporation_rate = evaporation_rate10000/10000.0
    min_height_delta = st.number_input('Min Height Delta' if not CHN else "最小高度差", value=0.05, min_value=0.0, disabled=not erosion)
    repose_slope = st.number_input('Repose Slope' if not CHN else "休止坡度", value=0.03, min_value=0.0, disabled=not erosion)
    gravity = st.number_input('Gravity' if not CHN else "重力", value=30.0, min_value=0.0, disabled=not erosion)

if 'first_submitted' not in st.session_state:
    st.session_state.first_submitted = True

if 'submitted' not in st.session_state:
    st.session_state.submitted = False
    

def onclick_submit():
    st.session_state.submitted = True

st.sidebar.button("Submit" if not CHN else "提交", on_click=onclick_submit)

if 'input_height' not in st.session_state:
    st.session_state.input_height = np.ones(shape=(dim, dim))*plainx/100

# Main content
st.title("Cities Skyline II Terrain Modifier" if not CHN else "城市天际线2：地形生成器")
def get_image_path(img):
    # Create a directory and save the uploaded image.
    file_path = f"data/uploadedImages/{img.name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as img_file:
        img_file.write(img.getbuffer())
    return file_path

uploaded_file = st.file_uploader("Upload terrain height map (PNG)." if not CHN else "上传初始地形图（PNG）", type= ['png'] )
threeD = st.toggle('3D Plot' if not CHN else "展示3D视图", value = False)
colm1, colm2 = st.columns(2)
if 'output_height' not in st.session_state:
    st.session_state.output_height = None


progress_text = 'Erosion in progress. Please wait.' if not CHN else '侵蚀模型处理中，请稍后...'
progress_text2 = 'Erosion finished.' if not CHN else '侵蚀模型处理完成。'

def click_submit():
    st.session_state.output_height = processTerrain(sorted_intplx, sorted_loudness, dim, seed, ksize, init_size, noise_size, erosion, full_width, rain_rate, 
                                                    evaporation_rate, min_height_delta, repose_slope, gravity, min_altitude, max_altitude, 
                                                    input_height = st.session_state.input_height, progress_text = progress_text, progress_text2 = progress_text2)

if st.session_state.submitted or st.session_state.first_submitted:
    if uploaded_file is not None:
        # Get actual image file
        bytes_data = get_image_path(uploaded_file)
        # ReSize
        input_height = cv2.resize(cv2.imread(bytes_data, cv2.IMREAD_ANYDEPTH), (dim, dim))/65536
        st.session_state.input_height = input_height
    else:
        st.session_state.input_height = np.ones(shape=(dim, dim))*plainx/100
     
if st.session_state.input_height is not None and (st.session_state.submitted or st.session_state.first_submitted):
    click_submit()

if st.session_state.input_height is not None:
    color_continuous_scale=[(0,'rgb(23, 23, 121)'), (0.25, 'rgb(0, 166, 80)'), (0.5,'rgb(216, 218, 120)'), (0.75,'rgb(98, 64, 57)'), (1,'rgb(255, 255, 255)')]
    if not threeD:
        input_map = go.Figure(data=go.Contour(z=st.session_state.input_height*4000, colorscale=color_continuous_scale))
        input_map.add_hline(y=0.375*dim, line_width=3, line_dash="dash", line_color="black")
        input_map.add_hline(y=(1-0.375)*dim, line_width=3, line_dash="dash", line_color="black")
        input_map.add_vline(x=0.375*dim, line_width=3, line_dash="dash", line_color="black")
        input_map.add_vline(x=(1-0.375)*dim, line_width=3, line_dash="dash", line_color="black")
    else:
        input_map = go.Figure(data=[go.Surface(z=st.session_state.input_height*4000, colorscale=color_continuous_scale)])
    input_map.update_layout(height = 700, title_text='Input' if not CHN else "输入高度图", title_x=0.5, title_xanchor= 'center')
    colm1.plotly_chart(input_map, use_container_width=True)

if st.session_state.output_height is not None:
    color_continuous_scale=[(0,'rgb(23, 23, 121)'), (0.25, 'rgb(0, 166, 80)'), (0.5,'rgb(216, 218, 120)'), (0.75,'rgb(98, 64, 57)'), (1,'rgb(255, 255, 255)')]
    if not threeD:
        output_map = go.Figure(data=go.Contour(z=cv2.resize(st.session_state.output_height,(512,512))*4000, colorscale=color_continuous_scale))
        output_map.add_hline(y=0.375*512, line_width=3, line_dash="dash", line_color="black")
        output_map.add_hline(y=(1-0.375)*512, line_width=3, line_dash="dash", line_color="black")
        output_map.add_vline(x=0.375*512, line_width=3, line_dash="dash", line_color="black")
        output_map.add_vline(x=(1-0.375)*512, line_width=3, line_dash="dash", line_color="black")
    else:
        output_map = go.Figure(data=[go.Surface(z=cv2.resize(st.session_state.output_height,(512,512))*4000, colorscale=color_continuous_scale)])
    output_map.update_layout(height = 700, title_text='Output' if not CHN else "输出高度图", title_x=0.5, title_xanchor= 'center')
    colm2.plotly_chart(output_map, use_container_width=True)

    worldmap = cv2.resize(st.session_state.output_height, (4096, 4096), interpolation=cv2.INTER_AREA)*65536
    worldmap = cv2.GaussianBlur(worldmap, revise_kernel, 0)
    worldmap16 = worldmap.astype(np.uint16)
    is_success, bufferWM = cv2.imencode(".png", worldmap16)
    io_buf_WM = io.BytesIO(bufferWM)

    _, _, _, col1 = st.columns(4, gap = 'small')
    _, _, _, col2 = st.columns(4, gap = 'small')
    with io_buf_WM as fileWM:
        col1.download_button(label="Download World Map" if not CHN else "下载世界地图", data = fileWM, file_name='World Map.png', mime="image/png",type = 'primary', use_container_width = True)

    terrain = cv2.resize(worldmap[1536:-1536, 1536:-1536], (4096, 4096), interpolation=cv2.INTER_CUBIC)
    terrain = cv2.GaussianBlur(terrain, (int(ks2/2)-1, int(ks2/2)-1), 0)
    terrain = terrain.astype(np.uint16)
    is_success, buffer = cv2.imencode(".png", terrain)
    io_buf = io.BytesIO(buffer)

    with io_buf as file:
        col2.download_button(label="Download Terrain Height Map" if not CHN else "下载地形高度图", data = file, file_name='Terrain.png', mime="image/png",type = 'primary', use_container_width = True)


st.divider()
footer = '''
For best performance, set resize dimension to 512, set Reverse Kernel Size to 64, and turn on the rain erosion.

Developed by Zhenning Zhao. Contact the Author at [znzhaopersonal@gmail.com](mailto://znzhaopersonal@gmail.com). See tech document [here](https://github.com/znzhao/CS2Terrain).
''' if not CHN else '''
推荐参数：为保证最佳画面表现力，请使用512缩放精度，64位复原平滑卷积核，并打开雨水侵蚀功能。

本地形编辑器由作者调用开源代码制作，无偿提供，不对有效性及后续技术支持提供保证，请谨慎使用。

[点此处](mailto://znzhaopersonal@gmail.com)联系开发者。B站主页：[@红色的青蛙](https://space.bilibili.com/124723924?spm_id_from=333.788.0.0)

详细技术文档请查阅[此文件](https://github.com/znzhao/CS2Terrain)。
'''
st.markdown(footer,unsafe_allow_html=True)

st.session_state.submitted = False
st.session_state.first_submitted = False
