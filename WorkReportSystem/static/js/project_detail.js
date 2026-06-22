let currentProgressId = null;
window.editProjectProgress = function(id){
    currentProgressId = id;

    document.getElementById(
        "edit_progress_id"
    ).value = id;

    document.querySelector(
        "#load_progress_btn"
    ).click();

    document.getElementById(
        "progressEditModal"
    ).style.display = "flex";
}

window.deleteProjectProgress = function(id){
    currentProgressId = id;

    document.getElementById(
        "deleteProgressModal"
    ).style.display = "flex";

}

window.closeDeleteProgressModal = function(){

    document.getElementById(
        "deleteProgressModal"
    ).style.display = "none";
}

window.confirmDeleteProgress = function(){

    document.getElementById(
        "delete_progress_id"
    ).value = currentProgressId;

    document.querySelector(
        "#delete_progress_btn"
    ).click();

    closeDeleteProgressModal();
}

window.closeProgressModal = function(){

    document.getElementById(
        "progressEditModal"
    ).style.display = "none";
}

window.addProject=function(){

    document.getElementById("p_id").value="";

    document.getElementById("p_name").value="";

    document.getElementById("p_leader").value="";

    document.getElementById("p_developers").value="";

    document.getElementById("p_testers").value="";

    document.getElementById("p_designer").value="";

    document.getElementById("p_structure").value="";

    document.getElementById("p_start_date").value="";

    document.getElementById("p_end_date").value="";

    document.getElementById("p_progress").value="";

    document.getElementById("p_delay").value="否";

    document.getElementById("p_risk").value="";

    document.getElementById(
        "project_modal_title"
    ).innerText="新增项目";

    document.getElementById(
        "projectModal"
    ).style.display="flex";
};

window.deleteMember=function(id){
    const box=
    document.querySelector(
        "#delete_member_id textarea"
    );
    if(box){
        box.value=id;

        box.dispatchEvent(
            new Event(
                "input",
                {bubbles:true}
            )
        );
    }

}

window.deleteRisk=function(id){
    const box=
    document.querySelector(
        "#delete_risk_id textarea"
    );
    if(box){
        box.value=id;
        box.dispatchEvent(
            new Event(
                "input",
                {bubbles:true}
            )
        );
    }
}

window.viewProject=function(

    project_name,

    leader,

    developers,

    testers,

    designer,

    structure,

    start_date,

    end_date,

    progress,

    delay,

    risk

){

    document.getElementById(
        "project_detail_content"
    ).innerHTML=`

        <div class="project-detail-item">
            <b>项目名称：</b>
            ${project_name}
        </div>

        <div class="project-detail-item">
            <b>项目负责人：</b>
            ${leader}
        </div>

        <div class="project-detail-item">
            <b>开发人员：</b>
            ${developers}
        </div>

        <div class="project-detail-item">
            <b>测试人员：</b>
            ${testers}
        </div>

        <div class="project-detail-item">
            <b>UI设计：</b>
            ${designer}
        </div>

        <div class="project-detail-item">
            <b>结构工程师：</b>
            ${structure}
        </div>

        <div class="project-detail-item">
            <b>项目周期：</b>
            ${start_date}
            ~
            ${end_date}
        </div>

        <div class="project-detail-item">
            <b>是否延期：</b>
            ${delay}
        </div>

        <div class="project-detail-item">
            <b>风险说明：</b>
            ${risk}
        </div>

        <div class="project-detail-item">
            <b>项目进度：</b>
            <br>
            ${progress}
        </div>

    `;

    document.getElementById(
        "projectViewModal"
    ).style.display="flex";
};

window.closeProjectViewModal=function(){

    document.getElementById(
        "projectViewModal"
    ).style.display="none";

};

