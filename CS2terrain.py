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
from rivers import add_rivers_to_terrain
from presets import preset_linear, preset_plain, preset_canyon, preset_plateau, preset_riverbend, preset_reverse
from utils import remove_duplicates, get_image_path, color_continuous_scale

if 'CHN' not in st.session_state:
    st.session_state.CHN = False

if 'show_warning' not in st.session_state:
    st.session_state.show_warning = True

if 'intpl_val_out_num' not in st.session_state:
        st.session_state.intpl_val_out_num = 0

if 'river_num' not in st.session_state:
        st.session_state.river_num = 0
    
if 'first_run' not in st.session_state:
    st.session_state.first_run = True

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if 'rerun' not in st.session_state:
    st.session_state.rerun = False

if 'input_terrain' not in st.session_state:
    st.session_state.input_terrain = np.ones(shape=(4096, 4096))*12.5/100*4000

if 'erode_terrain' not in st.session_state:
    st.session_state.erode_terrain = None

if 'output_terrain' not in st.session_state:
    st.session_state.output_terrain = None

if 'params' not in st.session_state:
    st.session_state.params = None

def show_warning(CHN):
    warning_title = 'Notice' if not CHN else '注意事项'
    warning_text = '''
    - The square surrounded by the dashed lines in the middle of output preview denotes the constructable area of the game. 
    - `terrain.png` is the map for the constructable area, while `world map.png` is the map surrounding the constructable area.
    - Download both `terrain.png` and `world map.png`. Both maps are required to be downloaded and loaded correctly into the game.
    - Put both files under `C:\\Users\\%username\\AppData\\LocalLow\\Colossal Order\\Cities Skylines II\\Heightmaps`, 
      where `%username` is the username of your own computer.
    - For best terrain performance, please turn on the rain erosion.
    
    ---
    This website is open-source and free to use. Please note that technical support is not guaranteed. Use at your own risk.
    
    See tech document [here](https://github.com/znzhao/CS2Terrain).
    ''' if not CHN else '''
    - 输出预览中心被虚线包围的区域代表游戏中的可建造范围。
    - 世界地图指的是游戏中作为背景的不可建造区域。地形高度图指的是游戏中的可建造范围。两者必须同时下载并正确导入游戏才可以正常显示地图。
    - 下载后将两张png灰度图放入以下文件夹：`C:\\Users\\%username\\AppData\\LocalLow\\Colossal Order\\Cities Skylines II\\Heightmaps`
      其中`%username`是个人电脑的用户名。
    - 为保证最佳画面表现力，请打开雨水侵蚀功能。

    ---
    本地形编辑器由作者调用开源代码制作，无偿提供，不对有效性及后续技术支持提供保证，请谨慎使用。

    B站主页：[@红色的青蛙](https://space.bilibili.com/124723924?spm_id_from=333.788.0.0)
    详细技术文档请查阅[此文件](https://github.com/znzhao/CS2Terrain)。
    '''
    @st.dialog(warning_title)
    def warning(warning_text):
        st.markdown(warning_text)
    warning(warning_text)

def gen_basic_panel(CHN):
    basic_panel = st.expander("Basics" if not CHN else "基础参数")
    with basic_panel:
        uploaded_file = st.file_uploader("Upload terrain height map (PNG)." if not CHN else "上传初始地形图（PNG）", type= ['png'] )
        seed = st.number_input('Random Seed' if not CHN else "随机种子", value = 127, 
                               help='Seed for generating the noise terrain.' if not CHN else "用于生成随机地形的随机种子。")
        noise_weight = st.slider('Noise Weight' if not CHN else "噪声权重", min_value = 0.0, max_value = 1.0, value=0.5,
                                 help='Lower weight means the output terrain will look more like the input terrain, vice versa.'
                                 if not CHN else "权重越低输出地图越接近初始地图， 否则更接近随机地图。")
        min_altitude, max_altitude = st.slider('Output Height Range (meter)' if not CHN else "输出高度范围（米）",
                                                0, 4000, (0, 1800), step = 1, 
                                                help='The altitude range for the output terrain. As a reference, the default plain height is 500 meters.'
                                                if not CHN else "输出地图的海拔范围。作为参考，游戏地形编辑器中的默认海平面高度为500米。")
    return seed, noise_weight, min_altitude, max_altitude, uploaded_file


