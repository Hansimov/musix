# MIDI 驱动工业机械音乐动画项目启动文档

**版本**：v1.0  
**日期**：2026-06-20  
**用途**：作为后续项目启动、架构设计、概念设计、资产建设、动画流程和技术栈选型的参考文档。  

---

## 0. 文档范围

本文档整理的是一个“以 MIDI 事件驱动工业机械装置、形成音乐化计算机动画作品”的项目方案。重点保留以下内容：

- 概念设计方法。
- Foreground / Midground / Background 场景构建方法。
- 工业机械装置的设计规则。
- MIDI 到动作、装置、镜头、灯光、特效的工作流程。
- Blender、Houdini、OpenUSD、CadQuery、物理验证工具等软件技术栈。
- Codex / 代码代理在工程自动化中的职责。
- 项目目录、数据格式、质量检查、MVP 里程碑。

本文档刻意排除以下内容：

- 特定音乐案例。
- 特定硬件环境。
- 操作系统取舍与远程工作站讨论。
- 图像、视频、三维生成模型相关流程。

---

# 1. 项目定义

## 1.1 项目目标

项目目标是创作一种类似“音乐机器剧场”的计算机动画作品：

> 使用 MIDI 中的时间、音符、力度、轨道、乐器等事件，驱动一套由机械、电气、电子、液压、气动、轨道、齿轮、线圈、管道、灯光和特效构成的工业化视觉场景，使画面中的机械装置像真实机器一样“演奏音乐”。

最终作品应满足四个标准：

1. **音乐同步可信**：关键动作必须与 MIDI 事件准确对应。
2. **机械因果可信**：装置运动要符合能量传递、力学结构和工程直觉。
3. **画面层次清晰**：Foreground / Midground / Background 分工明确。
4. **视觉完成度高**：场景精美、材质统一、灯光有主次、镜头有焦点、特效有节制。

## 1.2 核心原则

项目的核心原则可以压缩为一句话：

```text
MIDI 决定时间。
Planner 决定动作。
Physics 决定可行性。
DCC 决定画面。
代码代理提升工程效率。
```

这里的关键判断是：不要让自由物理仿真“碰巧”产生音乐节奏，而应由 MIDI 事件驱动确定性动作，再用物理逻辑检查动作是否合理。视觉上也不要随机堆砌机械零件，而应建立一套可复用的装置设计语言、资产体系和镜头流程。

---

# 2. 总体架构

## 2.1 逻辑架构

推荐总体架构如下：

```text
MIDI / MusicXML / DAW Export
        ↓
MIDI Event Parser
        ↓
Canonical Score Events
        ↓
Visual Instrument Mapping
        ↓
Device / Mechanism DSL
        ↓
Trajectory Planner + Resource Scheduler
        ↓
Physics Validation / Constraint Check
        ↓
Animation Cache
        ↓
Blender / Houdini / OpenUSD Scene Assembly
        ↓
Lighting / Materials / FX / Camera
        ↓
Preview Render / Final Render
        ↓
Audio-Video Mux / Review / Iteration
```

其中：

- **MIDI Event Parser**：把 MIDI 转为统一的音符事件、控制事件、速度图和结构段落。
- **Visual Instrument Mapping**：决定每个音乐轨道或音符范围对应哪种视觉装置。
- **Device / Mechanism DSL**：描述装置结构、运动自由度、物理限制和视觉反馈。
- **Trajectory Planner**：反推出物体、机械臂、锤子、滑轨、灯光等在每个时间点的状态。
- **Physics Validation**：检查速度、加速度、碰撞、关节范围、复位时间等约束。
- **Animation Cache**：把动作输出成可重复加载的数据，而不是只保存在 DCC 文件里。
- **DCC Scene Assembly**：在 Blender、Houdini 或 USD 管线中装配场景、材质、灯光、镜头和特效。

## 2.2 为什么主运动不应依赖自由物理仿真

自由物理仿真很适合生成二级运动，例如弹簧余震、碎屑、蒸汽、布线摆动、冲击后的微振动。但它不适合作为 MIDI 主事件的唯一来源。

原因如下：

- 自由仿真难以保证音符击打时间精确落在指定帧。
- 碰撞、摩擦、弹性会带来误差积累。
- 场景复杂后，仿真容易不稳定或不可复现。
- 音乐作品需要强可控性，不能把关键节奏交给随机误差。

因此建议：

```text
主运动：MIDI → 解析规划 → 关键帧 / 缓存
二级运动：碰撞、回弹、抖动、烟雾、火花、粒子 → 仿真 / 程序化
```

---

# 3. 概念设计体系

## 3.1 Art Bible：先建立风格宪法

在开始建模之前，必须先建立一份 Art Bible。它不是美术散文，而是一套可执行的规则。

示例：

