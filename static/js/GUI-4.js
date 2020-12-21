var symbolSizes=[ 0, 16, 8, 4, 4, 4]


function SeriesPoint(data){
    console.log(data)
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
            return symbolSizes[data["position"][2]]

        },
        itemStyle: {
            color: color[data["position"][2] - 1]
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

function SeriesLine(data){
    let objects=[
        {
            name: data[1]+'-'+data[4],
            type: 'lines',
            zlevel: 2,
            effect: {
                show: true,
                period: 6,
                trailLength: 0.7,
                color: '#fff',
                symbolSize: 3
            },
            lineStyle: {
                normal: {
                    color: color[0],
                    width: 0,
                    curveness: 0.2
                }
            },
            data: [{
                fromName: data[1],
                toName: data[4],
                coords: [data[10], data[11]],
                data:data
            }]
        },
        {
            name: data[1]+'-'+data[4],
            type: 'lines',
            zlevel: 2,
            symbol: ['none', 'arrow'],
            symbolSize: 3,
            effect: {
                show: true,
                period: 6,
                trailLength: 0,
                // symbol: planePath,
                symbolSize: 0
            },
            lineStyle: {
                color: color[0],
                width: 1,
                opacity: 0.6,
                curveness: 0.2
            },
            data: [{
                fromName: data[1],
                toName: data[4],
                coords: [data[10], data[11]],
                data:data
            }]
        },
    ]
    return objects;
}

function getLevel(l){
    if(l === "Tier 1")
        return 1;
    else if(l === "Tier 2")
        return 2;

    else if(l === "经销商")
        return 3;

    else if(l === "药店")
        return 4;

    else if(l === "医院")
        return 5;

}

function convertLinesData(data, showPoint=false){
    let lineList=[]
    let pointSet={}
    data.forEach(function (params){
        lineList = lineList.concat(SeriesLine(params));
        pointSet[params[1]]=params[10].concat([getLevel(params[8])]);
        pointSet[params[4]]=params[11].concat([getLevel(params[9])]);
    })
    let pointList=[]
    for(let key in pointSet){
        pointList.push({
            "name":key,
            "position":pointSet[key]
        })
    }
    // console.log(pointSet);
    if(showPoint)
        lineList = lineList.concat(convertPointsData(pointList));
    return lineList;
}


var color = ['#a6c84c', '#ffa022', '#46bee9', '#cc6666', "#999999"];

class TimeBar{
    constructor( startTime, endTime, updateFunc) {
        // console.log({a:dom});
        this.currentTime = startTime;
        this.startTime = startTime;
        this.endTime = endTime;
        this.backwardButton = document.getElementById("back")
        this.forwardButton = document.getElementById("forward")
        this.intervalButton = document.getElementById('interval')
        this.autoBUtton = document.getElementById('autoUpdate')
        this.scroll = document.getElementById("scroll")
        this.mask = document.getElementById("mask")
        this.bar = document.getElementById("bar")
        this.text = document.getElementById("timeText")
        this.updateFunc = updateFunc;
        this.autoID = null;
        this.autoType=1;
        this.autoTexts=["paused", "auto"]

        this.intervalMode= 0;
        let intervalType=["day","month"];
        this.intervalVal=[86400000, 2592000000]
        let bar = this;

        this.backwardButton.onclick= function (){
            if( bar.currentTime != null) {
                let lastTime = bar.currentTime;
                bar.currentTime = new Date(Math.max(bar.startTime.getTime(), bar.currentTime.getTime() - bar.intervalVal[bar.intervalMode]))
                bar.updateBar()
                updateFunc(bar.currentTime, null);
            }
        }

        this.forwardButton.onclick= function (){
            if( bar.currentTime != null) {
                let lastTime = bar.currentTime;
                bar.currentTime = new Date(Math.min(bar.endTime.getTime(), bar.currentTime.getTime() + bar.intervalVal[bar.intervalMode]))
                bar.updateBar()
                updateFunc(bar.currentTime, lastTime);
            }
        }

        this.intervalButton.onclick = function (){
            if( bar.currentTime != null) {
                bar.intervalMode = (bar.intervalMode + 1) % intervalType.length;
                bar.intervalButton.innerHTML = intervalType[bar.intervalMode];
            }

        }

        this.autoBUtton.onclick = function (){
            if( bar.currentTime != null) {
                bar.autoType = 1 - bar.autoType;
                bar.autoBUtton.innerText = bar.autoTexts[bar.autoType]
                bar.backwardButton.disabled = (bar.autoType === 0);
                bar.forwardButton.disabled = (bar.autoType === 0);
                ;
            }
        }
        this.updateBar();

        this.autoflowing(1000);
    }

    updateBar(){
        this.mask.style.width = ((this.currentTime-this.startTime)/(this.endTime-this.startTime)*this.scroll.offsetWidth).toString() + "px";
        this.bar.style.left = ((this.currentTime-this.startTime)/(this.endTime-this.startTime)*this.scroll.offsetWidth).toString() + "px";
        this.text.innerText = this.currentTime.toLocaleDateString();
    }

    setBar(timeStampe){
        let lastTime = this.currentTime
        this.currentTime = timeStampe
        this.updateFunc(this.currentTime, lastTime);
        this.updateBar();
    }

    autoflowing(intervalTime=500){
        let bar = this;
        this.autoID = setInterval(function (){

            if(bar.autoType === 0) {
                let lastTime = bar.currentTime;
                bar.currentTime = new Date(Math.min(bar.endTime.getTime(), bar.currentTime.getTime() + bar.intervalVal[bar.intervalMode]))
                bar.updateBar()
                bar.updateFunc(bar.currentTime, lastTime);
            }
        },intervalTime);
    }

    clear(){
        if (this.autoID!=null) {
            clearInterval(this.autoID);
            this.currentTime = this.startTime;
            this.updateBar();
            this.startTime=null;
            this.endTime=null
            this.currentTime=null;
            document.getElementById("timeText").innerText="";
            this.backwardButton.disabled = false;
            this.forwardButton.disabled = false;
        }

    }
}


function initGeoMapShow(seriesList){
    let dom = document.getElementById("container");
    let tiermap = {
        1: 'Tier 1',
        2: 'Tier 2',
        3: 'Tier 3',
        4: '药店',
        5: '医院'
    };
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
            show:true,
            trigger: 'item',
            formatter: function (val){
                console.log(val);
                if (val.componentSubType === "effectScatter"){
                    return "经销商:" + val.data.name +"<br> 经销商类型： " + tiermap[val.data.value[2]];
                }
                else if(val.componentSubType === "lines"){
                    return "从： "+val.data.fromName + "<br> 到 "+ val.data.toName + "<br> 销售金额: " + val.data.data[7];
                }
                else
                    return "";
            }
        },
        geo: {
            map: 'china',
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
            }
        },
        series: seriesList
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
        myChart.on("click", function (params){
            console.log("here")
        })
    }
}

