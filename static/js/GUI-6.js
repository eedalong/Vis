var showMode="Region"
var currentRegion="china"

function SeriesPoint(data){

    let object = {
        name: data["name"],
        type: 'effectScatter',
        coordinateSystem: 'geo',
        zlevel: 2,
        rippleEffect: {
            brushType: 'stroke'
        },
        label: {
            show: false,
            position: 'right',
            formatter: '{b}'
        },
        symbolSize: function (val) {
            console.log(val);
            return 10;

        },
        itemStyle: {
            color: "#ffffff"
        },
        data: [{
            name: data["name"],
            value: data["position"]
        }]
    };
    return object;
}

function convertPointsData(data) {
    let pointList = []
    data.forEach(function (params) {
        pointList.push(SeriesPoint(params));
    })
    return pointList;
}

function initRegionMapShow(regionName, data, isProvince=false){
    let dom = document.getElementById("container");
    let myChart = echarts.init(dom);
    myChart.dispose();
    myChart = echarts.init(dom);
    let option = {
        backgroundColor: '#404a59',
        title : {
            text: regionName,
            subtext: '',
            left: 'center',
            textStyle: {
                color: '#fff',
                fontSize: 40
            }
        },
        tooltip: {
            show:false,
            trigger: 'item',
        },
        visualMap: {
            type: "continuous",
            min: 0,
            max: 25,
            text: ["High", "Low"],
            realtime: false,
            calculable: true,
            color: ["red", "yellow"],
            show: true
        },
        // geo: {
        //     map: regionName,
        //     label: {
        //         show: false
        //     },
        //     roam: true,
        //     itemStyle: {
        //         areaColor: '#323c48',
        //         borderColor: '#ffffff'
        //     },
        //
        //     emphasis: {
        //         label: {
        //             show: true
        //         },
        //         itemStyle: {
        //             areaColor: '#2a333d',
        //             borderColor: '#ffffff'
        //         }
        //     },
        //     data:data
        // },
        series: [
            {
            name: regionName,
            type: 'map',
            // zoom: 1.2, // 缩放比例，可以根据实际情况调整
            mapType: regionName, // 使用中国地图
            label: {
                show: false
            },
            roam: true,
            itemStyle: {
                areaColor: '#323c48',
                borderColor: '#ffffff'
            },
            data:data,
        },
            SeriesPoint({name:"安徽",position: [112,21,3]})
        ]
    };

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
        // console.log(option)
        if(!isProvince) {
            myChart.on("click", function (params) {
                console.log(params)
                // initRegionMapShow(params.name, regionData(params.name), true)
                currentRegion=params.name
                getRegionData(params.name)

            })
        }
    }
}


function initPointMapShow(regionName, data, isProvince=false){
    let dom = document.getElementById("container");
    let myChart = echarts.init(dom);
    myChart.dispose();
    myChart = echarts.init(dom);
    let option = {
        backgroundColor: '#404a59',
        title : {
            text: regionName,
            subtext: '',
            left: 'center',
            textStyle: {
                color: '#fff',
                fontSize: 40
            }
        },
        tooltip: {
            show:false,
            trigger: 'item',
        },
        // visualMap: {
        //     type: "continuous",
        //     min: 0,
        //     max: 5,
        //     text: ["High", "Low"],
        //     realtime: false,
        //     calculable: true,
        //     color: ["blue", "green"],
        //     show: true
        // },
        geo: {
            map: regionName,
            label: {
                show: false
            },
            roam: true,
            itemStyle: {
                areaColor: '#323c48',
                borderColor: '#ffffff'
            },

            emphasis: {
                label: {
                    show: true
                },
                itemStyle: {
                    areaColor: '#2a333d',
                    borderColor: '#ffffff'
                }
            },
            data:data
        },
        series:convertPointsData([{name:"安徽",position: [112,21,3]}])
    };

    if (option && typeof option === "object") {
        myChart.setOption(option, true);
        // console.log(option)
        if(!isProvince) {
            myChart.on("click", function (params) {
                console.log(params)
                initPointMapShow(params.name, regionData(params.name), true)
                currentRegion=params.name
            })
        }
    }
}


function regionData(){
    let data=[]
    for(let key in regionDistribution)
    {
        data.push({
            name:key,
            value:regionDistribution[key]
        })
    }
    console.log(data)
    return data;

}



function init(){
    getRegionData("china")
    // showLinePrediction([])
}

function back(){
    getRegionData("china")
}


function changeMode(){
    if(showMode === "Region"){
        console.log(currentRegion)
        initPointMapShow(currentRegion, regionData(currentRegion));
        showMode="Point"
    }
    else{
        console.log(currentRegion)
        initRegionMapShow(currentRegion, regionData(currentRegion));
        showMode="Region";
    }
}


function getRegionData(regionName){
    $.ajax({
        type: "GET",
        url: 'http://localhost:8000/risk',
        dataType: 'json',
        crossDomain:true,
        data: {
            query_area:""
        },//
        success: function (data) {
            console.log(data)
            let riskData=[]
            if(currentRegion == "china")
            {
                for(let i in data.data){
                    for(let j in data.data[i]){
                        let risk=0;
                        for(let k in data.data[i][j])
                            risk += data.data[i][j][k];
                        riskData.push({"name":j.slice(0,-1), "value":risk});
                    }

                }
            }
            else{
                for(let i in data.data) {
                    for (let j in data.data[i]) {
                        if (currentRegion === j.slice(0, -1)) {
                            for (let k in data.data[i][j])
                                riskData.push({"name": k, "value": data.data[i][j][k]});
                        }
                    }

                }
            }
            console.log(riskData);

            initRegionMapShow(currentRegion, riskData, currentRegion != "china");
            currentRegion="china"
        }
    });
}