```yaml
style:
  genre: industrial_music_machine
  visual_keywords:
    - industrial
    - mechanical
    - electrical
    - cinematic
    - functional
  shape_language:
    primary: rectangular_steel_frames
    secondary: circular_gears_coils_turbines
    tertiary: cables_pipes_panels_gauges
    avoid:
      - random_ornaments
      - organic_fantasy_shapes
      - unmotivated_gears
  material_family:
    structure: dark_gunmetal
    moving_parts: brushed_steel
    warning_parts: yellow_black_paint
    energy_parts: cold_blue_emission
    heat_parts: warm_orange_sparks
  lighting:
    key: directional_industrial_light
    rim: strong_backlight
    accents: warning_lamps_and_device_lights
    atmosphere: light_fog
  composition:
    foreground: hero_device_high_detail
    midground: support_system_medium_detail
    background: large_silhouette_low_detail
```

Art Bible 的作用是避免每个镜头、每个装置、每个资产都长成不同风格。

## 3.2 高级工业场景的五个判断标准

### 1. Silhouette 清楚

远看就要知道这是：

- 电磁发射轨道。
- 液压鼓锤。
- 齿轮序列器。
- 管风琴阵列。
- 线圈能量塔。
- 传送带分拣系统。
- 机械臂拨弦装置。

如果远看只是一团灰色零件，说明设计失败。

### 2. 功能句子明确

每个主装置都要能用一句话描述它的功能。

例如：

```text
这是一台使用电磁轨道发射小球、击打金属音片、再通过回收槽复位的高速旋律装置。
```

如果一句话说不清，就容易变成“齿轮 + 管子 + 灯光”的随机复杂。

### 3. 密度有层级

不要全画面高密度。应遵循：

```text
主装置：高密度细节
中景支撑：中密度结构
远景背景：大轮廓，低细节
留白区域：用雾、光、阴影承担空间
```

### 4. 材质统一

高级工业画面不靠“每个零件不同材质”，而靠少量材质族的变化：

- 深色喷漆金属。
- 拉丝钢。
- 磨损边缘。
- 黄黑警示漆。
- 红色阀门。
- 蓝色电光。
- 橙色火花。
- 油污、尘土、划痕、铭牌、编号。

### 5. 动作有因果

高级动画不是东西都在动，而是观众能理解：

```text
电信号传来 → 电容充能 → 电磁阀打开 → 活塞推动 → 锤子击打 → 装置回弹 → 指示灯复位
```

---

# 4. 机械装置设计方法

## 4.1 装置的“机械句子”

每个会演奏的机械装置都应遵循以下结构：

```text
信号输入
  ↓
能量积累
  ↓
定位 / 瞄准
  ↓
释放动作
  ↓
击打 / 拨动 / 发光 / 喷发 / 响应
  ↓
余波
  ↓
复位
```

这是让机器“像真的在工作”的核心。

## 4.2 装置类型库

| 装置类型 | 适合映射的音乐元素 | 视觉特征 |
|---|---|---|
| 小球弹道装置 | 马林巴、木琴、钢片琴、快速琶音 | 发射、飞行、击打、回收 |
| 液压锤 / 气动锤 | Kick、低频重音、鼓组 | 大活塞、压力表、蒸汽、地面震动 |
| 齿轮序列器 | 重复节奏、ostinato、机械 loop | 齿轮、凸轮、拨片、棘轮 |
| 电磁线圈阵列 | 高音旋律、电子音、滑音 | 线圈、电弧、能量流、示波器 |
| 机器人拨弦装置 | 弦乐、竖琴、bass line | 机械臂、滑轨、拨片、张力线 |
| 工业管风琴 | 和弦、pad、长音 | 风箱、阀门、巨型管阵、压力变化 |
| 传送带分拣机 | 鼓组切分、快速节奏 | 翻板、分流、分拣、机械门 |
| 继电器/PCB 阵列 | 高频电子音、hi-hat、装饰音 | LED、继电器、触点、微型机械反馈 |

## 4.3 Hero Device 设计卡模板

每个主装置都应有结构化设计卡：

```yaml
device_name: electromagnetic_marimba_rail
musical_role: fast_melodic_arpeggio
visual_silhouette: long_horizontal_rail_with_vertical_coil_towers
mechanical_story:
  - signal_light_travels_along_rail
  - capacitor_bank_charges
  - solenoid_launcher_fires_ball
  - ball_hits_tuned_metal_bar
  - metal_bar_vibrates
  - catcher_returns_ball_to_conveyor
main_parts:
  - solenoid_coils
  - ball_magazine
  - tuned_bars
  - return_conveyor
  - capacitor_banks
materials:
  - dark_gunmetal
  - brushed_steel
  - ceramic_ball_white
  - amber_warning_labels
animation_phases:
  anticipation_frames: 6
  launch_frames: 2
  impact_time: exact_midi_event
  recoil_frames: 12
  reset_frames: 20
secondary_motion:
  - bar_vibration
  - coil_glow_decay
  - small_sparks
  - catcher_bounce
camera_ideas:
  - side_tracking_shot_following_ball
  - macro_shot_of_solenoid_firing
  - top_down_view_showing_pitch_layout
```

这类设计卡的作用是把“好不好看”转化为可执行的结构、动作和镜头需求。

---

# 5. Foreground / Midground / Background 场景设计

## 5.1 基本分工

