function renderLeaderCharts(){
    console.log(
        "图表数量:",
        document.querySelectorAll(
            ".leader-chart"
        ).length
    );

    document
    .querySelectorAll(
        ".leader-chart"
    )
    .forEach(dom=>{

        const option =
        JSON.parse(
            dom.dataset.option
        );

        let chart =
        echarts.getInstanceByDom(
            dom
        );

        if(chart){

            chart.dispose();

        }

        chart =
        echarts.init(
            dom
        );

        chart.setOption(
            option
        );

    });

}