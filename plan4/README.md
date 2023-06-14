<!--
 * @Description: 基于Socket的网球跟踪识别
 * @Author: shadow221213
 * @Date: 2023-06-14 14:38:36
 * @LastEditTime: 2023-06-14 15:47:24
-->

# 基于Socket的网球跟踪识别

## 底层逻辑

把**PC端**当成服务器，利用数据图传将**树莓派**获取图像传到PC端进行识别运算，并将结果回传

<table>
    <tr>
        <th rowspan="2">预训练集</th>
        <th colspan="2">总时长</th>
        <th rowspan="2">准确度</th>
    </tr>
    <tr>
        <th>传输时长</th>
        <th>识别时长</th>
    </tr>
    <tr align="center">
        <td>plan2</td>
        <td colspan="2">0.99s</td>
        <th>96.21%</th>
    </tr>
    <tr align="center">
        <td rowspan="2">plan4</td>
        <th colspan="2">0.0951s</td>
        <td rowspan="2">95.80%</td>
    </tr>
    <tr align="center">
        <td>0.0127s</td>
        <td>0.0824s</td>
    </tr>
</table>

发现结果主要受算力限制，考虑优化算法看怎么使得结果速度更优。