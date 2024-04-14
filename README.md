# Terrain Modifier for Cities Skyline II
The Terrain Modifier for Cities Skyline II is a Python-based tool using Streamlit, designed to enhance and adjust terrain heightmaps for use in the game "Cities Skyline II". It provides users with a variety of parameters to tweak and apply different terrain characteristics such as noise adjustment, erosion effects, and custom terrain anchoring.

## Features
- Interactive UI: Built using Streamlit, the tool provides a user-friendly interface for adjusting terrain settings.
- Multi-Language Support: Supports both English and Chinese languages.
- Custom Terrain Generation: Allows the user to manipulate terrain using noise and smoothing filters.
- Erosion Simulation: Apply rain erosion effects to simulate natural terrain erosion.
- 3D Visualization: Toggle between 2D and 3D views to visualize the terrain.
- Custom Anchors: Dynamically add or remove anchors to shape the terrain's height profile.

1. **Random Seed / 随机种子:**
   - This parameter controls the random seed used for generating the terrain. Changing the seed will produce different random patterns in the terrain. A larger seed value will result in a different set of random numbers being generated, leading to a different terrain.
   - 此参数控制用于生成地形的随机种子。改变种子将会在地形中产生不同的随机模式。较大的种子值将导致生成不同的随机数集，从而产生不同的地形。

2. **Signal Average Kernel Size / 信号平滑卷积核:**
   - This parameter determines the size of the kernel used for signal averaging. Increasing the kernel size will result in a smoother terrain, while decreasing it will retain more detail but may introduce noise.
   - 此参数确定用于信号平滑的卷积核的大小。增加卷积核大小将会产生更平滑的地形，而减小大小将会保留更多细节，但可能引入噪音。

3. **Initial Terrain Weight / 初始地形权重:**
   - This parameter controls the weight of the initial terrain. A larger value will give more influence to the initial terrain, resulting in terrain that resembles the initial state more closely.
   - 此参数控制初始地形的权重。较大的值将会赋予初始地形更大的影响力，导致地形更接近初始状态。

4. **Noise Terrain Weight / 噪声地形权重:**
   - This parameter controls the weight of the noise in the terrain. Increasing the value will amplify the influence of noise, leading to a more rugged terrain, while decreasing it will result in a smoother terrain.
   - 此参数控制地形中噪声的权重。增加该值将放大噪声的影响，导致地形更加崎岖，而减小它将导致地形更加平滑。

5. **Resize Dimension / 缩放精度:**
   - This parameter determines the dimensions to which the terrain is resized. A larger dimension will result in higher resolution but may slow down processing speed.
   - 此参数确定地形调整到的尺寸。较大的尺寸将会产生更高的分辨率，但可能会降低处理速度。

6. **Reverse Kernel Size / 复原平滑卷积核:**
   - This parameter determines the size of the kernel used for reverse smoothing. Increasing the kernel size will result in a smoother terrain after erosion.
   - 此参数确定用于反向平滑的卷积核的大小。增加卷积核大小将导致侵蚀后的地形更加平滑。

7. **Output Height Range (meter) / 输出高度范围（米）:**
   - This parameter defines the range of heights in the output terrain. Changing this range will affect the overall elevation of the terrain.
   - 此参数定义输出地形的高度范围。改变这个范围将影响地形的整体海拔高度。
  
## Methodology
TBD.
