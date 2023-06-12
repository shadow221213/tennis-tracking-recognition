<!--
 * @Description: 基于OpenCV的网球跟踪识别
 * @Author: shadow221213
 * @Date: 2023-06-11 22:03:52
 * @LastEditTime: 2023-06-12 21:43:21
-->
# 基于OpenCV的网球跟踪识别
==================================================

这是一个会受环境影响的版本，后续会上传其他版本

==================================================

## 底层逻辑
利用 **hsv** 的h层区分颜色排除一定程度的干扰，通过边缘检测+霍夫圆检测查找可能存在的圆形（因为球体从哪个方向看都是圆）。
再加上以下代码来排除一定量的干扰：

``` python
for circle in circles[0]:
    xx, yy, rr = map(int, circle)
    is_valid = Open[yy][xx] == 255

    if not is_valid:
        cnt = sum([
                    Open[min(yy + rr // 2,camra_height - 1)][xx] != 255,
                    Open[max(yy - rr // 2, 0)][xx] != 255,
                    Open[yy][min(xx + rr // 2, camra_width - 1)] != 255,
                    Open[yy][max(xx - rr // 2, 0)] != 255])
        is_valid = cnt >= 3
        
    if is_valid:
        cir.append((xx, yy, rr))
```