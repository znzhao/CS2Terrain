# Terrain Modifier for the game City Skiline II
# Author: Zhenning Zhao
# Version: 0.30

# Main code for the GUI
import io
import cv2
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_dimensions import st_dimensions
from scipy.interpolate import PchipInterpolator
from algorithm import process_terrain
from utils import remove_duplicates, get_image_path, color_continuous_scale

if 'intpl_val_outnum' not in st.session_state:
        st.session_state.intpl_val_outnum = 0
    
if 'first_run' not in st.session_state:
    st.session_state.first_run = True

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'input_terrain' not in st.session_state:
    st.session_state.input_terrain = np.ones(shape=(4096, 4096))*12.5/100*4000

if 'erode_terrain' not in st.session_state:
    st.session_state.erode_terrain = None

if 'output_terrain' not in st.session_state:
    st.session_state.output_terrain = None

if 'params' not in st.session_state:
    st.session_state.params = None

def gen_basic_panel(CHN):
    basic_panel = st.expander("Basics" if not CHN else "基础参数")
    with basic_panel:
        seed = st.number_input('Random Seed' if not CHN else "随机种子", value = 127, 
                               help='Seed for generating the noise terrain.' if not CHN else "用于生成随机地形的随机种子。")
        noise_weight = st.slider('Noise Weight' if not CHN else "噪声权重", min_value = 0.0, max_value = 1.0, value=0.5,
                                 help='Lower weight means the output terrain will look more like the input terrain, vice versa.'
                                 if not CHN else "权重越低输出地图越接近初始地图， 否则更接近随机地图。")
        min_altitude, max_altitude = st.slider('Output Height Range (meter)' if not CHN else "输出高度范围（米）",
                                                0, 4000, (0, 1800), step = 1, 
                                                help='The altitude range for the output terrain. As a reference, the default plain height is 500 meters.'
                                                if not CHN else "输出地图的海拔范围。作为参考，游戏地形编辑器中的默认海平面高度为500米。")
    return seed, noise_weight, min_altitude, max_altitude

