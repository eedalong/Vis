var regionDistribution = {
    "安徽":  8,
    "澳门":  1,
    "北京":  2,
    "重庆":  11,
    "福建":  6,
    "甘肃":  1,
    "广东":  7,
    "广西":  7,
    "贵州":  11,
    "海南":  2,
    "河北":  3,
    "黑龙江":1,
    "河南":  9,
    "湖北":  9,
    "湖南":  9,
    "江苏":  8,
    "江西":  8,
    "吉林":  1,
    "辽宁":  1,
    "内蒙古":4,
    "宁夏":  3,
    "青海":  10,
    "山东":  4,
    "上海":  5,
    "山西":  4,
    "陕西":  10,
    "四川":  10,
    "台湾":  4,
    "天津":  3,
    "香港":  4,
    "新疆":  10,
    "西藏":  4,
    "云南":  11,
    "浙江":  6
}

var regionNames=[
    "North-东北",
    "North-北京",
    "North-津冀",
    "North-鲁晋蒙",
    "South-上海",
    "South-浙闽",
    "South-粤桂琼",
    "South-苏皖赣",
    "West-西中",
    "West-西北",
    "West-西南",
]


var styleJson= [
    {
        "featureType": "water",
        "elementType": "all",
        "stylers": {
            "color": "#021019"
        }
    },
    {
        "featureType": "highway",
        "elementType": "geometry.fill",
        "stylers": {
            "color": "#000000"
        }
    },
    {
        "featureType": "highway",
        "elementType": "geometry.stroke",
        "stylers": {
            "color": "#147a92"
        }
    },
    {
        "featureType": "arterial",
        "elementType": "geometry.fill",
        "stylers": {
            "color": "#000000"
        }
    },
    {
        "featureType": "arterial",
        "elementType": "geometry.stroke",
        "stylers": {
            "color": "#0b3d51"
        }
    },
    {
        "featureType": "local",
        "elementType": "geometry",
        "stylers": {
            "color": "#000000"
        }
    },
    {
        "featureType": "land",
        "elementType": "all",
        "stylers": {
            "color": "#08304b"
        }
    },
    {
        "featureType": "railway",
        "elementType": "geometry.fill",
        "stylers": {
            "color": "#000000"
        }
    },
    {
        "featureType": "railway",
        "elementType": "geometry.stroke",
        "stylers": {
            "color": "#08304b"
        }
    },
    {
        "featureType": "subway",
        "elementType": "geometry",
        "stylers": {
            "lightness": -70
        }
    },
    {
        "featureType": "building",
        "elementType": "geometry.fill",
        "stylers": {
            "color": "#000000"
        }
    },
    {
        "featureType": "all",
        "elementType": "labels.text.fill",
        "stylers": {
            "color": "#857f7f"
        }
    },
    {
        "featureType": "all",
        "elementType": "labels.text.stroke",
        "stylers": {
            "color": "#000000"
        }
    },
    {
        "featureType": "building",
        "elementType": "geometry",
        "stylers": {
            "color": "#022338"
        }
    },
    {
        "featureType": "green",
        "elementType": "geometry",
        "stylers": {
            "color": "#062032"
        }
    },
    {
        "featureType": "boundary",
        "elementType": "all",
        "stylers": {
            "color": "#1e1c1c"
        }
    },
    {
        "featureType": "manmade",
        "elementType": "geometry",
        "stylers": {
            "color": "#022338"
        }
    },
    {
        "featureType": "poi",
        "elementType": "all",
        "stylers": {
            "visibility": "off"
        }
    },
    {
        "featureType": "all",
        "elementType": "labels.icon",
        "stylers": {
            "visibility": "off"
        }
    },
    {
        "featureType": "background",
        "elementType": "labels.text.fill",
        "stylers": {
            "color": "#2da0c6",
            "visibility": "off"
        }
    },
    {
        "featureType": "road",
        "elementType": "all",
        "stylers": {
            "visibility": "off"
        }
    },
    {
        "featureType": "poilabel",
        "elementType": "all",
        "stylers": {
            "visibility": "off"
        }
    },
    {
        "featureType": "boundary",
        "elementType": "all",
        "stylers": {
            "color": "#00ffffff",
            "hue": "#00ffff",
            "weight": "1.3",
            "lightness": 33,
            "saturation": 52,
            "visibility": "on"
        }
    }
]