from enum import Enum


class SidebarParameters(Enum):
    # back_and_expand_func
    EXPANDED = 1            # 展开
    COLLAPSED = 0           # 关闭
    WIDTH_EXPANDED = 180    # frame/widget最大宽度
    WIDTH_COLLAPSED = 0     # frame/widget最小宽度
    ANIM_DURATION = 150  # 动画持续时间（毫秒）
    ANIM_STEP = 10  # 动画步长
