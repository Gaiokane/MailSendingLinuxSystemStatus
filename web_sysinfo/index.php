<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>系统资源使用情况</title>
    <!-- 引入 echarts.js -->
    <script src="js\echarts.js"></script>
</head>

<body>

    <style type="text/css">
        .dcenter {
            overflow: auto;
            margin: auto;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }
    </style>
    
    <?php
        $con=mysqli_connect("host","user","pwd","db","port");
        
		if (mysqli_connect_errno($con))
		{
			echo "数据库连接失败：" . mysqli_connect_error();
        }
        
		$sql_tstamp = "SELECT DATE_FORMAT(tstamp,'%Y-%m-%d %H:%i') FROM `table` ORDER BY tstamp ASC;";
		$sql_cpuPercent = "SELECT cpuPercent FROM `table` ORDER BY tstamp ASC;";
        $sql_memoryPercent = "SELECT memoryPercent FROM `table` ORDER BY tstamp ASC;";
        
		if ($result_tstamp=mysqli_query($con,$sql_tstamp))
		{
			//返回记录数
            $rowcount_tstamp=mysqli_num_rows($result_tstamp);
            
            $tstamp = "";
            
            //循环遍历出数据表中的数据
			for($i=0;$i<$rowcount_tstamp;$i++){
				$array_tstamp = mysqli_fetch_row($result_tstamp);
                $tstamp .= "'".$array_tstamp[0]."'";
                
                //echo "rowcount_tstamp：$rowcount_tstamp</br>i：$i</br>";
                
                if ($row+1<$rowcount_tstamp) {
                    $tstamp .= " , ";
                }
            }
            
            /*while($arr=mysqli_fetch_assoc($result_tstamp)){//取出表中的所有结果集
                foreach($arr as $col){//遍历数据
                    $tstamp .= $col;
                }
            }*/
            
            /*while($row=mysqli_fetch_row($result_tstamp)){
                $tstamp .= $row[0];
            }*/
            
            //echo "tstamp合计：$rowcount_tstamp</br></br>";
            //echo "tstamp：$tstamp</br></br>";
        }
        
		if ($result_cpuPercent=mysqli_query($con,$sql_cpuPercent))
		{
			//返回记录数
            $rowcount_cpuPercent=mysqli_num_rows($result_cpuPercent);
            
            $cpuPercent = "";
            
            //循环遍历出数据表中的数据
			for($i=0;$i<$rowcount_cpuPercent;$i++){
				$array_cpuPercent = mysqli_fetch_row($result_cpuPercent);
                $cpuPercent .= "'".$array_cpuPercent[0]."'";
                
                if ($row+1<$rowcount_cpuPercent) {
                    $cpuPercent .= " , ";
                }
            }
            
            //echo "cpuPercent合计：$rowcount_cpuPercent</br></br>";
            //echo "cpuPercent：$cpuPercent</br></br>";
        }
        
		if ($result_memoryPercent=mysqli_query($con,$sql_memoryPercent))
		{
			//返回记录数
            $rowcount_memoryPercent=mysqli_num_rows($result_memoryPercent);
            
            $memoryPercent = "";
            
            //循环遍历出数据表中的数据
			for($i=0;$i<$rowcount_memoryPercent;$i++){
				$array_memoryPercent = mysqli_fetch_row($result_memoryPercent);
                $memoryPercent .= "'".$array_memoryPercent[0]."'";
                
                if ($row+1<$rowcount_memoryPercent) {
                    $memoryPercent .= " , ";
                }
            }
            
            //echo "memoryPercent合计：$rowcount_memoryPercent</br></br>";
            //echo "memoryPercent：$memoryPercent</br></br>";
        }
        
        mysqli_close($con);
        
		?>
        
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div class="dcenter" id="main" style="width: 1200px;height:800px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));
        
        var timeData = [
            //调用php中的tstamp
            <?php
                echo $tstamp;
            ?>
        ];
        
        /* 将timeData中的2009/替换为空 */
        /*timeData = timeData.map(function (str) {
            return str.replace('2009/', '');
        });*/
        
        option = {
            title: {
                text: '系统资源使用情况',
                subtext: '副标题',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    animation: false
                }
            },
            legend: {
                data: ['CPU使用率', '内存使用率'],
                left: 10
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            axisPointer: {
                link: { xAxisIndex: 'all' }
            },
            dataZoom: [
                {
                    show: true,
                    realtime: true,
                    /* 进度条开始结束范围 */
                    start: 70,
                    end: 100,
                    xAxisIndex: [0, 1]
                },
                {
                    type: 'inside',
                    realtime: true,
                    /* 进度条开始结束范围 */
                    start: 70,
                    end: 100,
                    xAxisIndex: [0, 1]
                }
            ],
            grid: [{
                left: 50,
                right: 50,
                height: '35%'
            }, {
                left: 50,
                right: 50,
                top: '55%',
                height: '35%'
            }],
            xAxis: [
                {
                    type: 'category',
                    boundaryGap: false,
                    axisLine: { onZero: true },
                    data: timeData
                },
                {
                    gridIndex: 1,
                    type: 'category',
                    boundaryGap: false,
                    axisLine: { onZero: true },
                    data: timeData,
                    position: 'top'
                }
            ],
            yAxis: [
                {
                    name: '百分比(%)',
                    type: 'value',
                    //max: 500//坐标轴最大值
                },
                {
                    gridIndex: 1,
                    name: '百分比(%)',
                    type: 'value',
                    inverse: false//Y轴反转
                }
            ],
            series: [
                {
                    name: 'CPU使用率',
                    type: 'line',
                    symbolSize: 8,
                    hoverAnimation: false,
                    data: [
                        //调用php中的cpuPercent
                        <?php
                            echo $cpuPercent;
                        ?>
                    ]
                },
                {
                    name: '内存使用率',
                    type: 'line',
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    symbolSize: 8,
                    hoverAnimation: false,
                    data: [
                        //调用php中的tstamp
                        <?php
                            echo $memoryPercent;
                        ?>
                    ]
                }
            ]
        };
        
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
</body>

</html>