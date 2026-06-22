custom_css = """
*{
    font-family:"Microsoft YaHei","Inter",sans-serif;
    box-sizing:border-box !important;
}
html,body{
    margin:0;padding:0;min-height:100vh;
    overflow-x:hidden !important;overflow-y:auto;
    background:#0b101d;
    background-image:radial-gradient(rgba(30,120,255,.08) 1px,transparent 1px),radial-gradient(rgba(30,120,255,.08) 1px,transparent 1px);
    background-size:25px 25px;
}
.app,.main,.gradio-container{width:100%;}

/* ========== PC ≥901px 严格70%宽度 超高权重 ========== */
@media screen and (min-width:901px){
    html body div.gradio-container{
        width:70% !important;
        max-width:1400px !important;
        min-width:1000px !important;
        margin:0 auto !important;
        padding:18px !important;
    }
}

.header-wrap{
    width:100%;background:linear-gradient(135deg,#04152f,#0a2866,#0f4cb8);
    border-radius:16px;padding:20px 24px;border:1px solid rgba(80,180,255,.35);
    box-shadow:0 0 20px rgba(50,150,255,.35),0 8px 25px rgba(0,0,0,.35);margin-bottom:18px;
}
.header-wrap h1{margin:0;color:white;font-size:28px;}
.header-wrap p{color:#bddcff;margin-top:8px;}
.card-box{
    width:100%;background:linear-gradient(145deg,#101a30,#162848);border-radius:16px;padding:16px;
    border:1px solid rgba(70,170,255,.25);box-shadow:0 0 20px rgba(40,120,255,.15);
}
[data-testid="chatbot"]{width:100% !important;height:70vh !important;}
[data-testid="chatbot"] .message{max-width:85% !important;width:auto !important;}
[data-testid="chatbot"] .message.user{background:linear-gradient(135deg,#0089a8,#00b6c7) !important;color:white !important;border-radius:18px 6px 18px 18px !important;}
[data-testid="chatbot"] .message.bot{background:linear-gradient(135deg,#0a1630,#12264d) !important;color:white !important;border:1px solid rgba(80,140,255,.15) !important;}
[data-testid="chatbot"] .message p{white-space:pre-wrap !important;word-break:break-word !important;overflow-wrap:anywhere !important;line-height:1.7;}
#query-input{width:100%;}
#query-input textarea{background:#0c162c !important;color:#eaf3ff !important;border-radius:14px !important;border:1px solid rgba(80,180,255,.3) !important;min-height:44px !important;font-size:15px !important;}
#query-input textarea:focus{border-color:#39a0ff !important;box-shadow:0 0 0 3px rgba(50,150,255,.2),0 0 20px rgba(50,150,255,.3) !important;}
footer,[data-testid="footer"]{display:none !important;}
::-webkit-scrollbar{width:8px;}
::-webkit-scrollbar-thumb{background:#2d65b8;border-radius:8px;}

/* ========== 手机 ≤900px 固定95% ========== */
@media screen and (max-width:900px){
    html body div.gradio-container{
        width:95% !important;
        max-width:95% !important;
        min-width:0 !important;
        margin:0 auto !important;
        padding:4px !important;
    }
    .header-wrap{padding:12px !important;}
    .header-wrap h1{font-size:20px !important;line-height:1.4 !important;}
    .card-box{padding:6px !important;max-width:100% !important;}
    [data-testid="chatbot"]{height:60vh !important;max-width:100% !important;}
    .gr-box,.gr-form,.gr-input,.gr-button,div[class*="row"],div[class*="column"]{max-width:100% !important;}
}
"""