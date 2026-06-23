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
    if(pageName==="ai"){
        loadAI()
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

    const lineData = JSON.parse(
            document
            .getElementById(
                "trend7Data"
            )
            .value
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

function reloadTrend(days){

    let rows = [];

    if(days == "7"){

        rows = JSON.parse(
            document
            .getElementById(
                "trend7Data"
            )
            .value
        );

    }

    if(days == "15"){

        rows = JSON.parse(
            document
            .getElementById(
                "trend15Data"
            )
            .value
        );

    }

    if(days == "30"){

        rows = JSON.parse(
            document
            .getElementById(
                "trend30Data"
            )
            .value
        );

    }

    const chart =
        echarts.getInstanceByDom(
            document.getElementById(
                "lineChart"
            )
        );

    chart.setOption({

        xAxis:{

            data:rows.map(
                r=>r.date
            )

        },

        series:[{

            data:rows.map(
                r=>r.count
            )

        }]

    });

}

function openProjectDetail(id){

    fetch(`/api/project/detail?id=${id}`)
    .then(r=>r.json())
    .then(data=>{

        document.getElementById("dashboard-root").innerHTML = `

        <div class="detail-page">

            <div class="detail-header">

                <h2>📁 项目详情</h2>

                <button onclick="loadWorkbench()">
                    ← 返回
                </button>

            </div>

            <div class="detail-card">

                <p>项目名称：${data.name}</p>
                <p>进度：${data.progress}%</p>
                <p>负责人：${data.leader}</p>
                <p>开发：${data.dev}</p>
                <p>测试：${data.test}</p>
                <p>风险：${data.risk}</p>
                <p>更新时间：${data.time}</p>

            </div>

        </div>

        `;

    });

}

function openSubmitDetail(id){
    fetch(`/api/submit/detail?id=${id}`)
    .then(r=>r.json())
    .then(data=>{
        const modal =
        document.createElement("div");
        modal.className="modal";
        modal.innerHTML = `
        <div class="modal-content">
            <h3>📤 提交详情</h3>
            <p><b>用户：</b>${data.user}</p>
            <p><b>日期：</b>${data.date}</p>
            <p><b>内容：</b>${data.content}</p>
            <p><b>帮助事项：</b>${data.help}</p>
            <button onclick="this.parentNode.parentNode.remove()">
                关闭
            </button>
        </div>
        `;
        document.body.appendChild(modal);
    });
}

function showSubmitDetail(date,content){

    const modal =
    document.createElement("div");

    modal.className="modal";

    modal.innerHTML=`

    <div class="modal-content">

        <h3>提交详情</h3>

        <p>${date}</p>

        <hr>

        <pre>${content}</pre>

        <button
          onclick="this.parentNode.parentNode.remove()">

            关闭

        </button>

    </div>
    `;

    document.body.appendChild(modal);

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
