from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d %H:%M")

def build_profile_page(
    username,
    real_name,
    avatar_color
):
    return f"""
           <!-- 个人中心 -->
    <div id="page-profile"
     class="page hidden">

            <div class="page-header">
        
                <h2>👤 个人中心</h2>
        
            </div>

    <div class="profile-layout">

        <!-- 左侧 -->

        <div class="profile-left">

            <div class="user-card">

                <div
                    class="avatar-big"
                    style="background:{avatar_color};">
                    
                        {real_name[0] if real_name else "U"}
                    
                    </div>

                <h3>{real_name}</h3>

                <p>{username}</p>

                <div class="user-info">

                    <div>

                        <label>身份</label>

                        <span>员工</span>

                    </div>

                    <div>

                        <label>最近登录</label>

                        <span>{now}</span>

                    </div>

                </div>

            </div>

        </div>

        <!-- 右侧 -->

        <div class="profile-right">

            <div class="password-card">

                <h3>

                    安全设置

                </h3>

                <input
                    id="oldPwd"
                    type="password"
                    placeholder="旧密码">

                <input
                    id="newPwd"
                    type="password"
                    placeholder="新密码">

                <button
                    onclick="changePassword()">

                    修改密码

                </button>

                <div id="pwdResult"></div>

            </div>

        </div>
    """