| 层级 | 作用 | 细节密度 | 动态强度 |
|---|---|---:|---:|
| Foreground | 主表演、主机械、主音乐事件 | 高 | 高 |
| Midground | 支撑系统、空间结构、次级机械 | 中 | 中 |
| Background | 规模感、环境氛围、大剪影 | 低到中 | 低 |

## 5.2 Foreground 规则

Foreground 是观众当前应该看的地方。

规则：

- 一个镜头只允许一个主装置成为绝对焦点。
- 主装置应占据画面显著面积。
- 主动作路径必须清楚，例如小球飞行、锤子击打、机械臂拨弦。
- 前景可有少量遮挡物，但不能遮挡关键运动。
- 主装置材质、灯光、轮廓必须比环境更突出。

典型 Foreground 元素：

- 电磁小球装置。
- 液压鼓锤。
- 机械拨弦臂。
- 齿轮拨片序列器。
- 线圈电弧阵列。

## 5.3 Midground 规则

Midground 的作用是证明主装置不是孤立道具，而属于一个大型工业系统。

适合放置：

- 平台、栏杆、支撑梁。
- 管线、电缆桥架、控制柜。
- 传送带、吊车、次级机械臂。
- 压力表、阀门、灯阵、风扇。

动态规则：

- 中景不要逐音符同步，而应按 beat、bar、section 或系统状态变化。
- 中景动作应慢于前景，避免抢戏。
- 中景可以承担“机械因果链”的传播，例如信号沿管线传递、压力触发泄压阀。

## 5.4 Background 规则

Background 的作用是制造世界规模和空间纵深。

适合放置：

- 巨型反应堆。
- 远处冷却塔。
- 管道群。
- 高层维修平台。
- 远景工厂剪影。
- 巨型电缆束。

动态规则：

- 背景不应频繁大幅运动。
- 用雾、灯光、烟雾、远处小灯、缓慢旋转结构制造生命感。
- 背景主要按 phrase 或 section 变化，而不是每个音符变化。

## 5.5 场景设计公式

一个镜头可用以下公式检查：

```text
1 个主装置
2–3 个中景支撑系统
1 个背景大剪影
若干灯光 / 烟雾 / 粒子 / 仪表反馈
明确的主光方向
明确的镜头焦点
```

如果一个镜头里有三个以上同等重要的机械装置，通常会变乱。

---

# 6. 动态设计体系

## 6.1 多时间尺度运动

工业场景的生命感来自多层运动，而不是所有东西都高速运动。

| 时间尺度 | 适合元素 |
|---|---|
| 0.1–0.5 秒 | 火花、电弧、灯光闪烁、阀门瞬时喷气 |
| 1–5 秒 | 风扇、皮带、仪表指针、警示灯、机械回弹 |
| 5–20 秒 | 吊车移动、机械臂复位、烟雾扩散、传送带循环 |
| 20–120 秒 | 背景巨构、远景灯阵、环境雾、全场照明状态 |

## 6.2 运动类型库

建议建立 `motion_library`，把常见运动封装成可复用模板。

### Continuous Rotation

适合：风扇、涡轮、齿轮、卷盘。

```yaml
motion_class: continuous_rotation
axis: Z
rpm: 24
startup_time: 3.0
wobble: 0.02
```

物理逻辑：

```text
电机启动 → 加速 → 稳态旋转 → 轻微轴承偏心
```

### Valve Burst

适合：蒸汽阀、泄压口、气动装置。

```yaml
motion_class: valve_burst
trigger: drum_accent
open_time: 0.08
hold_time: 0.25
close_time: 0.12
steam_intensity: velocity
```

物理逻辑：

```text
压力积累 → 阀门打开 → 蒸汽喷出 → 压力下降 → 阀门关闭
```

### Signal Flow

适合：管线灯、电缆、PCB 走线、能量环。

```yaml
motion_class: signal_flow
path: pipe_curve_01
speed: 8.0
pulse_width: 0.15
color: cyan
trigger: phrase_start
```

物理逻辑：

```text
控制信号沿线路传播 → 相关装置进入准备状态
```

### Rail Crane

适合：中景吊车、轨道车、桥式机械结构。

```yaml
motion_class: rail_crane
path: crane_track_curve
speed: 0.6
stop_points: [0.2, 0.55, 0.8]
hook_sway: true
max_sway_angle_deg: 4
```

物理逻辑：

```text
电机牵引 → 轨道平移 → 停止时吊钩因惯性摆动 → 阻尼衰减
```

### Energy Pulse

适合：反应堆核心、线圈、电容组、能量塔。

```yaml
motion_class: energy_pulse
base_emission: 1.5
pulse_source: bass_or_section
pulse_decay: 0.4
```

物理逻辑：

```text
能量输入 → 亮度增强 → 体积光增强 → 衰减回稳态
```

### Mechanical Idle

适合：大型设备、控制柜、管线、机械底座。

```yaml
motion_class: mechanical_idle
vibration_amp: 0.005
vibration_freq: 12
noise_phase: random
```

物理逻辑：

```text
内部电机 / 泵 / 流体造成轻微振动
```

## 6.3 同步层级