def gen_erosion_panel(CHN):
    erosion_panel = st.sidebar.expander("Erosion Parameters" if not CHN else "侵蚀参数")
    with erosion_panel:
        if not CHN:
            st.info('Turning on the rain erosion will result in better performance, but it will significantly affect the generation speed.')
        else:
            st.info('开启雨水侵蚀功能可以增强山脉画面表现力，但是会显著降低地形生成速度。')
            
        erosion = st.toggle('Apply Rain Erosion' if not CHN else "施加雨水侵蚀", value = False)
        rain_rate = st.number_input('Rain Rate (1/10000)' if not CHN else "降雨量（万分之一）", 
                                    value=8.0, min_value = 0.0, disabled = not erosion, step = 1.0,
                                    help='Higher rain rate will result in more erosion.' if not CHN else 
                                    '降雨量越大，侵蚀效果越强。')/10000.0
        evaporation_rate = st.number_input('Evaporation Rate (1/10000)' if not CHN else "蒸发速率（万分之一）",
                                           value=5.0, min_value=0.0, disabled=not erosion, step = 1.0,
                                           help='Higher evaporation rate will result in less erosion.' if not CHN else 
                                           '蒸发速率越大，侵蚀效果越弱。')/10000.0
        min_height_delta = st.number_input('Min Height Delta' if not CHN else "最小高度差",
                                           value=0.05, min_value=0.0, disabled=not erosion,
                                           help='min height delta will determine the minimum amount of dirt to carry.' if not CHN else 
                                           '最小高度差决定了雨水每次能够下降的最小高度。')
        repose_slope = st.number_input('Repose Slope' if not CHN else "安息角坡度", 
                                       value=0.03, min_value=0.0, disabled=not erosion,
                                       help='Repose slope is the angle such that the sand or rock can be piled into hills.' if not CHN else 
                                       '安息角坡度体现了材料性质，决定了不会发生滑坡现象的最大角度。')
        gravity = st.number_input('Gravity' if not CHN else "重力", 
                                  value=30.0, min_value=0.0, step = 1.0, disabled=not erosion,
                                  help='Higher gravity will result in faster rain dropping.' if not CHN else 
                                       '重力越大，雨水的下落速度也会越大。')
        sediment_capacity = st.number_input('Sediment Capacity' if not CHN else "沉积物容量", 
                                            value=50.0, min_value=0.0, disabled=not erosion, step = 1.0,
                                            help='Higher sediment capacity allows the rain water to carry more sands and rocks.' if not CHN else 
                                            '沉积物容量代表每单位雨水中允许携带的被溶解物的含量上限。')
        dissolving_rate = st.number_input('Dissolving Rate (%)' if not CHN else "溶解速率 (%)", 
                                            value=25.0, min_value=0.0, disabled=not erosion,
                                            help='Higher dissolving rate will dissolve the terrain faster.' if not CHN else 
                                            '溶解速率越大，雨水对地形的侵蚀效果越明显。')/100
        deposition_rate = st.number_input('Deposition Rate (%)' if not CHN else "沉降速率 (%)", 
                                            value= 0.1, min_value=0.0, disabled=not erosion,
                                            help='Higher deposition rate will make the terrain flatter.' if not CHN else 
                                            '沉降速率越大，沙石沉降速度越快，地形越平缓。')/100
        erosion_params = {
            'erosion': erosion,
            'rain_rate': rain_rate,
            'evaporation_rate': evaporation_rate,
            'min_height_delta': min_height_delta,
            'repose_slope': repose_slope,
            'gravity': gravity,
            'sediment_capacity': sediment_capacity,
            'dissolving_rate': dissolving_rate,
            'deposition_rate': deposition_rate,
        }
        return erosion_params

