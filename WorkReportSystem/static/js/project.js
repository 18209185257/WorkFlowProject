window.editUser = function(
    username,
    name,
    phone,
    role
){

    console.log(
        "edit",
        username,
        name,
        phone,
        role
    );

    currentUser = username;

    document.getElementById("m_username").value = username;
    document.getElementById("m_name").value = name;
    document.getElementById("m_phone").value = phone;
    document.getElementById("m_role").value = role;

    document.getElementById("editModal").style.display = "flex";
};
window.deleteUser = function(username){

    console.log("delete", username);

    window.currentDeleteUser = username;

    document.getElementById(
        "delete_username"
    ).innerHTML =
        "确定删除用户：" + username + " ?";

    document.getElementById(
        "deleteModal"
    ).style.display = "flex";
}

window.closeEditModal = function(){

    document.getElementById(
        "editModal"
    ).style.display = "none";
}

window.closeDeleteModal = function(){

    document.getElementById(
        "deleteModal"
    ).style.display = "none";
}

window.saveUser = function(){

    const data = {
        username: document.getElementById("m_username").value,
        name: document.getElementById("m_name").value,
        phone: document.getElementById("m_phone").value,
        role: document.getElementById("m_role").value
    };

    console.log(data);

    const box =
        document.querySelector(
            "#save_user_event textarea"
        );

    if(!box){
        console.log("save_user_event没找到");
        return;
    }

    box.value = JSON.stringify(data);

    box.dispatchEvent(
        new Event(
            "input",
            { bubbles:true }
        )
    );

     setTimeout(() => {

        document.getElementById(
            "editModal"
        ).style.display = "none";

    },300);
};

window.confirmDeleteUser = function(){

    const box =
        document.querySelector(
            "#delete_user_event textarea"
        );

    if(!box){
        console.log("delete_user_event没找到");
        return;
    }

    box.value =
        window.currentDeleteUser;

    box.dispatchEvent(
        new Event(
            "input",
            { bubbles:true }
        )
    );

     setTimeout(() => {

        document.getElementById(
            "deleteModal"
        ).style.display = "none";

    },300);
};

window.editProject=function(

    id,

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

    console.log("进入编辑");

    document.getElementById("p_id").value=id;

    document.getElementById("p_name").value=
        project_name;

    document.getElementById("p_leader").value=
        leader;

    document.getElementById("p_developers").value=
        developers;

    document.getElementById("p_testers").value=
        testers;

    document.getElementById("p_designer").value=
        designer;

    document.getElementById("p_structure").value=
        structure;

    document.getElementById("p_start_date").value=
        start_date;

    document.getElementById("p_end_date").value=
        end_date;

    document.getElementById("p_progress").value=
        progress;

    document.getElementById("p_delay").value=
        delay;

    document.getElementById("p_risk").value=
        risk;

    document.getElementById(
        "project_modal_title"
    ).innerText="编辑项目";

    document.getElementById(
        "projectModal"
    ).style.display="flex";
};

window.closeProjectModal=function(){
    document.getElementById(
        "projectModal"
    ).style.display="none";

    };

window.saveProject=function(){
    const data={
    id:
        document.getElementById("p_id").value,

    project_name:
        document.getElementById("p_name").value,

    main_leader:
        document.getElementById("p_leader").value,

    developers:
        document.getElementById("p_developers").value,

    testers:
        document.getElementById("p_testers").value,

    designer:
        document.getElementById("p_designer").value,

    structure:
        document.getElementById("p_structure").value,

    start_date:
        document.getElementById("p_start_date").value,

    end_date:
        document.getElementById("p_end_date").value,

    progress:
        document.getElementById("p_progress").value,

    delay:
        document.getElementById("p_delay").value,

    risk:
        document.getElementById("p_risk").value

};

    const box=document.querySelector(
        "#save_project_event textarea"
    );
    console.log(data);
    box.value=JSON.stringify(data);

    box.dispatchEvent(
        new Event(
            "input",
            {bubbles:true}
        )
    );

    closeProjectModal();

};