不要让所有元素都逐音符同步。建议：

| 场景层级 | 同步粒度 |
|---|---|
| 主装置 | Note-level |
| 次级机械 | Beat / Bar |
| 中景系统 | Phrase / Section |
| 背景氛围 | Section / Long-cycle |
| 灯光 | Beat + Velocity |
| 烟雾 / 蒸汽 | Accent trigger + physical decay |

这样画面会更像真实工业系统，而不是简单音乐可视化。

---

# 7. 从设计图到动态场景

这里的“设计图”指已经确定的远景、中景或装置概念图。落地时不应把整张图直接动态化，而应拆解成空间层、语义层和运动层。

## 7.1 三种落地路线

### 路线 A：2.5D 动态 Matte

适合远景。

流程：

```text
设计图
  ↓
分层：天空 / 远景建筑 / 烟囱 / 灯阵 / 雾 / 前景遮挡
  ↓
以 image planes 放入 3D 空间
  ↓
加入 parallax、灯光闪烁、烟雾、远景小运动
```

优点：快，成本低。  
缺点：不能大角度绕拍。

### 路线 B：投影贴图 + 简单几何

适合中远景。

流程：

```text
设计图
  ↓
搭建盒子、柱体、管道、平台等 proxy 几何
  ↓
投影或贴图到几何上
  ↓
把风扇、灯、烟、吊车、管线信号单独拆出来动画
```

优点：有更好的遮挡和视差。  
缺点：需要手动修投影、遮挡、材质。

### 路线 C：模块化 3D 重建

适合重要中景和会被观众注意的机械结构。

流程：

```text
设计图
  ↓
手工拆解部件
  ↓
灰模 blockout
  ↓
资产库替换
  ↓
添加运动控制器
  ↓
统一材质、灯光和特效
```

优点：可绕拍、可动画、可复用。  
缺点：成本最高。

## 7.2 Motion Tagging

每个设计图拆解后，建议维护一份 `motion_tags.yaml`：

```yaml
objects:
  - name: bg_smokestack_01
    layer: background
    role: atmosphere
    motion_class: slow_smoke
    physics: hot_air_rise
    attention_level: low

  - name: mg_cooling_fan_03
    layer: midground
    role: cooling_system
    motion_class: continuous_rotation
    axis: Z
    rpm: 18
    physics: electric_motor

  - name: mg_pipe_light_01
    layer: midground
    role: signal_path
    motion_class: signal_flow
    path: pipe_01_curve
    speed: 6.0
    physics: electrical_signal

  - name: mg_valve_02
    layer: midground
    role: pressure_release
    motion_class: valve_burst
    trigger: drum_accent
    physics: pressure_release
```

这份文件可以由代码代理转成 Blender 驱动、Geometry Nodes 参数、材质动画、关键帧或仿真触发器。

## 7.3 判断哪些元素能动

简单规则：

```text
有能量输入的东西可以动。
有机械自由度的东西可以动。
有流体、热、光、信号的东西可以动。
承重结构不乱动。
大建筑不乱动。
没有功能解释的装饰不乱动。
```

错误示例：

- 所有管子同时抖动。
- 所有灯随机闪。
- 所有齿轮无因果地旋转。
- 烟从不该冒烟的位置冒出。

正确示例：

- 风扇按电机逻辑启动。
- 泄压阀在压力峰值后喷气。
- 信号灯沿管线传播。
- 吊车沿轨道移动并在停止后轻微摆动。
- 反应堆核心按乐段缓慢脉冲。

---

# 8. MIDI 到视觉事件的数据设计

## 8.1 Canonical Score Event

原始 MIDI 数据不应直接驱动场景。先转换为统一事件格式：

```json
{
  "tempo_map": [
    {"time": 0.0, "bpm": 128}
  ],
  "events": [
    {
      "id": "e000001",
      "track": 0,
      "channel": 1,
      "instrument": "melodic_percussion",
      "note": 60,
      "velocity": 92,
      "start": 1.250,
      "end": 1.500,
      "duration": 0.250,
      "musical_role": "melody"
    }
  ],
  "sections": [
    {"name": "intro", "start": 0.0, "end": 12.0},
    {"name": "main", "start": 12.0, "end": 48.0}
  ]
}
```

## 8.2 Visual Instrument Mapping

把音乐轨道映射到视觉装置：

```yaml
instrument_maps:
  melody:
    midi_channel: 1
    visual_device: electromagnetic_marimba_rail
    note_range: [48, 84]
    strike_mode: ballistic_ball
    timing_priority: exact

  percussion_low:
    midi_channel: 10
    visual_device: hydraulic_hammer
    strike_mode: cam_arm
    timing_priority: exact

  harmony_pad:
    midi_channel: 3
    visual_device: industrial_pipe_organ
    strike_mode: valve_airflow
    timing_priority: phrase

  electronic_texture:
    midi_channel: 4
    visual_device: coil_light_array
    strike_mode: energy_pulse
    timing_priority: beat
```

## 8.3 Device Constraint Schema

每个装置都应定义物理和动画约束：

