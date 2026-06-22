// =========================
// 菜单切换
// =========================

function showPage(pageName, el){

    document
        .querySelectorAll(".page")
        .forEach(p=>{

            p.classList.add("hidden");

        });

    const page =
        document.getElementById(
            "page-" + pageName
        );

    if(page){

        page.classList.remove(
            "hidden"
        );

    }

    document
        .querySelectorAll(".menu")
        .forEach(m=>{

            m.classList.remove(
                "active"
            );

        });

    if(el){

        el.classList.add(
            "active"
        );

    }

    if(pageName==="workbench"){

        setTimeout(()=>{

            initDashboardCharts();

        },100);

    }

}

// =========================
// Dashboard图表
// =========================

function initDashboardCharts(){

    const pieDom =
        document.getElementById(
            "pieChart"
        );

    const lineDom =
        document.getElementById(
            "lineChart"
        );

    if(!pieDom || !lineDom){

        return;

    }

    if(
        pieDom.dataset.rendered
    ){

        return;

    }

    pieDom.dataset.rendered="1";

    const pieData =
        JSON.parse(
            pieDom.dataset.chart
        );

    const lineData =
        JSON.parse(
            lineDom.dataset.chart
        );

    // 饼图

    const pieChart =
        echarts.init(
            pieDom
        );

    pieChart.setOption({

        tooltip:{},

        legend:{
            bottom:0
        },

        series:[
            {
                type:"pie",

                radius:["45%","70%"],

                data:Object.keys(
                    pieData
                ).map(k=>({

                    name:k,

                    value:pieData[k]

                }))
            }
        ]

    });

    // 趋势图

    const lineChart =
        echarts.init(
            lineDom
        );

    lineChart.setOption({

        tooltip:{},

        xAxis:{
            type:"category",

            data:
                lineData.map(
                    i=>i.date
                )
        },

        yAxis:{
            type:"value"
        },

        series:[
            {
                type:"line",

                smooth:true,

                areaStyle:{},

                data:
                    lineData.map(
                        i=>i.count
                    )
            }
        ]
    });

}

// =========================
// 修改密码
// =========================

async function changePassword(){

    const user =
        document.getElementById(
            "dashboard-user"
        ).value;

    const oldPwd =
        document.getElementById(
            "oldPwd"
        ).value;

    const newPwd =
        document.getElementById(
            "newPwd"
        ).value;

    const res =
        await fetch(

            "/api/user/change_password",

            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({

                    user:user,

                    old_pwd:oldPwd,

                    new_pwd:newPwd

                })

            }

        );

    const data =
        await res.json();

    document.getElementById(
        "pwdResult"
    ).innerHTML = data.msg;

}


window.afterDashboardRender = function () {

    console.log("Dashboard Render Finish");

    let count = 0;

    const timer = setInterval(() => {

        const pieDom =
            document.getElementById("pieChart");

        const lineDom =
            document.getElementById("lineChart");

        if (pieDom && lineDom) {

            clearInterval(timer);

            initDashboardCharts();

        }

        count++;

        if(count > 30){

            clearInterval(timer);

        }

    },200);

}

function openDaily(){

    showGradioPage("daily");

}

function openMeeting(){

    showGradioPage("meeting");

}

function openProjectReport(){

    showGradioPage("projectReport");

}

function showGradioPage(page){

    document
        .querySelectorAll(".gradio-page")
        .forEach(i=>{

            i.style.display="none";

        });

    const target =
        document.getElementById(page);

    if(target){

        target.style.display="block";

    }

}

async function reloadTrend(days){

    const user =
        document.getElementById(
            "dashboard-user"
        ).value;

    const rows =
        await fetch(
            `/api/dashboard/trend?user=${user}&days=${days}`
        )
        .then(r=>r.json());

    const chart =
        echarts.getInstanceByDom(
            document.getElementById(
                "lineChart"
            )
        );

    chart.setOption({

        xAxis:{
            data:rows.map(
                i=>i.date
            )
        },

        series:[{

            data:rows.map(
                i=>i.count
            )

        }]
    });
}