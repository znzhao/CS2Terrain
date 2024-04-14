# Terrain Modifier for Cities Skyline II
# 城市天际线II地形美化工具

The Terrain Modifier for Cities Skyline II is a Python-based tool using Streamlit, designed to enhance and adjust terrain heightmaps for use in the game "Cities Skyline II". It provides users with a variety of parameters to tweak and apply different terrain characteristics such as noise adjustment, erosion effects, and custom terrain anchoring. The modified map with rain erosion applied will have exceptionally realistic terrain effects.

城市天际线II地形修改器是一个基于Python的工具，旨在增强和调整由游戏《城市天际线II》生成的地形高程图。它为用户提供了各种参数，可以调整和应用不同的地形特征，如噪声调整、侵蚀效果和自定义地形锚定。施加了雨水侵袭过程的修改地图将会拥有极佳的真实地形效果。

## Features
- Interactive UI: Built using Streamlit, the tool provides a user-friendly interface for adjusting terrain settings.
- Multi-Language Support: Supports both English and Chinese languages.
- Custom Terrain Generation: Allows the user to manipulate terrain using noise and smoothing filters.
- Erosion Simulation: Apply rain erosion effects to simulate natural terrain erosion.
- 3D Visualization: Toggle between 2D and 3D views to visualize the terrain.
- Custom Anchors: Dynamically add or remove anchors to shape the terrain's height profile.

## Parameter Instruction / 参数控制

### Basic / 基础噪声参数
1. **Random Seed / 随机种子:**
   - This parameter controls the random seed used for generating the terrain.
   - 此参数控制用于生成地形的随机种子。改变种子将会在地形中产生不同的随机模式。

2. **Signal Average Kernel Size / 信号平滑卷积核:**
   - This parameter determines the size of the kernel used for averaging input terrain. Increasing the kernel size will result in a smoother terrain, while decreasing it will retain more input detail.
   - 此参数确定用于平滑输入地形的卷积核的大小。增加卷积核大小将会产生更平滑的地形，而减小大小将会保留更多输入细节，但可能引入噪音。

3. **Initial Terrain Weight / 初始地形权重:**
   - This parameter controls the weight of the initial terrain. A larger value will give more influence to the initial terrain, resulting in terrain that resembles the initial state more closely.
   - 此参数控制初始地形的权重。较大的值将会赋予初始地形更大的影响力，导致地形更接近初始状态。

4. **Noise Terrain Weight / 噪声地形权重:**
   - This parameter controls the weight of the noise in the terrain. Increasing the value will amplify the influence of noise, leading to a more rugged terrain
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

### Detail Richness / 细节丰富度
This panel gets the anchored points for interpolating a detail richness curve, which defines the degree of detail richness according to the altitude of the input height. The curve contains at least 3 given anchors (ocean, plain, and mountain) and optional outside anchors.

这个板块获取了用于插值细节丰富度曲线的锚定点，该曲线根据输入高度的海拔定义了细节丰富度的程度。该曲线至少包含3个给定的锚定点（海洋、平原和山脉），以及可选的外部锚定点。

The ocean and mountain anchor is fixed at 0% and 100% of the possible height allowed by CS2 (0, 65536). The default plain altitude is at 12.5%, which is the initial height given by CS2 in-game terrain editor, however the player can change the place of the plain anchor.

海洋和山脉的锚定点固定在 CS2 允许的可能高度范围（0到65536）的 0% 和 100% 处。默认的平原海拔高度为 12.5%，这是 CS2 游戏地形编辑器中给出的初始高度，然而玩家可以自行改变平原锚点的位置。

### Rain Erosion / 雨水侵蚀作用

**Attension! Applying rain erosion is crucial to generating more realistic terrain. However, applying rain erosion could significantly affect the amount of time for the algorithm to run. For best performance, turn on the erosion with resize dimension smaller than or equal to 512, but turn it off for larger dimensions.**

**注意！施加雨水侵蚀对生成更逼真的地形至关重要。然而，施加雨水侵蚀可能会显著影响算法的运行时间。为了获得最佳性能，在缩放精度小于或等于512的情况下打开侵蚀，但对于更大的尺寸则应选择关闭。**

1. **Apply Rain Erosion / 施加雨水侵蚀:**
    - This parameter toggles the application of rain erosion on the terrain. When enabled, rain erosion will be applied to the terrain, modifying its features over time.
    - 此参数切换是否在地形上应用雨水侵蚀。当启用时，将对地形应用雨水侵蚀，随着时间的推移修改其特征。

2. **Full Width / 降雨范围:**
    - This parameter defines the range over which rain erosion will occur. Increasing it will extend the area affected by rain erosion.
    - 此参数定义雨水侵蚀发生的范围。增加它将扩大受雨水侵蚀影响的区域。

3. **Rain Rate (1/10000) / 降雨量（万分之一）:**
    - This parameter controls the rate of rainfall used in the erosion simulation. Increasing it will result in more erosion over time.
    - 此参数控制侵蚀模拟中使用的降雨量。随着时间的推移，增加它将导致更多的侵蚀。

4. **Evaporation Rate (1/10000) / 蒸发速率（万分之一）:**
    - This parameter controls the rate of evaporation of water in the erosion simulation. Increasing it will cause water to evaporate more quickly, affecting the erosion process.
    - 此参数控制侵蚀模拟中水的蒸发速率。增加它将导致水更快地蒸发，从而影响侵蚀过程。

5. **Min Height Delta / 最小高度差:**
    - This parameter defines the minimum height difference required for erosion to occur. Increasing it will require larger height differences for erosion to take place.
    - 此参数定义了侵蚀发生所需的最小高度差。增加它将需要更大的高度差才能发生侵蚀。

6. **Repose Slope / 休止坡度:**
    - This parameter controls the slope at which sediment is deposited during erosion. Increasing it will result in sediment being deposited at steeper slopes.
    - 此参数控制侵蚀过程中沉积物沉积的坡度。增加它将导致沉积物沉积在更陡峭的坡度上。

7. **Gravity / 重力:**
    - This parameter controls the strength of gravity in the erosion simulation. Increasing it will result in more pronounced effects of gravity on the erosion process.
    - 此参数控制侵蚀模拟中重力的强度。增加它将导致重力对侵

## Methodology
TBD.