```yaml
device: hydraulic_hammer
limits:
  min_reset_time: 0.18
  max_linear_speed: 4.0
  max_acceleration: 35.0
  max_stroke: 0.45
  min_stroke: 0.02
  collision_proxy: hydraulic_hammer_proxy.obj
controls:
  hammer_height: [0.0, 0.45]
  valve_open: [0.0, 1.0]
  warning_light: [0.0, 1.0]
secondary:
  recoil_decay: 0.35
  steam_delay: 0.08
```

## 8.4 Animation Cache

不要把动作只存进 DCC 文件。应输出可复现缓存：

```json
{
  "fps": 60,
  "objects": {
    "hammer_A": {
      "channels": {
        "location.z": [
          [0, 0.45],
          [12, 0.05],
          [20, 0.42]
        ],
        "custom.valve_open": [
          [0, 0.0],
          [10, 1.0],
          [18, 0.0]
        ]
      }
    }
  }
}
```

优点：

- 可回放。
- 可检查。
- 可重建。
- 可批量替换资产。
- 可从同一事件表输出到不同 DCC 工具。

---

# 9. 软件技术栈

## 9.1 Python 核心层

用途：

- MIDI 解析。
- 事件格式化。
- 装置映射。
- 轨迹规划。
- 物理约束检查。
- 资产索引。
- 预览任务调度。
- 渲染命令生成。
- 测试和质量检查。

建议库：

- `mido`：MIDI message 与文件解析。
- `pretty_midi`：更高层的 note/instrument/time 表达。
- `numpy` / `scipy`：轨迹计算、插值、优化。
- `pydantic`：配置 schema 校验。
- `pyyaml` / `jsonschema`：配置文件。
- `pytest`：单元测试。
- `rich` / `typer`：命令行工具。

## 9.2 Blender

Blender 适合作为主场景装配、动画缓存导入、材质、灯光、镜头和渲染工具。

主要用途：

- Python API 自动建场景。
- Asset Browser 管理资产库。
- Geometry Nodes 生成管线、栏杆、灯阵、实例化细节。
- Drivers 绑定 MIDI / 控制曲线 / 自定义属性。
- Keyframes 承载主运动。
- Rigid Body Constraints 做局部机械约束原型。
- Fluid / Particles / Volumes 做烟、蒸汽、火花、尘埃。
- Cycles / Eevee 做预览与渲染。
- 命令行渲染支持批处理。

适合承担：

```text
scene assembly
look development
camera blocking
lighting
material unification
animation cache playback
preview render
final render
```

## 9.3 Houdini

Houdini 适合程序化工业资产和复杂特效。

主要用途：

- 管线、平台、楼梯、栏杆、线缆桥架生成。
- 机械 greeble 细节生成。
- 烟、蒸汽、粒子、碎屑、电弧等特效。
- Houdini Digital Assets 封装可复用工具。
- PDG / TOPs 批量生成变体、缓存和预览。
- Solaris / USD 做大场景装配和渲染管线。

适合承担：

```text
procedural assets
industrial set dressing
FX simulation
batch variants
USD scene publishing
```

## 9.4 CadQuery / FreeCAD 类参数化 CAD 工具

适合生成工程味更强的基础机械部件：

- 齿轮。
- 法兰。
- 支架。
- 轴承座。
- 管道接头。
- 机械外壳。
- 控制盒。
- 标准化结构件。

这类部件不一定直接用于最终高精渲染，但非常适合作为：

```text
accurate base geometry
collision proxy
manufacturing-style asset foundation
procedural variants
```

## 9.5 OpenUSD

OpenUSD 适合作为大场景资产组织和交换格式。

主要用途：

- 大型场景分层。
- 引用资产。
- 实例化重复结构。
- 多镜头共享场景。
- 分离 layout、animation、lookdev、lighting。
- 与 Blender、Houdini、Unreal 等工具交换数据。

推荐层级：

```text
assets.usd      # 资产定义
layout.usd      # 场景摆放
animation.usd   # 时间采样动作
lookdev.usd     # 材质
lighting.usd    # 灯光
shot.usd        # 镜头组合
```

## 9.6 物理验证工具

物理工具应定位为“验证”和“辅助生成”，而不是直接支配全部主动画。

可选工具：

- MuJoCo：多关节、接触、机器人和动画相关验证。
- Drake：动力学、控制、优化、机器人机制验证。
- Project Chrono：多体系统、机电系统、车辆、柔性体/接触等工程仿真。
- PyBullet：快速原型、轻量刚体测试。

适合验证：

- 机械臂关节范围。
- 速度和加速度限制。
- 轨迹可达性。
- 简化碰撞。
- 小球弹道可行性。
- 复位时间。
- 重力和惯性是否合理。

## 9.7 Unreal Engine（可选）

Unreal 更适合实时预览、大场景交互、虚拟制片式镜头和程序化世界搭建。

可选用途：

- 实时镜头预览。
- 大场景交互式漫游。
- Sequencer 电影化镜头。
- PCG 工具生成大规模环境。

但对于本项目的核心机械同步动画，不建议把 Unreal 作为唯一主控系统。更稳妥的方式是通过 USD / Alembic / glTF 接收已经规划好的动画和资产。

