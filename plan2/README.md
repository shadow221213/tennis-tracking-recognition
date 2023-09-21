<!--
 * @Description: 基于YOLO的网球跟踪识别
 * @Author: shadow221213
 * @Date: 2023-06-12 13:45:13
 * @LastEditTime: 2023-09-21 16:30:04
-->

# 基于YOLO的网球跟踪识别

==================================================

这是一个较准确的版本，后续会上传其他版本

==================================================

## 底层逻辑

因为需要在树莓派上流畅运行，测试过三种yolov5的预训练模型。（以下模型结果均是在 img_cnt = 357，epoch = 200，等待100s，相同训练集和验证集下进行）

<table>
    <tr>
        <th>预训练集</th>
        <th>识别时长</th>
        <th>准确度</th>
    </tr>
    <tr align="center">
        <td>yolov5x.pt</td>
        <td>12.46s</td>
        <td>94.97%</td>
    </tr>
    <tr align="center">
        <td>yolov5l.pt</td>
        <td>7.24s</td>
        <td>95.68%</td>
    </tr>
    <tr align="center">
        <td>yolov5m.pt</td>
        <td>4.09s</td>
        <th>97.90%</th>
    </tr>
    <tr align="center">
        <td>yolov5s.pt</td>
        <td>1.87s</td>
        <td>97.40%</td>
    </tr>
    <tr align="center">
        <td>yolov5n.pt</td>
        <th>0.99s</mark></th>
        <td>96.21%</td>
    </tr>
</table>

可能是因为样本质量不好或者迭代次数太少的关系，导致这个结果不太稳定，但是基于对时间的考虑，最终决定选择“**yolov5n.pt**”这个预训练模型，测试帧率在1帧左右，正所谓“一帧能玩，两帧流畅，三帧电竞”，只能说也不是不能用。
