function getCurrentUser(){

    return document.getElementById(
        "dashboard-user"
    ).value;

}

function setActiveMenu(index){
    document
    .querySelectorAll(".menu")
    .forEach((m,i)=>{
        if(i===index){
            m.classList.add("active");
        }else{
            m.classList.remove("active");
        }
    });
}

window.renderDashboard = function () {
    const pieDom = document.getElementById("pieChart");
    const lineDom = document.getElementById("lineChart");
    // ========= 饼图 =========
    if (pieDom) {

        const data = JSON.parse(pieDom.dataset.chart);

        echarts.init(pieDom).setOption({
            title: { text: "提交结构" },
            tooltip: { trigger: "item" },
            series: [{
                type: "pie",
                radius: "65%",
                data: data
            }]
        });
    }

    // ========= 折线 =========
    if (lineDom) {

        const data = JSON.parse(lineDom.dataset.chart);

        echarts.init(lineDom).setOption({
            title: { text: "7天提交趋势" },
            tooltip: {},
            xAxis: {
                type: "category",
                data: data.map(i => i.date)
            },
            yAxis: { type: "value" },
            series: [{
                type: "line",
                smooth: true,
                areaStyle: {},
                data: data.map(i => i.value)
            }]
        });
    }
};
window.startDashboard=function(){

    const timer=setInterval(()=>{

        const dom=
            document.getElementById(
                "dashboard_user"
            );

        if(dom){

            clearInterval(timer);

            window.USER_REAL_NAME=
                dom.value;

            renderDashboard();

        }

    },200);

};