## 9.8 FFmpeg

用途：

- 图像序列转视频。
- 合成音频与视频。
- 生成预览 mp4。
- 生成不同码率版本。
- 自动化审片输出。

---

# 10. 资产库设计

## 10.1 资产类别

建议建立以下资产树：

```text
assets/
  structural/
    beams/
    trusses/
    ladders/
    walkways/
    railings/
  mechanical/
    gears/
    belts/
    chains/
    bearings/
    pistons/
    cams/
    crank_slider/
    robotic_arms/
  electrical/
    cables/
    cable_trays/
    control_cabinets/
    pcb_panels/
    leds/
    oscilloscopes/
    transformers/
    coils/
  piping/
    pipes/
    valves/
    flanges/
    elbows/
    pressure_gauges/
  music_devices/
    tuned_bars/
    drums/
    resonators/
    strings/
    pipe_organs/
  fx/
    steam_emitters/
    spark_emitters/
    smoke_volumes/
    light_pulses/
  decals/
    warning_labels/
    serial_numbers/
    arrows/
    panel_text/
```

## 10.2 资产元数据

每个资产都应有元数据：

```yaml
asset_id: valve_large_037
category: piping/valve
unit: meter
scale_class: medium
visual_weight: high
usable_layers:
  - midground
  - background
render_mesh: valve_large_037_render.glb
collision_proxy: valve_large_037_proxy.obj
material_family: dark_steel
pivot_policy: center_of_rotation
sockets:
  pipe_in: [-1.0, 0.0, 0.0]
  pipe_out: [1.0, 0.0, 0.0]
animation_capable: true
controls:
  open_ratio: [0.0, 1.0]
  wheel_rotation: [0.0, 360.0]
```

没有元数据的资产只是一堆模型；有元数据的资产才是可自动化调度的系统部件。

## 10.3 Render Mesh 与 Collision Proxy 分离

每个机械资产应尽量分成：

```text
高质量渲染模型：用于画面。
低复杂度碰撞模型：用于碰撞和验证。
控制骨架 / pivot：用于动画。
连接 socket：用于装配。
材质槽：用于统一 lookdev。
```

这样可以避免复杂模型拖慢动画验证，也能让资产更容易复用。

---

# 11. Blender 场景组织建议

推荐集合结构：

```text
SCENE_ROOT
  CAMERAS
  LIGHTING
  FOREGROUND_HERO_DEVICES
  MIDGROUND_SYSTEMS
  BACKGROUND_STRUCTURES
  FX_STEAM
  FX_SPARKS
  FX_DUST
  FX_LIGHT_PULSES
  MOTION_CONTROLLERS
  MOTION_PATHS
  RENDER_HELPERS
```

每个动态对象建议添加 custom properties：

```text
motion_class
system_id
phase
intensity
midi_channel
physical_role
attention_level
sync_level
```

然后由 Python 扫描场景并绑定动作：

```python
for obj in scene.objects:
    motion_class = obj.get("motion_class")
    if motion_class == "continuous_rotation":
        bind_continuous_rotation(obj)
    elif motion_class == "valve_burst":
        bind_valve_burst(obj)
    elif motion_class == "signal_flow":
        bind_signal_flow(obj)
```

这样场景不再依赖纯手工关键帧，而是由统一规则驱动。

---

# 12. 材质、灯光与镜头

## 12.1 材质原则

工业场景高级感主要来自材质统一和局部差异。

建议材质族：

```text
base_dark_gunmetal
brushed_steel
black_rubber
aged_yellow_paint
red_valve_paint
blue_emissive_electric
orange_heat_sparks
dirty_concrete
oily_floor
scratched_glass
```

每个材质应提供：

- Base Color。
- Roughness。
- Metallic。
- Normal / Bump。
- Edge wear。
- Dirt mask。
- Decal overlay。

## 12.2 灯光原则

不要把场景均匀照亮。应建立层级：

```text
主装置：最亮、最高对比度。
中景：比主装置暗一级。
背景：主要靠轮廓和体积光。
能量部件：局部自发光。
警示灯：节奏反馈。
```

推荐灯光状态：

| 音乐结构 | 灯光状态 |
|---|---|
| Intro | 低照度，仪表和小灯可见 |
| Build-up | 机械逐步点亮 |
| Main section | 主装置高亮，背景有脉冲 |
| Bridge | 局部冷光，减少运动 |
| Finale | 全场联动，强背光和更多体积感 |

## 12.3 镜头原则

镜头服务于音乐和机械因果链。

镜头类型：

| 类型 | 用途 |
|---|---|
| 解释性镜头 | 看清装置怎么工作 |
| 跟随镜头 | 跟随小球、机械臂、传送带 |
| 宏观镜头 | 展示整个工业音乐机器 |
| 近景镜头 | 展示击打、阀门、电弧、仪表 |
| 转场镜头 | 从一个装置连接到另一个装置 |

镜头不应随意漂浮。每个镜头都应回答：

