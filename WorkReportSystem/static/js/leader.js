function openAIPanel(){
    document
    .getElementById("ai-panel")
    .classList
    .add("show")

}

function openAIPanel(){

    document
    .getElementById("ai-panel")
    .classList.remove("hidden");

}

function closeAIPanel(){

    document
    .getElementById("ai-panel")
    .classList.add("hidden");

}

function refreshLeaderDashboard(){

    const btn = document.getElementById(
        "leader_refresh_btn"
    );

    if(btn){

        btn.click();

    }

}

