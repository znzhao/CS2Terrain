![image](https://github.com/znzhao/CS2Terrain/blob/main/fig/plain.png?raw=true)
# Terrain Modifier for Cities Skyline II 城市天际线II地形美化工具

The Terrain Modifier for Cities Skyline 2 (CS2) is a Python-based tool using Streamlit, designed to enhance and adjust terrain heightmaps for use in the game "Cities Skyline II". It provides users with a variety of parameters to tweak and apply different terrain characteristics such as noise adjustment, erosion effects, and custom terrain anchoring. The modified map with rain erosion applied will have exceptionally realistic terrain effects.

城市天际线II地形修改器是一个基于Python的工具，旨在增强和调整由游戏《城市天际线II》生成的地形高程图。它为用户提供了各种参数，可以调整和应用不同的地形特征，如噪声调整、侵蚀效果和自定义地形锚定。施加了雨水侵袭过程的修改地图将会拥有极佳的真实地形效果。

## Instructions 使用方法

1. Open CS2. Use the map editor to roughly adjust the terrain's height by raising or lowering it. Detailed terrain changes manually in-game are unnecessary. The algorithm will add details to the rough map later.

   打开CS2。使用地图编辑器大致抬高或降低地形的高度。在游戏中不需要手动进行详细的地形更改。算法将在稍后向粗略地图添加细节。

2. Export the height map. Open the following folder: "C:\Users%username\AppData\LocalLow\Colossal Order\Cities Skylines II\Heightmaps". You should see the height map that you just exported.

   导出高度图。打开以下文件夹：“C:\Users%username\AppData\LocalLow\Colossal Order\Cities Skylines II\Heightmaps”。您应该看到刚刚导出的高度图。

3. Open the [Terrain Modifier for Cities Skyline II](https://cs2terrain.streamlit.app/). Upload the height map that you just exported.

   打开城市天际线II地形修改器。上传刚刚导出的地形修改器。

4. Customize the parameters. For optimal in-game terrain performance, enable rain erosion. When you find the output terrain meets your requirements, export the output height map to the same folder.

   自定义调整参数。为了获得最佳的游戏地形性能，请打开雨水侵蚀功能。当您发现输出地形满足您的要求时，将输出高度图导出到同一文件夹。

5. Restart the game and enter the map editor. Import the exported height map in-game. This should give you a randomly generated unique map with vivid mountains.

   重新启动游戏并进入地图编辑器。在游戏中导入导出的高度图。这样应该会给您一个独一无二的拥有壮丽山脉的随机生成地图。

6. Build your city as you wish. Enjoy!

   尽情建设您的城市吧！

## Parameter Instruction 参数控制

### Basic 基础噪声参数
1. **Random Seed 随机种子:**
   - This parameter controls the random seed used for generating the terrain.
   - 此参数控制用于生成地形的随机种子。改变种子将会在地形中产生不同的随机模式。

2. **Noise Terrain Weight 噪声地形权重:**
   - This parameter controls the weight of the noise terrain. A smaller value will give more influence to the noise terrain, resulting in terrain that resembles the initial state.
   - 此参数控制噪声地形的权重。较小的值将会赋予初始地形更大的影响力，导致地形更接近初始状态。

3. **Output Height Range (meter) 输出高度范围（米）:**
   - This parameter defines the range of heights in the output terrain. Changing this range will affect the overall elevation of the terrain.
   - 此参数定义输出地形的高度范围。改变这个范围将影响地形的整体海拔高度。


### Rain Erosion 雨水侵蚀作用

**Attention! Applying rain erosion is essential for creating realistic terrain. However, it can significantly increase the algorithm's runtime. For optimal results, please proceed with applying rain erosion. Though it may take extra time, the outcome will be worth the wait.**

**注意！ 应用雨蚀对于生成更逼真的地形至关重要。然而，这可能会显著延长算法的运行时间。为了获得最佳效果，请务必应用雨蚀。虽然这可能需要一些额外的等待时间，但最终的结果将是值得的。**

1. **Apply Rain Erosion 施加雨水侵蚀:**
    - This parameter toggles the application of rain erosion on the terrain. When enabled, rain erosion will be applied to the terrain, modifying its features over time.
    - 此参数切换是否在地形上应用雨水侵蚀。当启用时，将对地形应用雨水侵蚀，随着时间的推移修改其特征。

2. **Rain Rate (1/10,000) 降雨量（万分之一）:**
    - This parameter controls the rate of rainfall used in the erosion simulation. Increasing it will result in more erosion over time.
    - 此参数控制侵蚀模拟中使用的降雨量。随着时间的推移，增加它将导致更多的侵蚀。

3. **Evaporation Rate (1/10,000) 蒸发速率（万分之一）:**
    - This parameter controls the rate of evaporation of water in the erosion simulation. Increasing it will cause water to evaporate more quickly, affecting the erosion process.
    - 此参数控制侵蚀模拟中水的蒸发速率。增加它将导致水更快地蒸发，从而影响侵蚀过程。

4. **Min Height Delta 最小高度差:**
    - This parameter defines the minimum height difference required for erosion to occur. Increasing it will require larger height differences for erosion to take place.
    - 此参数定义了侵蚀发生所需的最小高度差。增加它将需要更大的高度差才能发生侵蚀。

5. **Repose Slope 休止坡度:**
    - This parameter controls the slope at which sediment is deposited during erosion. Increasing it will result in sediment being deposited at steeper slopes.
    - 此参数控制侵蚀过程中沉积物沉积的坡度。增加它将导致沉积物沉积在更陡峭的坡度上。

6. **Gravity 重力:**
    - This parameter controls the strength of gravity in the erosion simulation. Increasing it will result in more pronounced effects of gravity on the erosion process.
    - 此参数控制侵蚀模拟中重力的强度。增加它将导致重力对侵。
   
7. **Sediment Capacity 沉积物容量:**
    - Higher sediment capacity allows the rain water to carry more sands and rocks.
    - 沉积物容量代表每单位雨水中允许携带的被溶解物的含量上限。
   
8. **Dissolving Rate (%) 溶解速率 (%):**
    - Higher dissolving rate will dissolve the terrain faster.
    - 溶解速率越大，雨水对地形的侵蚀效果越明显。
      
9. **Deposition Rate (%) 沉降速率 (%):**
    - Higher deposition rate will make the terrain flatter.
    - 沉降速率越大，沙石沉降速度越快，地形越平缓。
   

### Spline Curve 重采样曲线
This panel gets the anchored points for interpolating a resampling curve, which transfrom the terrain according to the curve. The website includes several predetermined curves that behave well, but you can always change the details of each curve by yourself.

这个面板获取了用于插值重采样曲线的锚定点，该曲线将输入的高度转换成输出的高度。网页内置了一部分表现较好的重采样曲线函数。如果对最终地形不满意，则可以通过改变下方的锚定点坐标进行微调。

### River Generation 河流生成
This panel controls river generation. This panel is in beta stage and will be changed in the future.

这个面板获取了控制河流生成。该面板目前还在测试中，未来有计划对其中的功能进行修改。

## Tech Details 技术细节

This program modifies the height map generated from CS2 according to the following procedure:

该程序根据以下步骤修改从CS2生成的高度图：

1. The height map generated by CS2 has a size of $4096\times 4096$. For the sake of program speed, resize the height map to the specified dimensions.

   城市天际线2中生成的高度图大小为 $4096\times 4096$。出于程序速度的考虑，将高度图调整大小到指定的尺寸。

2. Apply average blur to the height map. This results in a smoother input height map. Normalize the range of the height map to (0,1).

   对高度图应用平均模糊。这将导致更平滑的输入高度图。将高度图的范围归一化到(0,1)。

3. Randomly generate the detailed mountain texture height according to Fourier-based power law noise with frequency bounds. Normalize the range of the noise map to (0,1).

   根据傅立叶基础的幂律噪声和频率边界随机生成详细的山脉纹理高度。将噪声地图的范围归一化到(0,1)。

4. Use fade interpolation to obtain the detail richness curve. This function maps the percentage of height to the detail richness to be added to this altitude.

   使用渐进插值来获得详细丰富度曲线。此函数将高度的百分比映射到要添加到此高度的详细丰富度。

5. Combine the input height and the noise height according to the equation:
   $terrain height = weight_{original} \times input + weight_{noise} \times detail\ richness \times noise$

   根据以下方程将输入高度和噪声高度组合起来：
   $地形高度 = 初始地形权重 \times 初始地形高度 + 细节地形权重 \times 该高程细节丰富度 \times 噪声细节$

7. Apply rain erosion to the height map. The key algorithm comes from Daniel Andrino. Please refer to the [original repository](https://github.com/dandrino/terrain-erosion-3-ways?tab=MIT-1-ov-file) for more details.

   对高度图应用雨水侵蚀。关键算法来自Daniel Andrino。请参阅原始文档以获取更多详细信息。

8. Resize the map to $4096 \times 4096$. Apply another Gaussian blur to the height map to refine the map for resizing.

   将地图大小重新调整为 $4096 \times 4096$。对高度图应用另一个高斯模糊，以便为调整大小的地图进行精磨。

## MIT License 版权声明
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