```text
观众应该看哪里？
这个镜头展示了哪个机械因果？
它对应音乐中的哪个结构？
运动方向是否清楚？
背景是否抢戏？
```

---

# 13. Codex / 代码代理工作方式

## 13.1 代码代理适合做什么

适合：

- 写 MIDI 解析工具。
- 写配置 schema。
- 写 Blender Python 脚本。
- 写 Houdini 批处理脚本。
- 写资产导入、命名、打标脚本。
- 写 motion library。
- 写预览渲染命令。
- 写质量检查脚本。
- 写测试。
- 生成装置设计卡模板。
- 根据 motion tags 批量绑定动画。

不适合：

- 直接替代 art direction。
- 在无规则情况下随机搭场景。
- 只凭一句话生成最终可用镜头。
- 绕过测试直接改生产文件。

## 13.2 AGENTS.md 模板

```markdown
# Project Rules

## Units
- Units are SI: meters, kilograms, seconds.
- Frame rate is 60 fps unless explicitly overridden.

## Core Principle
- MIDI event time is the source of truth.
- Never hand-key note timing in DCC tools.
- Every visual hit must be derived from canonical score events.

## Asset Rules
- Every asset must define unit, scale class, render mesh, collision proxy, sockets, material family, and animation capability.
- Hero devices must have a design card before implementation.
- Render mesh and collision proxy should be separated.

## Animation Rules
- Foreground devices can use note-level sync.
- Midground systems use beat/bar/section-level sync.
- Background atmosphere uses phrase/section-level sync.
- Main mechanical impacts must pass timing and physical feasibility checks.

## Scene Rules
- Each shot must define foreground, midground, and background roles.
- Each shot must have a primary focal device.
- Do not add random moving parts without physical role.

## Quality Checks
Before marking a task done, run:
- unit tests
- schema validation
- animation cache validation
- preview render
- shot review checklist
```

## 13.3 自动化命令示例

```bash
make parse-midi INPUT=music/source.mid
make plan-motion SHOT=shot_003
make validate-motion SHOT=shot_003
make build-scene SHOT=shot_003
make preview-fast SHOT=shot_003
make preview-sync SHOT=shot_003
make render-final SHOT=shot_003
```

---

# 14. 项目目录建议

```text
project_root/
  README.md
  AGENTS.md
  pyproject.toml

  music/
    midi/
    audio/
    events/

  configs/
    style_bible.yaml
    device_maps.yaml
    scene_defaults.yaml

  src/
    midi_parser/
    score_events/
    mechanism_dsl/
    planners/
    validators/
    exporters/
    asset_registry/
    render_queue/

  assets/
    structural/
    mechanical/
    electrical/
    piping/
    music_devices/
    fx/
    decals/

  scenes/
    master_layout/
    shots/

  shots/
    shot_001/
      shot.yaml
      motion_tags.yaml
      camera.yaml
      lighting.yaml
      preview/
      renders/

  dcc/
    blender/
      scripts/
      templates/
    houdini/
      hdas/
      scripts/
    usd/
      layers/

  cache/
    animation/
    simulation/
    geometry/

  renders/
    previews/
    finals/

  tests/
    test_midi_parser.py
    test_planners.py
    test_schema.py
    test_motion_validation.py
```

---

# 15. 质量检查表

## 15.1 概念设计检查

| 检查项 | 通过标准 |
|---|---|
| 主装置功能是否一句话说清 | 是 |
| Silhouette 是否远看可读 | 是 |
| 是否有机械因果链 | 是 |
| 是否避免随机齿轮和随机管线 | 是 |
| 材质族是否统一 | 是 |
| 是否有明确 Foreground / Midground / Background | 是 |

## 15.2 动画检查

| 检查项 | 通过标准 |
|---|---|
| 主击打时间误差 | 小于指定帧误差 |
| 同一执行器复位时间 | 不冲突 |
| 速度和加速度 | 不超出 device limits |
| 关节范围 | 不超限 |
| 运动方向 | 观众可读 |
| 二级运动 | 有但不抢戏 |
| 中景/背景 | 不逐音符乱动 |

## 15.3 画面检查

| 检查项 | 评分 |
|---|---:|
| 主体一眼可读 | 1–10 |
| 空间层次清楚 | 1–10 |
| 机械功能可信 | 1–10 |
| 材质统一 | 1–10 |
| 灯光主次明确 | 1–10 |
| 背景不抢戏 | 1–10 |
| 动态有生命感 | 1–10 |
| 音乐和机械关系明确 | 1–10 |

低于 7 的镜头不进入精修。

---

# 16. MVP 里程碑

## 16.1 MVP 目标

先做一个 20–30 秒 vertical slice，而不是完整长片。

MVP 包含：

- 一个中央工业音乐舞台。
- 3–4 个 Hero Device。
- 清晰的前中后景结构。
- 8–12 个镜头。
- 完整 MIDI 事件到动作缓存链路。
- 统一材质和灯光。
- 基础烟雾、火花、灯光、仪表反馈。
- 带音频的预览视频。

## 16.2 阶段规划

### 阶段 1：风格与系统设计

产出：