window.deleteProject=function(
    id,
    name
){

    window.currentProject=id;

    document.getElementById(
        "delete_project_name"
    ).innerHTML= "确定删除项目："+name+" ?";

    document.getElementById(
        "projectDeleteModal"
    ).style.display="flex";

};

window.closeProjectDeleteModal=function(){

    document.getElementById(
    "projectDeleteModal"
    ).style.display="none";

};

window.confirmDeleteProject=function(){

    const box=document.querySelector(
        "#delete_project_event textarea"
    );

    box.value=window.currentProject;

    box.dispatchEvent(
    new Event("input",
        {bubbles:true}
    )
    );

    closeProjectDeleteModal();

};
window.viewProject=function(id){
    const box=document.querySelector(
    "#project_detail_event textarea"
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

window.selectMyProject = function(projectId){
    const box = document.querySelector(
        "#current_project_id textarea"
    );
    if(!box){
        console.log("current_project_id没找到");
        return;
    }
    box.value = projectId;
    box.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );
    alert("项目已选中");
}

window.selectProject=function(projectId){
    const box=document.querySelector(
        "#current_project_id textarea"
    );
    if(!box){
        return;
    }
    box.value=projectId;
    box.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );
    const refreshBox=document.querySelector(
        "#refresh_progress_btn"
    );
    if(refreshBox){
        refreshBox.click();
    }
    const kpiBtn=document.querySelector(
    "#refresh_project_kpi_btn"
);

if(kpiBtn){
    kpiBtn.click();
}
}

window.deleteMyProgress=function(id){
    const box=document.querySelector(
        "#delete_progress_id textarea"
    );
    box.value=id;
    box.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );
    document.querySelector(
        "#delete_progress_btn"
    ).click();
}

window.editMyProgress=function(id){
    const box=document.querySelector(
        "#edit_progress_id textarea"
    );
    box.value=id;
    box.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );
    document.querySelector(
        "#load_progress_btn"
    ).click();
}

window.editMyProgress=function(id){
    const box=document.querySelector(
        "#edit_progress_id textarea"
    );
    box.value=id;
    box.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );
    document.querySelector(
        "#load_progress_btn"
    ).click();
}

window.openMyProgressModal=function(
    progress,
    risk,
    nextPlan
){
    document.getElementById(
        "mp_progress"
    ).value=progress;

    document.getElementById(
        "mp_risk"
    ).value=risk;

    document.getElementById(
        "mp_next"
    ).value=nextPlan;

    document.getElementById(
        "myProgressModal"
    ).style.display="flex";
}

window.closeMyProgressModal=function(){
    document.getElementById(
        "myProgressModal"
    ).style.display="none";
}

window.saveMyProgress=function(){
    document.querySelector(
        "#edit_progress_content textarea"
    ).value=
    document.getElementById(
        "mp_progress"
    ).value;

    document.querySelector(
        "#edit_risk_content textarea"
    ).value=
    document.getElementById(
        "mp_risk"
    ).value;

    document.querySelector(
        "#edit_next_plan textarea"
    ).value=
    document.getElementById(
        "mp_next"
    ).value;

    document.querySelector(
        "#save_edit_progress_btn"
    ).click();

    closeMyProgressModal();
}

window.deleteMyProgress=function(id){
    window.currentMyProgress=id;
    document.getElementById(
        "myProgressDeleteModal"
    ).style.display="flex";
}

window.closeDeleteMyProgressModal=function(){
    document.getElementById(
        "myProgressDeleteModal"
    ).style.display="none";
}

window.confirmDeleteMyProgress=function(){
    const box=document.querySelector(
        "#delete_progress_id textarea"
    );
    box.value=
    window.currentMyProgress;
    box.dispatchEvent(
        new Event(
            "input",
            {
                bubbles:true
            }
        )
    );
    document.querySelector(
        "#delete_progress_btn"
    ).click();
    closeDeleteMyProgressModal();
}

