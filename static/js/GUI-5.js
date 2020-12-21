var color = ['#a6c84c', '#ffa022', '#46bee9', '#fff'];

var selected_levels=["country", "region", "province"]

var selected_level="country";

function selectLevel(level){
    document.getElementById("selected_level").innerText = level;
    selected_level = level
}

function highlightRegion(inputRegionName){
    let level = selected_level;
    console.log(level)
    let regionData= [];

    if (inputRegionName === null){
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: 1
            })
        }
    }
    else if( level === selected_levels[0]){
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: 0
            })
        }
    }
    else if( level === selected_levels[1]){
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: (regionDistribution[key] === regionDistribution[inputRegionName])?0:1
            })
        }
    }
    else {
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: (key === inputRegionName)?0:1
            })
        }
    }


    return regionData;

}

function normalRegion(inputRegionName){
    let level = document.getElementById("selected_level").innerText;
    console.log(level)
    let regionData= [];

    if (inputRegionName === null){
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: 1
            })
        }
    }
    else if( level === selected_levels[0]){
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: 1
            })
        }
    }
    else if( level === selected_levels[1]){
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: 1
            })
        }
    }
    else {
        for(let key in regionDistribution){
            regionData.push({
                name:key,
                value: 1
            })
        }
    }


    return regionData;

}


function initGeoMapShow(seriesList){
    let dom = document.getElementById("container");
    let myChart = echarts.init(dom);
    let option = {
        backgroundColor: '#404a59',
        title : {
            text: '',
            subtext: '',
            left: 'center',
            textStyle: {
                color: '#fff'
            }
        },
        tooltip: {
            show:false,
            trigger: 'item',
        },
        visualMap: {
            type: "continuous",
            min: 0,
            max: 2,
            text: ["High", "Low"],
            realtime: false,
            calculable: true,
            color: ["blue", "yellow"],
            show: false
        },
        series: [{
                name: '',
                type: 'map',
                zoom: 1.2, // 缩放比例，可以根据实际情况调整
                mapType: 'china', // 使用中国地图
                label: {
                    show: false,
                    emphasis:{
                      show:true
                    },
                },
                roam: true,
                itemStyle: {
                    areaColor: '#323c48',
                    borderColor: '#ffffff',
                    emphasis:{
                        label: {
                            show:true
                        }
                    },
                },
                emphasis:{
                    label: {
                        show:true
                    }
                },

                data:highlightRegion(null)
        }]
    };

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
        myChart.on("mouseover", function (params){
            console.log(params)
            let regionData = highlightRegion(params["name"]);
            option.series[0].data=regionData;
            myChart.setOption(option, true);
            }
        )
        myChart.on("mouseout", function (params){
                console.log(params)
                let regionData = normalRegion(params["name"]);
                option.series[0].data=regionData;
                myChart.setOption(option, true);
            }
        )

        myChart.on("click", function (params) {
            console.log(params);
            let regionData = normalRegion(params["name"]);
            option.series[0].data=regionData;
            myChart.setOption(option, true);
            getPredictionData(params["name"]);
        })
        console.log(option)
    }
}


function showPredict(inputRegionName, data){
    if (inputRegionName == "")
        inputRegionName="全国";
    showLinePrediction(inputRegionName, data);
}

function showLinePrediction(name,lineData){
    let lineChart = echarts.init(document.getElementById("line_chart"));
    lineChart.clear()
    let option = {
        title: {
            text: name
        },
        xAxis: {
            type: 'category',
            data: lineData.x,//横坐标的list， 字符串list， 例如 ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: lineData.y, //纵坐标list，例如[820, 932, 901, 934, 1290, 1330, 1320],
            type: 'line'
        }]
    };
    lineChart.setOption(option,true);

}

var count = 1;

function init(){
    initGeoMapShow([]);
    // showLinePrediction([])
}

function queryRegion(regionName){
    if( selected_level === "country"){
        return "";
    }
    else if(selected_level === "region"){
        return regionNames[regionDistribution[regionName]];
    }
    else
        return regionName;
}


function getPredictionData(regionName){
    $.ajax({
        type: "GET",
        url: 'http://localhost:8000/', //url
        dataType: 'json',
        crossDomain:true,
        data: {
            query_area: queryRegion(regionName), //全国预测输入为空，大区则输入为大区名字，省份预测则为省份名字
        },//
        complete: function (data) {  //将这里的complete改为success
            console.log(data)
            let lineData = data;
            //需要将data处理为Linedata的样式
            // LineData样式：
            // {
            //     x:[], //横坐标值的list， 字符串list
            //     y:[]  //纵坐标值的list， 数值list
            // }
            lineData={
                x:['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                y:[820, 932, 901, 934, 1290, 1330, 1320]
            }

            showPredict(queryRegion(regionName), lineData)
        }
    });
}