# Terrain Modifier for Cities Skyline II / 城市天际线II地形美化工具

The Terrain Modifier for Cities Skyline 2 (CS2) is a Python-based tool using Streamlit, designed to enhance and adjust terrain heightmaps for use in the game "Cities Skyline II". It provides users with a variety of parameters to tweak and apply different terrain characteristics such as noise adjustment, erosion effects, and custom terrain anchoring. The modified map with rain erosion applied will have exceptionally realistic terrain effects.

城市天际线II地形修改器是一个基于Python的工具，旨在增强和调整由游戏《城市天际线II》生成的地形高程图。它为用户提供了各种参数，可以调整和应用不同的地形特征，如噪声调整、侵蚀效果和自定义地形锚定。施加了雨水侵袭过程的修改地图将会拥有极佳的真实地形效果。

## Instructions / 使用方法

1. Open CS2. Use the map editor to roughly adjust the terrain's height by raising or lowering it. Detailed terrain changes manually in-game are unnecessary. The algorithm will add details to the rough map later.

   打开CS2。使用地图编辑器大致抬高或降低地形的高度。在游戏中不需要手动进行详细的地形更改。算法将在稍后向粗略地图添加细节。

2. Export the height map. Open the following folder: "C:\Users%username\AppData\LocalLow\Colossal Order\Cities Skylines II\Heightmaps". You should see the height map that you just exported.

   导出高度图。打开以下文件夹：“C:\Users%username\AppData\LocalLow\Colossal Order\Cities Skylines II\Heightmaps”。您应该看到刚刚导出的高度图。

3. Open the [Terrain Modifier for Cities Skyline II](https://cs2terrain.streamlit.app/). Upload the height map that you just exported.

   打开城市天际线II地形修改器。上传刚刚导出的地形修改器。

4. Customize the parameters. For optimal in-game terrain performance, enable rain erosion with a resize dimension $\leq$ 512. When you find the output terrain meets your requirements, export the output height map to the same folder.

   自定义调整参数。为了获得最佳的游戏地形性能，请将雨水侵蚀功能打开，并将缩放尺寸设为 $\leq$ 512。当您发现输出地形满足您的要求时，将输出高度图导出到同一文件夹。

5. Restart the game and enter the map editor. Import the exported height map in-game. Use the in-game blur brush to gently blur the entire map. This should give you a randomly generated unique map with vivid mountains.

   重新启动游戏并进入地图编辑器。在游戏中导入导出的高度图。使用游戏内的模糊画笔轻轻涂抹整个地图。这样应该会给您一个独一无二的拥有壮丽山脉的随机生成地图。

6. Build your city as you wish. Enjoy!

   尽情建设您的城市吧！

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

## Tech Details / 技术细节

This program modifies the height map generated from CS2 according to the following procedure:

该程序根据以下步骤修改从CS2生成的高度图：

1. The height map generated by CS2 has a size of $4096\times 4096$. For the sake of program speed, resize the height map to the specified dimensions.

   城市天际线2中生成的高度图大小为$4096\times 4096$。出于程序速度的考虑，将高度图调整大小到指定的尺寸。

2. Apply average blur to the height map. This results in a smoother input height map. Normalize the range of the height map to (0,1).

   对高度图应用平均模糊。这将导致更平滑的输入高度图。将高度图的范围归一化到(0,1)。

3. Randomly generate the detailed mountain texture height according to Fourier-based power law noise with frequency bounds. Normalize the range of the noise map to (0,1).

   根据傅立叶基础的幂律噪声和频率边界随机生成详细的山脉纹理高度。将噪声地图的范围归一化到(0,1)。

4. Use fade interpolation to obtain the detail richness curve. This function maps the percentage of height to the detail richness to be added to this altitude.

   使用渐进插值来获得详细丰富度曲线。此函数将高度的百分比映射到要添加到此高度的详细丰富度。

5. Combine the input height and the noise height according to the equation: $terrain height = weight_{original} \times input + weight_{noise} \times detail\ richness \times noise$

   根据以下方程将输入高度和噪声高度组合起来：$地形高度 = 初始地形权重 \times 初始地形高度 + 细节地形权重 \times 该高程细节丰富度 \times 噪声细节$

6. Apply rain erosion to the height map. The key algorithm comes from Daniel Andrino. Please refer to the [original repository](https://github.com/dandrino/terrain-erosion-3-ways?tab=MIT-1-ov-file) for more details.

   对高度图应用雨水侵蚀。关键算法来自Daniel Andrino。请参阅原始文档以获取更多详细信息。

7. Resize the map to $4096 \times 4096$. Apply another Gaussian blur to the height map to refine the map for resizing.

   将地图调整大小为 $4096 \times 4096$。对高度图应用另一个高斯模糊，以便为调整大小的地图进行精磨。

## MIT License / 版权声明
Copyright (c) 2024 Zhenning Zhao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
