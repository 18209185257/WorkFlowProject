window.editCustomer=function(
    id,
    customer_name,
    contact_name,
    phone,
    email,
    address

){

    document.getElementById("c_id").value=id;

    document.getElementById("c_name").value=
        customer_name;

    document.getElementById("c_contact").value=
        contact_name;

    document.getElementById("c_phone").value=
        phone;

    document.getElementById("c_email").value=
        email;

    document.getElementById("c_address").value=
        address;

    document.getElementById(
        "customer_modal_title"
    ).innerText="编辑客户";

    document.getElementById(
        "customerModal"
    ).style.display="flex";
};

window.saveCustomer=function(){

    const data={

        id:
        document.getElementById("c_id").value,

        customer_name:
        document.getElementById("c_name").value,

        contact_name:
        document.getElementById("c_contact").value,

        phone:
        document.getElementById("c_phone").value,

        email:
        document.getElementById("c_email").value,

        address:
        document.getElementById("c_address").value
    };

    console.log("保存客户=",data);

    const box=
        document.querySelector(
            "#save_customer_event textarea"
        )
        ||
        document.querySelector(
            "#save_customer_event input"
        );

    console.log("事件框=",box);

    if(!box){
        alert("save_customer_event未找到");
        return;
    }

    box.value=JSON.stringify(data);

    box.dispatchEvent(
        new Event(
            "input",
            {bubbles:true}
        )
    );

    closeCustomerModal();
};

window.deleteCustomer=function(id){
    if(!confirm("确定删除客户？")){
        return;
    }
    const box=document.querySelector(
    "#delete_customer_event textarea"
    ) ||
    document.querySelector(
        "#delete_customer_event input"
    );
    box.value=id;
    box.dispatchEvent(
        new Event(
            "input",
            {bubbles:true}
        )
    );
};

window.openCustomerModal=function(){

    document.getElementById("c_id").value="";

    document.getElementById("c_name").value="";

    document.getElementById("c_contact").value="";

    document.getElementById("c_phone").value="";

    document.getElementById("c_email").value="";

    document.getElementById("c_address").value="";

    document.getElementById(
        "customer_modal_title"
    ).innerText="新增客户";

    document.getElementById(
        "customerModal"
    ).style.display="flex";
};

window.closeCustomerModal=function(){

    document.getElementById(
        "customerModal"
    ).style.display="none";
};

setInterval(()=>{

    const dom=
        document.getElementById(
            "dashboard_user"
        );

    if(dom && !window.dashboardStarted){

        window.dashboardStarted=true;

        startDashboard();

    }

},500);