def gen_erosion_panel(CHN):
    erosion_panel = st.expander("Erosion Parameters" if not CHN else "侵蚀参数")
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
                                           value=10.0, min_value=0.0, disabled=not erosion, step = 1.0,
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
                                  value=10.0, min_value=0.0, step = 1.0, disabled=not erosion,
                                  help='Higher gravity will result in faster rain dropping.' if not CHN else 
                                       '重力越大，雨水的下落速度也会越大。')
        sediment_capacity = st.number_input('Sediment Capacity' if not CHN else "沉积物容量", 
                                            value=50.0, min_value=0.0, disabled=not erosion, step = 1.0,
                                            help='Higher sediment capacity allows the rain water to carry more sands and rocks.' if not CHN else 
                                            '沉积物容量代表每单位雨水中允许携带的被溶解物的含量上限。')
        dissolving_rate = st.number_input('Dissolving Rate (%)' if not CHN else "溶解速率 (%)", 
                                            value=15.0, min_value=0.0, disabled=not erosion,
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

def gen_spline_panel_erosion(CHN, sidebar_width, min_altitude, max_altitude):
    def increment_counter():
        st.session_state.intpl_val_out_num += 1
    def decrement_counter():
        if st.session_state.intpl_val_out_num > 0:
            st.session_state.intpl_val_out_num -= 1
        else:
            st.session_state.intpl_val_out_num = 0
    
    spline_panel = st.expander("Spline Curve" if not CHN else "重采样曲线")
    with spline_panel:
        if not CHN:
            st.info('By changing the x percentage of the terrain height into the pecent of y, the spline function will change the flatness of the map')
        else:
            st.info('通过将输入高度转换为输出高度，重采样曲线将会改变输出地图的平坦度。')
        colx, coly = st.columns(2)        
        options = ['Plain', 'Riverbend', 'Plateau', 'Canyon', 'Reverse', 'Linear(Customize)', ] if not CHN else ["平原曲线", "河畔曲线", "高原曲线", "峡谷曲线", "倒置曲线", "线性（自定义）"]
        preset_id = options.index(st.selectbox('Preset' if not CHN else "加载预设", options = options, key = 'Post Preset'))   
        colx, coly = st.columns(2)
        if preset_id == 0:
            intpl_x, intpl_y = preset_plain(CHN, colx, coly, min_altitude, max_altitude, key = 'post')
        if preset_id == 1:
            intpl_x, intpl_y = preset_riverbend(CHN, colx, coly, min_altitude, max_altitude, key = 'post')
        if preset_id == 2:
            intpl_x, intpl_y = preset_plateau(CHN, colx, coly, min_altitude, max_altitude, key = 'post')
        if preset_id == 3:
            intpl_x, intpl_y = preset_canyon(CHN, colx, coly, min_altitude, max_altitude, key = 'post')
        if preset_id == 4:
            intpl_x, intpl_y = preset_reverse(CHN, colx, coly, min_altitude, max_altitude, key = 'post')
        if preset_id == 5:
            intpl_x, intpl_y = preset_linear(CHN, colx, coly, min_altitude, max_altitude, key = 'post')

        if st.session_state.intpl_val_out_num > 0:
            key_xs = [str("Additional Final Anchor "+str(i)) for i in range(st.session_state.intpl_val_out_num)]
            key_ys = [str("Additional Final Altitude "+str(i)) for i in range(st.session_state.intpl_val_out_num)]
            value_xs = [colx.number_input('Additional Anchor (m)' if not CHN else '额外最终锚点 (米)', value=0.0,
                                          min_value=0.0, max_value=4000.0, step = 1.0, key = key_xs[i]) for i in range(st.session_state.intpl_val_out_num)]
            value_ys = [coly.number_input('Adjusted Altitude (m)' if not CHN else '输出最终高度 (米)', value=0.0,
                                           min_value=0.0, max_value=4000.0, step = 1.0, key = key_ys[i]) for i in range(st.session_state.intpl_val_out_num)]
            intpl_x = intpl_x + [x for x in value_xs]
            intpl_y = intpl_y + [y for y in value_ys]
        colx.button('Add Anchor' if not CHN else "增加锚点", on_click=increment_counter, use_container_width = True)
        coly.button('Delete Anchor' if not CHN else "减少锚点", on_click=decrement_counter, disabled=st.session_state.intpl_val_out_num==0, use_container_width = True)
        intpl_y = [intpl_y[i] for i in sorted(range(len(intpl_x)), key=lambda x: intpl_x[x])]
        intpl_x = sorted(intpl_x)
        intpl_x, intpl_y = remove_duplicates(intpl_x, intpl_y)
        intpl_func = PchipInterpolator(intpl_x, intpl_y)
        oneline = np.linspace(min_altitude, max_altitude, 100).tolist()
        curve = intpl_func(oneline)
        showdata = pd.DataFrame([curve]).T
        indname = 'Initial Height (m)' if not CHN else "初始高度 (米)"
        colname = 'Adjusted Height (m)' if not CHN else "调整高度 (米)"
        showdata.columns = [colname]
        showdata.index = oneline
        showdata.index.name = indname
        
        fig = px.line(showdata, y = colname)
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        fig.update_layout(autosize=True, height = sidebar_width)
        fig.update_layout(title={'text': 'Spline Curve' if not CHN else '重采样曲线', 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    return intpl_func

def gen_river_panel(CHN):
    def increase_river_num():
        st.session_state.river_num += 1
        st.session_state.rerun = True
    def decrease_river_num():
        if st.session_state.river_num > 0:
            st.session_state.river_num -= 1
        else:
            st.session_state.river_num = 0
        st.session_state.rerun = True

    river_panel = st.expander("River Generation" if not CHN else "河流生成")
    with river_panel:
        river_params = None
        radius = st.number_input('Radius' if not CHN else "采样半径", value = 0.02, step = 0.01, max_value=0.2, min_value=0.01,
                    help='Radius of the Possion Disk Sampling.' if not CHN else "泊松盘采样半径。", disabled=st.session_state.river_num == 0)
        
        colx, coly = st.columns(2)
        colx.button('Add River' if not CHN else "增加河流", on_click=increase_river_num, use_container_width = True)
        coly.button('Delete River' if not CHN else "减少河流", on_click=decrease_river_num, disabled=st.session_state.river_num==0, use_container_width = True)
        
        if st.session_state.river_num > 0:
            if not CHN:
                if st.session_state.river_num > 1:
                    river_labels = ["River " + str(i) for i in range(st.session_state.river_num)] 
                else:
                    river_labels = ["River 0"]
            else:
                if st.session_state.river_num > 1:
                    river_labels = ["河流 " + str(i) for i in range(st.session_state.river_num)]
                else:
                    river_labels = ["河流 0"]

            tabs = st.tabs(river_labels)
            key_seeds = [str("River Source Seed"+str(i)) for i in range(st.session_state.river_num)]
            key_source_xs = [str("River Source x"+str(i)) for i in range(st.session_state.river_num)]
            key_source_ys = [str("River Source y"+str(i)) for i in range(st.session_state.river_num)]
            key_estuary_xs = [str("River Estuary x"+str(i)) for i in range(st.session_state.river_num)]
            key_estuary_ys = [str("River Estuary y"+str(i)) for i in range(st.session_state.river_num)]
            key_length = [str("River Length"+str(i)) for i in range(st.session_state.river_num)]
            key_bifur = [str("River Bifur"+str(i)) for i in range(st.session_state.river_num)]
            key_fracs = [str("River Frac"+str(i)) for i in range(st.session_state.river_num)]
            key_magnitudes = [str("River Magnitude"+str(i)) for i in range(st.session_state.river_num)]
            key_river_widths = [str("River Width"+str(i)) for i in range(st.session_state.river_num)]
            key_river_deepths = [str("River Deepth"+str(i)) for i in range(st.session_state.river_num)]
            
            river_seeds = []
            source_xs = []
            source_ys = []
            estuary_xs = []
            estuary_ys = []
            river_lengths = []
            prob_bifurs = []
            fracs = []
            magnitudes = []
            river_widths = []
            river_deepths = []
            
            for i, tab in enumerate(tabs):
                with tab:
                    river_seed = st.number_input('River Seed' if not CHN else "随机河流种子", value = 0, key = key_seeds[i],
                        help='Seed for generating the noise terrain.' if not CHN else "用于生成河流的随机种子。")

                    colx, coly = st.columns(2)
                    source_x = colx.number_input('River Source Coordinate (X)' if not CHN else '水源点坐标 (x轴)', value=0.0,
                                                min_value=0.0, max_value = 511.0, step = 1.0, key = key_source_xs[i])
                    source_y = coly.number_input('River Source Coordinate (Y)' if not CHN else '水源点坐标 (y轴)', value=0.0,
                                                min_value=0.0, max_value = 511.0, step = 1.0, key = key_source_ys[i])

                    estuary_x = colx.number_input('River Estuary Coordinate (X)' if not CHN else '汇入点坐标 (x轴)', value=0.0,
                                                min_value=0.0, max_value = 511.0, step = 1.0, key = key_estuary_xs[i])
                    estuary_y = coly.number_input('River Estuary Coordinate (Y)' if not CHN else '汇入点坐标 (y轴)', value=0.0,
                                                min_value=0.0, max_value = 511.0, step = 1.0, key = key_estuary_ys[i])
                    length = st.number_input('River Max Length' if not CHN else "河流最大长度", min_value = 1, value = 7, key = key_length[i],
                        help='The maximum length of the generated river.'
                                if not CHN else "河流生成的最大长度。")
                    prob_bifur = st.slider('Probability of Bifurcation' if not CHN else "分流概率", 
                        min_value = 0.0, max_value = 1.0, value = 0.5, key = key_bifur[i],
                        help='The probability of having a bifurcation of the river path.'
                        if not CHN else "河流分流产生支流的概率。")
                    frac = st.slider('Fracs' if not CHN else "分形次数", min_value = 1, max_value = 7, value = 2, key = key_fracs[i],
                        help='Number of fracs to break the linear feature of the river.'
                        if not CHN else "分形次数决定了河流的线性程度。")
                    magnitude = st.slider('Magnitude' if not CHN else "扰动程度", min_value = 0.0, max_value = 1.0, value = 0.9, key = key_magnitudes[i],
                        help='Magnitude of river noisiness.'
                        if not CHN else "河流的噪声程度。")
                    river_width = st.slider('River Width' if not CHN else "河流宽度", min_value = 0.0, max_value = 4.0, value = 2.0, key = key_river_widths[i],)
                    river_deepth = st.slider('River Deepth' if not CHN else "河流深度", min_value = 0, max_value = 500, value = 200, key = key_river_deepths[i],)
                river_seeds.append(river_seed)
                source_xs.append(source_x/512*1024)
                source_ys.append(source_y/512*1024)
                estuary_xs.append(estuary_x/512*1024)
                estuary_ys.append(estuary_y/512*1024)
                river_lengths.append(length)
                prob_bifurs.append(prob_bifur)
                fracs.append(frac)
                magnitudes.append(magnitude)
                river_widths.append(river_width)
                river_deepths.append(river_deepth)
            river_params = {
                'radius': radius,
                'n_rivers': st.session_state.river_num,
                'river_seeds': river_seeds,
                'source_xs': source_xs,
                'source_ys': source_ys,
                'estuary_xs': estuary_xs,
                'estuary_ys': estuary_ys,
                'river_lengths': river_lengths,
                'prob_bifurs': prob_bifurs,
                'fracs': fracs,
                'magnitudes': magnitudes,
                'river_widths': river_widths,
                'river_depths': river_deepths,
                }
        return river_params

@st.fragment
def fragmented_sidebar():
    def onclick_submit():
        st.session_state.submitted = True
        st.session_state.rerun = True
    def on_change():
        st.session_state.show_warning = True
        st.session_state.rerun = True
        
    CHN = st.toggle('ENG/中文', value = False, on_change = on_change)
    st.session_state.CHN = CHN
    st.header("Terrain Setting Parameters" if not CHN else "参数设置")
    sidebar_width = st_dimensions(key="sidebar")
    sidebar_width = sidebar_width['width'] if sidebar_width is not None else 700
    seed, noise_weight, min_altitude, max_altitude, uploaded_file = gen_basic_panel(CHN)
    erosion_params = gen_erosion_panel(CHN)
    intpl_func_final = gen_spline_panel_erosion(CHN, sidebar_width, float(min_altitude), float(max_altitude))
    river_params = gen_river_panel(CHN)
    st.button("Submit" if not CHN else "提交", on_click=onclick_submit)
    params = {
        'seed': seed,
        'noise_weight': noise_weight,
        'min_altitude': min_altitude,
        'max_altitude': max_altitude,
        'erosion_params': erosion_params,
    }
    if st.session_state.rerun:
        st.session_state.rerun = False
        st.rerun()
    return CHN, params, intpl_func_final, river_params, uploaded_file

def gen_sidebar():
    with st.sidebar:
        CHN, params, intpl_func_final, river_params, uploaded_file = fragmented_sidebar()
    return CHN, params, intpl_func_final, river_params, uploaded_file
        
def gen_main_content(CHN, uploaded_file, params, intpl_func_final, river_params, main_width):
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
        if river_params is None:
            output_terrain_no_river = intpl_func_final(st.session_state.erode_terrain)
            st.session_state.output_terrain = output_terrain_no_river
        else:
            output_terrain_no_river = intpl_func_final(st.session_state.erode_terrain)
            river_terrain = add_rivers_to_terrain(st.session_state.erode_terrain, params, river_params)
            st.session_state.output_terrain = np.clip(output_terrain_no_river - river_terrain, 0, 4000)
            
    # Main content
    st.title("Cities Skyline II Terrain Modifier" if not CHN else "城市天际线2：地形美化工具")
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
        input_map.update_layout(height = main_width/2, title_text='Input' if not CHN else "输入高度图", title_x = 0.5, title_xanchor = 'center')
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
    CHN, params, intpl_func_final, river_params, uploaded_file = gen_sidebar()
    gen_main_content(CHN, uploaded_file, params, intpl_func_final, river_params, main_width)
    if st.session_state.show_warning:
        show_warning(st.session_state.CHN)
        st.session_state.show_warning = False
    
if __name__ == '__main__':
    main()