- Art Bible。
- 装置类型表。
- Foreground / Midground / Background 规则。
- 资产分类表。
- 项目目录和配置 schema。

### 阶段 2：核心数据链路

产出：

- MIDI parser。
- Canonical score events。
- Device mapping。
- Motion cache 格式。
- 基础验证工具。

### 阶段 3：Hero Device 灰模

产出：

- 3–4 个主装置设计卡。
- Blender 灰模。
- 主运动控制器。
- 简单预览动画。

### 阶段 4：场景搭建

产出：

- 主舞台 layout。
- 中景支撑结构。
- 背景大剪影。
- 资产库第一版。
- 材质族第一版。

### 阶段 5：镜头与灯光

产出：

- 8–12 个镜头。
- 镜头说明表。
- 灯光状态表。
- 预览剪辑。

### 阶段 6：特效与打磨

产出：

- 蒸汽、火花、体积雾。
- 仪表、警示灯、信号流。
- 二级运动。
- 同步检查。
- 最终 preview。

---

# 17. 常见风险与规避

## 17.1 风险：画面变成随机复杂

规避：

- 每个装置必须有功能句子。
- 每个运动必须有物理角色。
- 每个镜头只允许一个主焦点。
- 先灰模构图，再替换资产。

## 17.2 风险：音乐同步不准

规避：

- MIDI 时间作为唯一真源。
- 主运动由 planner 反推。
- 动画缓存统一输出。
- 自动检查帧级误差。

## 17.3 风险：资产库失控

规避：

- 所有资产必须有 metadata。
- 统一命名规则。
- render mesh 和 collision proxy 分离。
- 资产必须归类到 catalog。

## 17.4 风险：场景太重

规避：

- 重复结构使用实例化。
- 背景降低细节。
- 中景采用 proxy。
- 只精修镜头可见区域。
- 建立 preview / final 两套质量等级。

## 17.5 风险：代码代理改坏工程

规避：

- AGENTS.md 固化规则。
- schema validation。
- 单元测试。
- 预览渲染。
- Git 分支。
- 小步提交。

---

# 18. 项目启动清单

启动项目时，按以下顺序执行：

1. 建立项目目录。
2. 编写 `AGENTS.md`。
3. 编写 `style_bible.yaml`。
4. 定义 `canonical_score_event.schema.json`。
5. 定义 `device_card.schema.yaml`。
6. 定义 `asset_metadata.schema.yaml`。
7. 实现 MIDI parser。
8. 实现第一个 device planner。
9. 实现 Blender animation cache importer。
10. 建立 3 个基础材质族。
11. 建立 20 个基础工业资产。
12. 搭建第一个 Hero Device 灰模。
13. 生成第一个 10 秒 preview。
14. 用质量检查表评分。
15. 低于标准则回到灰模阶段，不急着精修。

---

# 19. 推荐参考资料

以下资料用于支撑软件技术栈和管线设计：

- Blender Python API：<https://docs.blender.org/api/current/>
- Blender Command Line Rendering：<https://docs.blender.org/manual/en/latest/advanced/command_line/render.html>
- Blender Drivers：<https://docs.blender.org/manual/en/latest/animation/drivers/index.html>
- Blender Geometry Nodes Simulation Zone：<https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html>
- Blender Rigid Body Constraints：<https://docs.blender.org/manual/en/latest/physics/rigid_body/constraints/index.html>
- Blender Asset Browser：<https://docs.blender.org/manual/en/latest/editors/asset_browser.html>
- Houdini Digital Assets：<https://www.sidefx.com/docs/houdini/assets/intro.html>
- Houdini HOM Python API：<https://www.sidefx.com/docs/houdini/hom/index.html>
- OpenUSD Introduction：<https://openusd.org/release/intro.html>
- OpenUSD Scenegraph Instancing：<https://openusd.org/dev/api/_usd__page__scenegraph_instancing.html>
- CadQuery Documentation：<https://cadquery.readthedocs.io/>
- Mido Documentation：<https://mido.readthedocs.io/>
- MuJoCo：<https://mujoco.org/>
- Drake：<https://drake.mit.edu/>
- Project Chrono：<https://projectchrono.org/>
- Unreal Engine PCG：<https://dev.epicgames.com/documentation/unreal-engine/procedural-content-generation-overview>
- Unreal Engine Sequencer Python：<https://dev.epicgames.com/documentation/unreal-engine/python-scripting-in-sequencer-in-unreal-engine>
- FFmpeg Documentation：<https://ffmpeg.org/ffmpeg.html>

---

# 20. 最终原则摘要

```text
不要先追求复杂模型；先追求清晰设计。
不要先堆资产；先做灰模构图。
不要让自由物理决定节奏；让 MIDI 决定时间。
不要让所有元素都动；让有物理角色的元素动。
不要让中景背景抢戏；它们服务主装置。
不要只做单个镜头；建立资产、动作、材质、灯光系统。
不要把 DCC 文件当唯一真源；所有关键动作和配置都应可复现。
```

这类作品的核心不是“做一个漂亮场景”，而是建立一个能持续生产漂亮场景、可信机械、音乐同步动画的工程化系统。
