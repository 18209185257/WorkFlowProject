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

function changePassword(){

    const oldPwd =

        document.getElementById(
            "oldPwd"
        ).value;

    const newPwd =

        document.getElementById(
            "newPwd"
        ).value;

    const oldBox =

        document.querySelector(
            "#old_pwd_event textarea"
        );

    const newBox =

        document.querySelector(
            "#new_pwd_event textarea"
        );

    oldBox.value = oldPwd;

    newBox.value = newPwd;

    oldBox.dispatchEvent(

        new Event(
            "input",
            {bubbles:true}
        )

    );

    newBox.dispatchEvent(

        new Event(
            "input",
            {bubbles:true}
        )

    );

    document
    .getElementById(
        "change_pwd_btn"
    )
    .click();

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

    const data = window.PROJECT_DETAIL_DATA?.[id];

    if(!data){
        console.error("项目不存在:", id);
        return;
    }

    document.getElementById("projectModalBody").innerHTML = `
        <h2>${data.name}</h2>
        <p>负责人：${data.leader}</p>
        <p>进度：${data.progress}%</p>
        <p>风险：${data.risk}</p>
    `;

    document.getElementById("projectModal").style.display = "flex";
}

function openSubmitDetail(id){

    const data = window.SUBMIT_DETAIL_DATA?.[id];

    if(!data){
        console.error("提交不存在:", id);
        return;
    }

    document.getElementById("submitModalBody").innerHTML = `
        <h3>${data.type}</h3>
        <p>日期：${data.date}</p>
        <p>${data.content}</p>
    `;

    document.getElementById("submitModal").style.display = "flex";
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

function closeModal(id){

    document.getElementById(
        id
    ).style.display="none";

}

function getProjectData(id){
    const root =
        document.getElementById(
            "projectData"
        );

    const data =
        JSON.parse(
            root.dataset.json
        );

    return data[id];
}

function getProjectData(id){
    const root =
        document.getElementById(
            "projectData"
        );

    const data =
        JSON.parse(
            root.dataset.json
        );

    return data[id];
}

function toggleSubmitRow(row){

    const dom =
        row.querySelector(".submit-desc");

    const opened =
        dom.dataset.opened === "1";

    if(opened){

        dom.innerText =
            dom.dataset.short;

        dom.dataset.opened = "0";

    }else{

        dom.innerText =
            dom.dataset.full;

        dom.dataset.opened = "1";

    }

}
function toggleProjectRow(row){

    const dom =
        row.querySelector(".p-progress");

    const opened =
        dom.dataset.opened === "1";

    if(opened){

        dom.innerText =
            dom.dataset.short;

        dom.dataset.opened = "0";

    }else{

        dom.innerText =
            dom.dataset.full;

        dom.dataset.opened = "1";

    }

}

function runAI(type){
     const box = document.getElementById("ai-result");
     box.innerHTML = "🤖 AI分析中，请稍等...";
     if(type==="project"){
         document.getElementById(
        "ai_" + type + "_btn1"
     ).click();
     }else{
         document.getElementById(
        "ai_" + type + "_btn"
     ).click();
     }
}

function askAI() {

    const input =
        document.getElementById("ai-question");

    const question = input.value;

    if (!question) return;

    const eventBox =
        document.getElementById("ai_question_event");

    if (!eventBox) {
        console.error("ai_question_event not found");
        return;
    }

    // 1️⃣ 写入Gradio事件
    eventBox.value = question;

    eventBox.dispatchEvent(
        new Event("input", { bubbles: true })
    );

    // 2️⃣ 触发AI分析状态（关键）
    const resultBox =
        document.getElementById("ai-result");

    resultBox.innerHTML = "🤖 AI正在分析中...";

    // 3️⃣ 点击隐藏按钮（触发后端）
    const sendBtn =
        document.getElementById("ai_send_btn");

    if (!sendBtn) {
        console.error("ai_send_btn not found");
        return;
    }

    sendBtn.click();

    // 4️⃣ 清空输入框（修复点）
    input.value = "";

}

window.addEventListener(
    "ai-result-update",
    function(e){

        const box =
        document.getElementById(
            "ai-result"
        );

        if(box){

            box.innerHTML =
            e.detail;
        }
    }
);

document.addEventListener(
"keydown",
function(e){

    if(
        e.key === "Enter"
        &&
        !e.shiftKey
    ){

        const box =
        document.getElementById(
            "ai-question"
        );

        if(
            document.activeElement
            === box
        ){

            e.preventDefault();

            askAI();

        }

    }

});

const observer = new MutationObserver(

function(){

    const status =
    document.getElementById(
        "ai-status-bar"
    );

    if(status){

        status.style.display =
        "none";

    }
}

);

observer.observe(

    document.getElementById(
        "ai-result"
    ),

    {
        childList:true,
        subtree:true
    }

);

function resetAIState() {

    const box =
        document.getElementById("ai-result");

    if (box) {
        box.innerHTML = "";
    }

}

function openAIAssistant(){

    showPage(
        "page-ai"
    );

}

const pwdResult =

document.querySelector(
"#pwd_result textarea"
);

if(pwdResult){

    pwdResult.addEventListener(

        "input",

        function(){

            const result =

            pwdResult.value;

            if(!result){

                return;

            }

            if(result === "SUCCESS"){

                alert(
                    "密码修改成功，请重新登录"
                );

                location.reload();

                return;

            }

            alert(result);

        }

    );

}

setInterval(function(){

    const box =
    document.querySelector(
        "#pwd_result textarea"
    );

    if(!box){
        return;
    }

    const msg = box.value;

    if(!msg){
        return;
    }

    box.value = "";

    if(msg.startsWith("SUCCESS")){

        alert("密码修改成功，请重新登录");

        location.reload();

        return;
    }

    if(msg.startsWith("ERROR")){

        alert(
            msg.replace(
                "ERROR:",
                ""
            )
        );
    }

},500);