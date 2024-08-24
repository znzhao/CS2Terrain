import streamlit as st

def preset_plain(CHN, colx, coly, min_altitude, max_altitude, key = 'post'):
    ocean_lower_x = colx.number_input('Ocean Lower Anchor (m)' if not CHN else "海洋下界锚点 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_plain_x0')
    ocean_lower_y = coly.number_input('Ocean Lower Altitude (m)' if not CHN else "海洋下界输出 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_plain_y0')
    ocean_upper_x = colx.number_input('Ocean Upper Anchor (m)' if not CHN else "海洋上界锚点 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_x1')
    ocean_upper_y = coly.number_input('Ocean Upper Altitude (m)' if not CHN else "海洋上界输出 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_y1')
    plain_lower_x = colx.number_input('Plain Lower Anchor (m)' if not CHN else "平原下界锚点 (米)", 
                                        value=325.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_x2')
    plain_lower_y = coly.number_input('Plain Lower Altitude (m)' if not CHN else "平原下界输出 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_y2')
    plain_x       = colx.number_input('Plain Anchor (m)' if not CHN else "平原锚点 (米)", 
                                        value=525.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_x3')
    plain_y       = coly.number_input('Plain Altitude (m)' if not CHN else "平原输出 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_y3')
    plain_upper_x = colx.number_input('Plain Upper Anchor (m)' if not CHN else "平原上界锚点 (米)", 
                                        value=800.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_x4')
    plain_upper_y = coly.number_input('Plain Upper Altitude (m)' if not CHN else "平原上界输出 (米)", 
                                        value=600.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_y4')
    mount_lower_x = colx.number_input('Mount Lower Anchor (m)' if not CHN else "山脉下界锚点 (米)", 
                                        value=1200.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_x5')
    mount_lower_y = coly.number_input('Mount Lower Altitude (m)' if not CHN else "山脉下界输出 (米)", 
                                        value=1000.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plain_y5')
    mount_upper_x = colx.number_input('Mount Upper Anchor (m)' if not CHN else "山脉上界锚点 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_plain_x6')
    mount_upper_y = coly.number_input('Mount Upper Altitude (m)' if not CHN else "山脉上界输出 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_plain_y6')

    intpl_x = [ocean_lower_x, ocean_upper_x, plain_lower_x, plain_x, plain_upper_x, mount_lower_x, mount_upper_x]
    intpl_y = [ocean_lower_y, ocean_upper_y, plain_lower_y, plain_y, plain_upper_y, mount_lower_y, mount_upper_y]
    return intpl_x, intpl_y

def preset_canyon(CHN, colx, coly, min_altitude, max_altitude, key = 'post'):
    plain_lower_x_1 = colx.number_input('Plain Lower Anchor 1 (m)' if not CHN else "平原下界锚点1 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_canyon_x0')
    plain_lower_y_1 = coly.number_input('Plain Lower Altitude 1 (m)' if not CHN else "平原下界输出1 (米)", 
                                        value=700.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y0')
    plain_upper_x_1 = colx.number_input('Plain Upper Anchor 1 (m)' if not CHN else "平原上界锚点1 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x1')
    plain_upper_y_1 = coly.number_input('Plain Upper Altitude 1 (m)' if not CHN else "平原上界输出1 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y1')
    riverbend_lower_x_1 = colx.number_input('Riverbend Lower Anchor 1 (m)' if not CHN else "河畔下界锚点1 (米)", 
                                        value=350.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x2')
    riverbend_lower_y_1 = coly.number_input('Riverbend Lower Altitude 1 (m)' if not CHN else "河畔下界输出1 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y2')
    riverbend_upper_x_1 = colx.number_input('Riverbend Upper Anchor 1 (m)' if not CHN else "河畔上界锚点1 (米)", 
                                        value=450.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x3')
    riverbend_upper_y_1 = coly.number_input('Riverbend Upper Altitude 1 (m)' if not CHN else "河畔上界输出1 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y3')
    riverbend_lower_x_2 = colx.number_input('Riverbend Lower Anchor 2 (m)' if not CHN else "河畔下界锚点2 (米)", 
                                        value=550.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x5')
    riverbend_lower_y_2 = coly.number_input('Riverbend Lower Altitude 2 (m)' if not CHN else "河畔下界输出2 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y5')
    riverbend_upper_x_2 = colx.number_input('Riverbend Upper Anchor 2 (m)' if not CHN else "河畔上界锚点2 (米)", 
                                        value=650.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x6')
    riverbend_upper_y_2 = coly.number_input('Riverbend Upper Altitude 2 (m)' if not CHN else "河畔上界输出2 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y6')
    plain_lower_x_2 = colx.number_input('Plain Lower Anchor 2 (m)' if not CHN else "平原下界锚点2 (米)", 
                                        value=700.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x7')
    plain_lower_y_2 = coly.number_input('Plain Lower Altitude 2 (m)' if not CHN else "平原下界输出2 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y7')
    plain_upper_x_2 = colx.number_input('Plain Upper Anchor 2 (m)' if not CHN else "平原上界锚点2 (米)", 
                                        value=800.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x8')
    plain_upper_y_2 = coly.number_input('Plain Upper Altitude 2 (m)' if not CHN else "平原上界输出2 (米)", 
                                        value=700.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y8')

    mount_lower_x = colx.number_input('Mount Lower Anchor (m)' if not CHN else "山脉下界锚点 (米)", 
                                        value=1300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_x9')
    mount_lower_y = coly.number_input('Mount Lower Altitude (m)' if not CHN else "山脉下界输出 (米)", 
                                        value=1000.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_canyon_y9')
    mount_upper_x = colx.number_input('Mount Upper Anchor (m)' if not CHN else "山脉上界锚点 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_canyon_x10')
    mount_upper_y = coly.number_input('Mount Upper Altitude (m)' if not CHN else "山脉上界输出 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_canyon_y10')

    intpl_x = [plain_lower_x_1, plain_upper_x_1, riverbend_lower_x_1, riverbend_upper_x_1, riverbend_lower_x_2, riverbend_upper_x_2, plain_lower_x_2, plain_upper_x_2, mount_lower_x, mount_upper_x]
    intpl_y = [plain_lower_y_1, plain_upper_y_1, riverbend_lower_y_1, riverbend_upper_y_1, riverbend_lower_y_2, riverbend_upper_y_2, plain_lower_y_2, plain_upper_y_2, mount_lower_y, mount_upper_y]
    return intpl_x, intpl_y

def preset_plateau(CHN, colx, coly, min_altitude, max_altitude, key = 'post'):
    ocean_lower_x = colx.number_input('Ocean Lower Anchor (m)' if not CHN else "海洋下界锚点 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_plateau_x0')
    ocean_lower_y = coly.number_input('Ocean Lower Altitude (m)' if not CHN else "海洋下界输出 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_plateau_y0')
    ocean_upper_x = colx.number_input('Ocean Upper Anchor (m)' if not CHN else "海洋上界锚点 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x1')
    ocean_upper_y = coly.number_input('Ocean Upper Altitude (m)' if not CHN else "海洋上界输出 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y1')
    plain_lower_x = colx.number_input('Plain Lower Anchor (m)' if not CHN else "平原下界锚点 (米)", 
                                        value=325.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x2')
    plain_lower_y = coly.number_input('Plain Lower Altitude (m)' if not CHN else "平原下界输出 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y2')
    plain_x       = colx.number_input('Plain Anchor (m)' if not CHN else "平原锚点 (米)", 
                                        value=525.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x3')
    plain_y       = coly.number_input('Plain Altitude (m)' if not CHN else "平原输出 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y3')
    plain_upper_x = colx.number_input('Plain Upper Anchor (m)' if not CHN else "平原上界锚点 (米)", 
                                        value=800.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x4')
    plain_upper_y = coly.number_input('Plain Upper Altitude (m)' if not CHN else "平原上界输出 (米)", 
                                        value=600.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y4')
    plateau_lower_x = colx.number_input('Plateau Lower Anchor (m)' if not CHN else "高原下界锚点 (米)", 
                                        value=825.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x5')
    plateau_lower_y = coly.number_input('Plateau Lower Altitude (m)' if not CHN else "高原下界输出 (米)", 
                                        value=800.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y5')
    plateau_upper_x = colx.number_input('Plateau Upper Anchor (m)' if not CHN else "高原上界锚点 (米)", 
                                        value=1000.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x6')
    plateau_upper_y = coly.number_input('Plateau Upper Altitude (m)' if not CHN else "高原上界输出 (米)", 
                                        value=800.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y6')
    mount_lower_x = colx.number_input('Mount Lower Anchor (m)' if not CHN else "山脉下届锚点 (米)", 
                                        value=1200.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x7')
    mount_lower_y = coly.number_input('Mount Lower Altitude (m)' if not CHN else "山脉下届输出 (米)", 
                                        value=1000.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y7')
    mount_upper_x = colx.number_input('Mount Upper Anchor (m)' if not CHN else "山脉上界锚点 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_plateau_x8')
    mount_upper_y = coly.number_input('Mount Upper Altitude (m)' if not CHN else "山脉上界输出 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_plateau_y8')

    intpl_x = [ocean_lower_x, ocean_upper_x, plain_lower_x, plain_x, plain_upper_x, plateau_lower_x, plateau_upper_x, mount_lower_x, mount_upper_x]
    intpl_y = [ocean_lower_y, ocean_upper_y, plain_lower_y, plain_y, plain_upper_y, plateau_lower_y, plateau_upper_y, mount_lower_y, mount_upper_y]
    return intpl_x, intpl_y

def preset_riverbend(CHN, colx, coly, min_altitude, max_altitude, key = 'post'):
    ocean_lower_x = colx.number_input('Ocean Lower Anchor (m)' if not CHN else "海洋下界锚点 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_plateau_x0')
    ocean_lower_y = coly.number_input('Ocean Lower Altitude (m)' if not CHN else "海洋下界输出 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_plateau_y0')
    ocean_upper_x = colx.number_input('Ocean Upper Anchor (m)' if not CHN else "海洋上界锚点 (米)", 
                                        value=200.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x1')
    ocean_upper_y = coly.number_input('Ocean Upper Altitude (m)' if not CHN else "海洋上界输出 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y1')
    riverbend_lower_x = colx.number_input('Riverbend Lower Anchor (m)' if not CHN else "河畔下界锚点 (米)", 
                                        value=300/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x5')
    riverbend_lower_y = coly.number_input('Riverbend Lower Altitude (m)' if not CHN else "河畔下界输出 (米)", 
                                        value=400/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y5')
    riverbend_upper_x = colx.number_input('Riverbend Upper Anchor (m)' if not CHN else "河畔上界锚点 (米)", 
                                        value=400/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x6')
    riverbend_upper_y = coly.number_input('Riverbend Upper Altitude (m)' if not CHN else "河畔上界输出 (米)", 
                                        value=400.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y6')
    plain_lower_x = colx.number_input('Plain Lower Anchor (m)' if not CHN else "平原下界锚点 (米)", 
                                        value=425.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x2')
    plain_lower_y = coly.number_input('Plain Lower Altitude (m)' if not CHN else "平原下界输出 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y2')
    plain_x       = colx.number_input('Plain Anchor (m)' if not CHN else "平原锚点 (米)", 
                                        value=600.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x3')
    plain_y       = coly.number_input('Plain Altitude (m)' if not CHN else "平原输出 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y3')
    plain_upper_x = colx.number_input('Plain Upper Anchor (m)' if not CHN else "平原上界锚点 (米)", 
                                        value=900.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x4')
    plain_upper_y = coly.number_input('Plain Upper Altitude (m)' if not CHN else "平原上界输出 (米)", 
                                        value=600.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y4')
    mount_lower_x = colx.number_input('Mount Lower Anchor (m)' if not CHN else "山脉下届锚点 (米)", 
                                        value=1200.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_x7')
    mount_lower_y = coly.number_input('Mount Lower Altitude (m)' if not CHN else "山脉下届输出 (米)", 
                                        value=1000.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_plateau_y7')
    mount_upper_x = colx.number_input('Mount Upper Anchor (m)' if not CHN else "山脉上界锚点 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_plateau_x8')
    mount_upper_y = coly.number_input('Mount Upper Altitude (m)' if not CHN else "山脉上界输出 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_plateau_y8')

    intpl_x = [ocean_lower_x, ocean_upper_x, riverbend_lower_x, riverbend_upper_x, plain_lower_x, plain_x, plain_upper_x, mount_lower_x, mount_upper_x]
    intpl_y = [ocean_lower_y, ocean_upper_y, riverbend_lower_y, riverbend_upper_y, plain_lower_y, plain_y, plain_upper_y, mount_lower_y, mount_upper_y]
    return intpl_x, intpl_y

def preset_reverse(CHN, colx, coly, min_altitude, max_altitude, key = 'post'):
    platform_upper_x = colx.number_input('Platform Upper Anchor (m)' if not CHN else "高台上界锚点 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_reverse_x0')
    platform_upper_y = coly.number_input('Platform Upper Altitude (m)' if not CHN else "高台上界输出 (米)", 
                                        value=600.0/1800*(max_altitude-min_altitude)+min_altitude, 
                                        min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_reverse_y0')
    platform_lower_x = colx.number_input('Platform Lower Anchor (m)' if not CHN else "高台下界锚点 (米)", 
                                        value=300.0/1800*(max_altitude-min_altitude)+min_altitude, 
                                        min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_reverse_x1')
    platform_lower_y = coly.number_input('Platform Lower Altitude (m)' if not CHN else "高台下界输出 (米)", 
                                        value=600.0/1800*(max_altitude-min_altitude)+min_altitude, 
                                        min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_reverse_y1')
    riverbend_upper_x = colx.number_input('Riverbend Lower Anchor (m)' if not CHN else "河畔下界锚点 (米)", 
                                        value=325.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_reverse_x2')
    riverbend_upper_y = coly.number_input('Riverbend Lower Altitude (m)' if not CHN else "河畔下界输出 (米)", 
                                        value=400.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_reverse_y2')
    riverbend_lower_x = colx.number_input('Riverbend Upper Anchor (m)' if not CHN else "河畔上界锚点 (米)", 
                                        value=500.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_reverse_x3')
    riverbend_lower_y = coly.number_input('Riverbend Upper Altitude (m)' if not CHN else "河畔上界输出 (米)", 
                                        value=400.0/1800*(max_altitude-min_altitude)+min_altitude, min_value=min_altitude, 
                                        max_value=max_altitude, step = 1.0, key = key + '_reverse_y3')
    ocean_x = colx.number_input('Ocean Anchor (m)' if not CHN else "海洋锚点 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_reverse_x4')
    ocean_y = coly.number_input('Ocean Altitude (m)' if not CHN else "海洋输出 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_reverse_y4')
    intpl_x = [platform_upper_x, platform_lower_x, riverbend_upper_x, riverbend_lower_x, ocean_x]
    intpl_y = [platform_upper_y, platform_lower_y, riverbend_upper_y, riverbend_lower_y, ocean_y]
    return intpl_x, intpl_y

def preset_linear(CHN, colx, coly, min_altitude, max_altitude, key = 'post'):
    ocean_x = colx.number_input('Ocean Anchor (m)' if not CHN else "海洋锚点 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_linear_x0')
    ocean_y = coly.number_input('Ocean Altitude (m)' if not CHN else "海洋输出 (米)", 
                                        value=min_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_linear_y0')
    mount_x = colx.number_input('Mount Anchor (m)' if not CHN else "山脉锚点 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, disabled=True, key = key + '_linear_x1')
    mount_y = coly.number_input('Mount Altitude (m)' if not CHN else "山脉输出 (米)", 
                                        value=max_altitude, min_value=min_altitude, max_value=max_altitude, step = 1.0, key = key + '_linear_y1')
    intpl_x = [ocean_x, mount_x,]
    intpl_y = [ocean_y, mount_y,]
    return intpl_x, intpl_y