def gen_spline_panel(CHN, sidebar_width, min_altitude, max_altitude):
    def increment_counter():
        st.session_state.intpl_val_outnum += 1
    def decrement_counter():
        if st.session_state.intpl_val_outnum > 0:
            st.session_state.intpl_val_outnum -= 1
        else:
            st.session_state.intpl_val_outnum = 0
    
    spline_panel = st.expander("Spline Curve" if not CHN else "样条曲线")
    with spline_panel:
        if not CHN:
            st.info('By changing the x percentage of the terrain height into the pecent of y, the spline function will change the flatness of the map')
        else:
            st.info('通过将输入高度转换为输出高度，样条曲线将会改变输出地图的平坦度。')
        colx, coly = st.columns(2)
        ocean_lower_x = colx.number_input('Ocean Lower Anchor (m)' if not CHN else "海洋下届锚点 (米)", 
                                          value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True)
        ocean_lower_y = coly.number_input('Ocean Lower Altitude (m)' if not CHN else "海洋下届输出 (米)", 
                                          value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        ocean_upper_x = colx.number_input('Ocean Upper Anchor (m)' if not CHN else "海洋上界锚点 (米)", 
                                          value=300.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        ocean_upper_y = coly.number_input('Ocean Upper Altitude (m)' if not CHN else "海洋上界输出 (米)", 
                                          value=300.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        plain_lower_x = colx.number_input('Plain Lower Anchor (m)' if not CHN else "平原下界锚点 (米)", 
                                          value=325.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        plain_lower_y = coly.number_input('Plain Lower Altitude (m)' if not CHN else "平原下界输出 (米)", 
                                          value=500.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        plain_x       = colx.number_input('Plain Anchor (m)' if not CHN else "平原锚点 (米)", 
                                          value=525.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        plain_y       = coly.number_input('Plain Altitude (m)' if not CHN else "平原输出 (米)", 
                                          value=500.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        plain_upper_x = colx.number_input('Plain Upper Anchor (m)' if not CHN else "平原上界锚点 (米)", 
                                          value=800.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        plain_upper_y = coly.number_input('Plain Upper Altitude (m)' if not CHN else "平原上界输出 (米)", 
                                          value=600.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        mount_lower_x = colx.number_input('Mount Lower Anchor (m)' if not CHN else "山脉下届锚点 (米)", 
                                          value=1200.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        mount_lower_y = coly.number_input('Mount Lower Altitude (m)' if not CHN else "山脉下届输出 (米)", 
                                          value=1000.0, min_value=min_altitude, max_value=max_altitude, step = 1.0)
        mount_upper_x = colx.number_input('Mount Upper Anchor (m)' if not CHN else "山脉上界锚点 (米)", 
                                          value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True)
        mount_upper_y = coly.number_input('Mount Upper Altitude (m)' if not CHN else "山脉上界输出 (米)", 
                                          value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0)

        intpl_x = [ocean_lower_x, ocean_upper_x, plain_lower_x, plain_x, plain_upper_x, mount_lower_x, mount_upper_x]
        intpl_y = [ocean_lower_y, ocean_upper_y, plain_lower_y, plain_y, plain_upper_y, mount_lower_y, mount_upper_y]

        if st.session_state.intpl_val_outnum > 0:
            key_xs = [str("Additional Anchor "+str(i)) for i in range(st.session_state.intpl_val_outnum)]
            key_ys = [str("Additional Altitude "+str(i)) for i in range(st.session_state.intpl_val_outnum)]
            value_xs = [colx.number_input('Additional Anchor (m)' if not CHN else '额外锚点 (米)', value=0.0,
                                          min_value=0.0, max_value=4000.0, step = 1.0, key = key_xs[i]) for i in range(st.session_state.intpl_val_outnum)]
            value_ys = [coly.number_input('Adjusted Altitude (m)' if not CHN else '输出高度 (米)', value=0.0,
                                           min_value=0.0, max_value=4000.0, step = 1.0, key = key_ys[i]) for i in range(st.session_state.intpl_val_outnum)]
            intpl_x = intpl_x + [x for x in value_xs]
            intpl_y = intpl_y + [y for y in value_ys]
        colx.button('Add Anchor' if not CHN else "增加锚点", on_click=increment_counter)
        coly.button('Delete Anchor' if not CHN else "减少锚点", on_click=decrement_counter, disabled=st.session_state.intpl_val_outnum==0)
        intpl_y = [intpl_y[i] for i in sorted(range(len(intpl_x)), key=lambda x: intpl_x[x])]
        intpl_x = sorted(intpl_x)
        intpl_x, intpl_y = remove_duplicates(intpl_x, intpl_y)
        intpl_func = PchipInterpolator(intpl_x, intpl_y)
        oneline = np.linspace(min_altitude, max_altitude, 50).tolist()
        curve = intpl_func(oneline)
        showdata = pd.DataFrame([curve]).T
        colname = 'Initial Height (m)' if not CHN else "初始高度 (米)"
        indname = 'Adjusted Height (m)' if not CHN else "调整高度 (米)"
        showdata.columns = [colname]
        showdata.index = oneline
        showdata.index.name = indname
        
        fig = px.line(showdata, y = colname)
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        fig.update_layout(autosize=True, height = sidebar_width)
        fig.update_layout(title={'text': 'Spline Curve' if not CHN else '样条曲线', 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    return intpl_func

def gen_sidebar():
    def onclick_submit():
        st.session_state.submitted = True
    with st.sidebar:
        CHN = st.sidebar.toggle('CHN/中文', value = False)
        st.header("Terrain Setting Parameters" if not CHN else "参数设置")
        sidebar_width = st_dimensions(key="sidebar")
        sidebar_width = sidebar_width['width'] if sidebar_width is not None else 700
        seed, noise_weight, min_altitude, max_altitude = gen_basic_panel(CHN)
        erosion_params = gen_erosion_panel(CHN)
        intpl_func = gen_spline_panel(CHN, sidebar_width, float(min_altitude), float(max_altitude))
        st.sidebar.button("Submit" if not CHN else "提交", on_click=onclick_submit)
        params = {
            'seed': seed,
            'noise_weight': noise_weight,
            'min_altitude': min_altitude,
            'max_altitude': max_altitude,
            'erosion_params': erosion_params,
        }
    return CHN, params, intpl_func



def gen_main_content(CHN, params, intpl_func, main_width):
    def click_submit(input_terrain, progressing_text, progressed_text):
        def check_rerun():
            if params != st.session_state.params:
                return True
            if not np.array_equal(input_terrain, st.session_state.input_terrain):
                return True
            if st.session_state.first_run:
                return True
            return False
        if check_rerun():
            st.session_state.params = params
            st.session_state.input_terrain = input_terrain
            st.session_state.erode_terrain = process_terrain(CHN, params, 
                                                            input_terrain = st.session_state.input_terrain, 
                                                            progressing_text = progressing_text, 
                                                            progressed_text = progressed_text)
        st.session_state.output_terrain = intpl_func(st.session_state.erode_terrain)

    # Main content
    st.title("Cities Skyline II Terrain Modifier" if not CHN else "城市天际线2：地形生成器")
    uploaded_file = st.file_uploader("Upload terrain height map (PNG)." if not CHN else "上传初始地形图（PNG）", type= ['png'] )
    threeD = st.toggle('3D Plot' if not CHN else "展示3D视图", value = False)
    colm1, colm2 = st.columns(2)
    progressing_text = 'Erosion in progress. Please wait.' if not CHN else '侵蚀模型处理中，请稍后...'
    progressed_text = 'Erosion finished.' if not CHN else '侵蚀模型处理完成。'

    if st.session_state.submitted or st.session_state.first_run:
        if uploaded_file is not None:
            # Get actual image file
            bytes_data = get_image_path(uploaded_file)
            input_terrain = cv2.resize(cv2.imread(bytes_data, cv2.IMREAD_ANYDEPTH), (4096, 4096))
            input_terrain = input_terrain/65536*4000
        else: 
            input_terrain = np.ones(shape=(4096, 4096))*12.5/100*4000
    
        click_submit(input_terrain, progressing_text, progressed_text)
        st.session_state.submitted = False

    if st.session_state.input_terrain is not None:
        input_plot_terrain = cv2.resize(st.session_state.input_terrain, (512, 512))
        if not threeD:
            input_map = go.Figure(data=go.Contour(z=input_plot_terrain, colorscale=color_continuous_scale))
            input_map.add_hline(y=0.375*512, line_width=3, line_dash="dash", line_color="black")
            input_map.add_hline(y=(1-0.375)*512, line_width=3, line_dash="dash", line_color="black")
            input_map.add_vline(x=0.375*512, line_width=3, line_dash="dash", line_color="black")
            input_map.add_vline(x=(1-0.375)*512, line_width=3, line_dash="dash", line_color="black")
        else:
            input_map = go.Figure(data=[go.Surface(z=input_plot_terrain, colorscale=color_continuous_scale)])
        input_map.update_layout(height = main_width/2, title_text='Input' if not CHN else "输入高度图", title_x=0.5, title_xanchor= 'center')
        colm1.plotly_chart(input_map, use_container_width=True)
    
    if st.session_state.output_terrain is not None:
        output_plot_terrain = cv2.resize(st.session_state.output_terrain, (512, 512))
        if not threeD:
            output_map = go.Figure(data=go.Contour(z=output_plot_terrain, colorscale=color_continuous_scale))
            output_map.add_hline(y=0.375*512, line_width=3, line_dash="dash", line_color="black")
            output_map.add_hline(y=(1-0.375)*512, line_width=3, line_dash="dash", line_color="black")
            output_map.add_vline(x=0.375*512, line_width=3, line_dash="dash", line_color="black")
            output_map.add_vline(x=(1-0.375)*512, line_width=3, line_dash="dash", line_color="black")
        else:
            output_map = go.Figure(data=[go.Surface(z=output_plot_terrain, colorscale=color_continuous_scale)])
        output_map.update_layout(height = main_width/2, title_text='Output' if not CHN else "输出高度图", title_x=0.5, title_xanchor= 'center')
        colm2.plotly_chart(output_map, use_container_width=True)

    if st.session_state.first_run:
        st.session_state.first_run = False

    # Download World Map
    revise_kernel = (31, 31)
    world_map = st.session_state.output_terrain/4000*65536
    world_map = cv2.GaussianBlur(world_map, revise_kernel, 0)
    world_map16 = world_map.astype(np.uint16)
    is_success, buffer_WM = cv2.imencode(".png", world_map16)
    io_buf_WM = io.BytesIO(buffer_WM)

    _, _, _, col1 = st.columns(4, gap = 'small')
    _, _, _, col2 = st.columns(4, gap = 'small')
    with io_buf_WM as fileWM:
        col1.download_button(label="Download World Map" if not CHN else "下载世界地图", 
                             data = fileWM, file_name='World Map.png', mime="image/png",
                             type = 'primary', use_container_width = True)

    # Download Terrain Map
    terrain_map = cv2.resize(world_map[1536:-1536, 1536:-1536], (4096, 4096), interpolation=cv2.INTER_CUBIC)
    terrain_map = cv2.GaussianBlur(terrain_map, revise_kernel, 0)
    terrain_map = terrain_map.astype(np.uint16)
    is_success, buffer_TM = cv2.imencode(".png", terrain_map)
    io_buf = io.BytesIO(buffer_TM)
    with io_buf as file:
        col2.download_button(label="Download Terrain Height Map" if not CHN else "下载地形高度图", 
                             data = file, file_name='Terrain.png', mime="image/png",
                             type = 'primary', use_container_width = True)


def main():
    st.set_page_config(layout="wide")
    main_width = st_dimensions(key="main") 
    main_width = main_width['width'] if main_width is not None else 1400
    CHN, params, intpl_func = gen_sidebar()
    gen_main_content(CHN, params, intpl_func, main_width)
    st.divider()
    footer = '''
    The square surrounded by the dashed lines in the middle of output preview denotes the constructable area of the game. 

    Be Careful! World map and terrain height map are different! The world map denotes the map surrounding the constructable area. You CANNOT build on the world map.
    Terrain height map denotes the map for the constructable area, which is the main area for you to construct your city. Both maps are required to be downloaded and loaded correctly into the game for the best terrain performance. 

    Developed by Zhenning Zhao. Contact the Author at [znzhaopersonal@gmail.com](mailto://znzhaopersonal@gmail.com). See tech document [here](https://github.com/znzhao/CS2Terrain).
    ''' if not CHN else '''
    输出预览中心被虚线包围的方形区域代表游戏中的可建造范围。

    请注意：世界地图指的是游戏中作为背景的不可建造区域。地形高度图指的是游戏中的可建造范围。两者必须同时下载并正确导入游戏才可以正常显示地图。

    为保证最佳画面表现力，请打开雨水侵蚀功能。

    本地形编辑器由作者调用开源代码制作，无偿提供，不对有效性及后续技术支持提供保证，请谨慎使用。

    [点此处](mailto://znzhaopersonal@gmail.com)联系开发者。B站主页：[@红色的青蛙](https://space.bilibili.com/124723924?spm_id_from=333.788.0.0)

    详细技术文档请查阅[此文件](https://github.com/znzhao/CS2Terrain)。
    '''
    st.markdown(footer,unsafe_allow_html=True)


    
if __name__ == '__main__':
    main()