function updateGeoMapShow(seriesList, isMerged=false){
    let dom = document.getElementById("container");
    let myChart = echarts.init(dom);
    let option = myChart.getOption()
    option.series = seriesList;
    if (option && typeof option === "object") {
        myChart.setOption(option, isMerged);
    }
}

var count = 1;

var timeBar = null


function init(){
    initGeoMapShow([]);
    // getData()
    //


    // var request = new XMLHttpRequest();
    // request.open('GET', "http://localhost:8000/flow");
    // request.setRequestHeader("Content-type","application/json");
    // send_data = {
    //     batch_number:"BJ45743",
    //     starter:"BY100002"
    // };
    // request.send(JSON.stringify(send_data));
    // request.onload = function(e){
    //     console.log("请求成功")
    //     console.log(request.status, "请求的URL的相应状态")
    //     console.log(request.readyState, "请求的结果，一般都是4")
    //     if (request.status === 200) {
    //         alert('设置回调事件成功！');
    //         window.history.back(-1); //返回上个页面
    //     }
    //     else{
    //         alert('设置失败，请重试！');
    //         window.history.back(-1);
    //     }
    // }
    // request.onerror = function(e){
    //     alert('请求失败')
    // }
}


function getData(){
    let batch_number = document.getElementById("batch").value;
    let starter = document.getElementById("start").value;
    console.log(batch_number)
    console.log(starter)
    $.ajax({
        type: "GET",
        url: 'http://localhost:8000/flow',
        dataType: 'json',
        crossDomain:true,
        data: {
            // batch_number:"BJ45743",
            // starter:"BY100002"
            batch_number:batch_number,
            starter:starter
        },//
        success: function (data) {
            console.log(data)
            initGeoMapShow([]);
            if (timeBar != null){
                timeBar.clear()
            }
            timeBar = new TimeBar(new Date(data.data[0][0]), new Date(data.data[data.data.length-1][0]),function (currentTime,lastTime) {
                // console.log(currentTime.getTime())
                let showLines=[];
                let needUpdate=false;
                data.data.forEach(function (ele) {
                    // console.log(ele["sale_date"])
                    if ((new Date(ele[0])).getTime() <= currentTime.getTime()) {
                        showLines.push(ele)
                        if (lastTime == null)
                            needUpdate = true;
                        else if ((new Date(ele[0])).getTime() > lastTime){
                            needUpdate=true;
                        }
                    }
                })
                console.log(convertLinesData(showLines, true))
                if(needUpdate)
                    updateGeoMapShow(convertLinesData(showLines, true),true)
            })
        }
    });
}