window.renderDashboardCharts=function(){

    // 饼图

    const pieDom =
        document.getElementById(
            "submitPieChart"
        );

    if(pieDom){

        const pieData =
            JSON.parse(
                pieDom.dataset.chart
            );

        const pie =
            echarts.init(
                pieDom
            );

        pie.setOption({

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
    }

    // 趋势图

    const lineDom =
        document.getElementById(
            "submitLineChart"
        );

    if(lineDom){

        const lineData =
            JSON.parse(
                lineDom.dataset.chart
            );

        const line =
            echarts.init(
                lineDom
            );

        line.setOption({

            tooltip:{},

            xAxis:{
                type:"category",

                data:Object.keys(
                    lineData
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

                    data:Object.values(
                        lineData
                    )
                }
            ]
        });
    }
}

/* =====================
   工作台
===================== */

async function loadWorkbench(){

    setActiveMenu(0);

    const root =
        document.getElementById(
            "dashboard-root"
        );

    root.innerHTML =
        "<div class='loading'>加载工作台...</div>";

    const user =
        getCurrentUser();

    const kpi =
        await fetch(
            "/api/dashboard/kpi?user="+user
        ).then(r=>r.json());

    root.innerHTML = `

    <div class="welcome-card">

        <h1>
            欢迎回来，${user}
        </h1>

        <p>
            今日工作情况总览
        </p>

    </div>

    <div class="kpi-row">

        <div class="kpi-card">

            <div class="kpi-value">
                ${kpi.total}
            </div>

            <div>
                总提交
            </div>

        </div>

        <div class="kpi-card">

            <div class="kpi-value">
                ${kpi.report}
            </div>

            <div>
                日报
            </div>

        </div>

        <div class="kpi-card">

            <div class="kpi-value">
                ${kpi.meeting}
            </div>

            <div>
                会议
            </div>

        </div>

        <div class="kpi-card">

            <div class="kpi-value">
                ${kpi.project}
            </div>

            <div>
                项目
            </div>

        </div>

    </div>

    <div class="chart-row">

        <div
            id="pieChart"
            class="chart-card">
        </div>

        <div
            id="lineChart"
            class="chart-card">
        </div>

    </div>

    <div class="bottom-row">

        <div
            id="projectTop"
            class="panel-card">
        </div>

        <div
            id="recentSubmit"
            class="panel-card">
        </div>

    </div>

    <div
        id="aiPanel"
        class="ai-card">
    </div>

    `;

    renderPieChart();
    renderLineChart();
    loadTopProject();
    loadRecentSubmit();
    loadAIAnalysis();

}


function loadProject(){

    document.getElementById(
        "dashboard-root"
    ).innerHTML="<h2>我的项目</h2>";
}

/* =====================
   我的提交
===================== */

async function loadSubmit(){

    setActiveMenu(2);

    const user =
        getCurrentUser();

    const rows =
        await fetch(
            "/api/dashboard/submit?user="+user
        ).then(r=>r.json());

    let html = `

    <div class="page-title">

        我的提交

    </div>

    <div class="timeline">
    `;

    rows.forEach(r=>{

        html += `
        <div class="timeline-item">

            <div>

                ${r.type}

            </div>

            <div>

                ${r.time}

            </div>

            <div>

                ${r.content}

            </div>

        </div>
        `;
    });

    html = `

<div class="page-title">

    我的提交

</div>

<div class="submit-toolbar">

    <button onclick="openDailyReport()">

        写日报

    </button>

    <button onclick="openMeeting()">

        写会议记录

    </button>

    <button onclick="openProjectProgress()">

        写项目进展

    </button>

</div>

`;

    document.getElementById(
        "dashboard-root"
    ).innerHTML = html;
}

/* =====================
   AI分析
===================== */

async function loadAI(){

    setActiveMenu(3);

    const root =
        document.getElementById(
            "dashboard-root"
        );

    root.innerHTML=`

        <div class="page-title">

            AI分析

        </div>

        <div id="aiPanel"></div>

    `;

    loadAIAnalysis();

}


/* =====================
   个人中心
===================== */

async function loadProfile(){

    setActiveMenu(4);

    const root =
        document.getElementById(
            "dashboard-root"
        );
    const user = getCurrentUser();
    root.innerHTML=`

        <div class="page-title">

            个人中心

        </div>

        <div class="card">

            用户：

            ${user}

        </div>

    `;

}

async function renderPieChart(){

    const chartDom =
        document.getElementById(
            "pieChart"
        );

    if(!chartDom){

        console.log("pieChart不存在");

        return;
    }

    const chart =
        echarts.init(chartDom);

    chart.setOption({

        tooltip:{},

        series:[{

            type:"pie",

            radius:"65%",

            data:Object.keys(
                window.PIE_DATA
            ).map(k=>({

                name:k,

                value:window.PIE_DATA[k]

            }))

        }]

    });

}

async function renderLineChart(){

    const chartDom =
        document.getElementById(
            "lineChart"
        );

    if(!chartDom){

        console.log("lineChart不存在");

        return;
    }

    const chart =
        echarts.init(chartDom);

    chart.setOption({

        tooltip:{},

        xAxis:{

            type:"category",

            data:
            window.LINE_DATA.map(
                i=>i.date
            )

        },

        yAxis:{

            type:"value"

        },

        series:[{

            type:"line",

            smooth:true,

            data:
            window.LINE_DATA.map(
                i=>i.count
            )

        }]

    });

}

/* =====================
   我的项目
===================== */

async function loadProject(){

    setActiveMenu(1);

    const user =
        getCurrentUser();

    const rows =
        await fetch(
            "/api/dashboard/project?user="+user
        ).then(r=>r.json());

    let html=`

    <div class="page-title">

        我的项目

    </div>

    <table class="project-table">

        <tr>

            <th>项目名称</th>

            <th>负责人</th>

            <th>进度</th>

            <th>风险</th>

            <th>更新时间</th>

        </tr>
    `;

    rows.forEach(r=>{

        html += `
        <tr>

            <td>${r.project_name}</td>

            <td>${r.leader}</td>

            <td>${r.progress}</td>

            <td>${r.risk}</td>

            <td>${r.update_time}</td>

        </tr>
        `;
    });

    html += "</table>";

    document.getElementById(
        "dashboard-root"
    ).innerHTML = html;
}

async function loadAI(){

    setActiveMenu(3);

    const user =
        getCurrentUser();

    const ai =
        await fetch(
            "/api/dashboard/ai?user="+user
        ).then(r=>r.json());

    const weekly =
        await fetch(
            "/api/dashboard/weekly?user="+user
        ).then(r=>r.json());

    const risk =
        await fetch(
            "/api/dashboard/risk?user="+user
        ).then(r=>r.json());

    let riskHtml="";

    risk.forEach(r=>{

        riskHtml += `
        <div class="risk-item">

            <b>${r.project}</b>

            <span>
                ${r.risk}
            </span>

        </div>
        `;
    });

    document.getElementById(
        "dashboard-root"
    ).innerHTML = `

    <div class="ai-page">

        <div class="ai-card">

            <h2>
                🤖 AI分析
            </h2>

            <pre>
${ai.content}
            </pre>

        </div>

        <div class="ai-card">

            <h2>
                ⚠ 风险预警
            </h2>

            ${riskHtml}

        </div>

        <div class="ai-card">

            <h2>
                📝 自动周报
            </h2>

            <pre>
${weekly.content}
            </pre>

        </div>

    </div>
    `;
}

function openDailyPage(){

    document.querySelector(
        "#daily_page_btn"
    ).click();
}

function openMeetingPage(){

    document.querySelector(
        "#meeting_page_btn"
    ).click();
}

function openProjectPage(){

    document.querySelector(
        "#project_page_btn"
    ).click();
}

async function renderProjectRank(){

    const rows =
        await fetch(
            "/api/dashboard/rank"
        ).then(r=>r.json());

    const chart =
        echarts.init(
            document.getElementById(
                "projectRankChart"
            )
        );

    chart.setOption({

        title:{
            text:"项目健康度排行"
        },

        tooltip:{},

        xAxis:{
            type:"value"
        },

        yAxis:{
            type:"category",

            data:rows.map(
                i=>i[0]
            )
        },

        series:[{

            type:"bar",

            data:rows.map(
                i=>parseInt(
                    String(i[1]).replace("%","")
                )
            )

        }]
    });
}

async function generateDaily(){
    const task =
        prompt(
            "请输入今天完成的工作"
        );

    if(!task) return;

    const data =
        await fetch(
            "/api/ai/daily?task="+task
        ).then(r=>r.json());

    alert(data.content);
}

async function generateMeeting(){

    const txt =
        prompt(
            "粘贴会议记录"
        );

    if(!txt) return;

    const data =
        await fetch(
            "/api/ai/meeting?content="+txt
        ).then(r=>r.json());

    alert(data.content);
}
