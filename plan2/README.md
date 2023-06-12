<!--
 * @Description: 基于YOLO的网球跟踪识别
 * @Author: shadow221213
 * @Date: 2023-06-12 13:45:13
 * @LastEditTime: 2023-06-12 21:22:07
-->

# 基于YOLO的网球跟踪识别

==================================================

这是一个较准确的版本，后续会上传其他版本

==================================================

## 底层逻辑

因为需要在树莓派上流畅运行，测试过三种yolov5的预训练模型。（以下模型结果均是在 img_cnt = 357，epoch = 200，等待100s，相同训练集和验证集下进行）

<table>
<tr><font face="楷体">
<th>预训练集</th>
<th>识别时长</th>
<th>准确度</th>
</font></tr>
<tr><font face="consolas">
<th>yolov5x.pt</th>
<th>12.46s</th>
<th>94.97%</th>
</tr>
<tr>
<th>yolov5l.pt</th>
<th>7.24s</th>
<th>95.68%</th>
</tr>
<tr>
<th>yolov5m.pt</th>
<th>4.09s</th>
<th><font color="red">97.90%</font></th>
</tr>
<tr>
<th>yolov5s.pt</th>
<th>1.87s</th>
<th>97.40%</th>
</tr>
<tr>
<th>yolov5n.pt</th>
<th><font color="red">0.99s</font></th>
<th>96.21%</th>
</font></tr>
</table>

可能是因为样本质量不好或者迭代次数太少的关系，导致这个结果不太稳定，但是基于对时间的考虑，最终决定选择“**yolov5n.pt**”这个预训练模型，测试帧率在1帧左右，正所谓“一帧能玩，两帧流畅，三帧电竞”，只能说也不是不能用。
