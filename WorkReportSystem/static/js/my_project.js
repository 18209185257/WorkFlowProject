window.viewMyProject = function(id){
    const box =
    document.querySelector(
        "#current_project_id textarea"
    );
    if(box){
        box.value = id;
        box.dispatchEvent(
            new Event(
                "input",
                {bubbles:true}
            )
        );
    }
    const btn =
    document.querySelector(
        "#open_project_btn"
    );
    if(btn){
        btn.click();
    }
}

function openMyProject(projectId){
    const idBox =
        document.querySelector(
            "#current_project_id textarea"
        );
    if(idBox){
        idBox.value = projectId;
        idBox.dispatchEvent(
            new Event(
                "input",
                {bubbles:true}
            )
        );
    }
    const btn =
        document.querySelector(
            "#load_project_btn button"
        );
    if(btn){
        btn.click();
    }
}