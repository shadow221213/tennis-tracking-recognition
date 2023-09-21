<!--
 * @Description: 基于Socket的网球跟踪识别
 * @Author: shadow221213
 * @Date: 2023-06-14 14:38:36
 * @LastEditTime: 2023-09-21 16:31:48
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
        <th>plan2</th>
        <td colspan="2">0.99s</td>
        <th>96.21%</th>
    </tr>
    <tr align="center">
        <th rowspan="2">640</th>
        <td colspan="2">0.0951s</td>
        <td rowspan="2">95.80%</td>
    </tr>
    <tr align="center">
        <td>0.0127s</td>
        <td>0.0824s</td>
    </tr>
    <tr align="center">
        <th rowspan="2">480</th>
        <td colspan="2">0.07794s</td>
        <td rowspan="2">95.40%</td>
    </tr>
    <tr align="center">
        <td>0.0083s</td>
        <td>0.06964s</td>
    </tr>
    <tr align="center">
        <th rowspan="2">320</th>
        <th colspan="2">0.07025s</th>
        <td rowspan="2">94.80%</td>
    </tr>
    <tr align="center">
        <th>0.00548s</th>
        <th>0.06477s</th>
    </tr>
</table>

320*320的图像可能因为太过于模糊，只有当用手拿着的时候才可以成功识别，并发现结果主要受算力限制，最终调整图像大小也只能优化到14帧，有点遗憾。