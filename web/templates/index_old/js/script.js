Update_message();

const sending_message = document.getElementById("message");

// 输入框 和 消息 绑定（同步）
sending_message.addEventListener("input", function () {
    if (sending_message.value != '') {
        document.querySelector(".chat-box >  div:nth-child(2)").innerHTML = `
        <div class="message user">
            <p class="message-content user">` + sending_message.value + `</p>
        </div>
        `;
    }
    else {
        document.querySelector(".chat-box >  div:nth-child(2)").innerHTML = ``;
    };
});

// 回车 发送
sending_message.addEventListener("keydown", function (event) {
    if (event.keyCode === 13) {
        // 执行 发送 操作
        sending();
    }
});

// 更新消息窗口 
function Update_message() {
    localStorage.setItem('sending_state', "yes");
    local_cache = localStorage.getItem("local_cache");
    if (local_cache == null || local_cache == '') {
        local_cache = { data_message: [{ ai: '您好，我是智慧疾病咨询ai，我可以回答您关于疾病的一些问题' }] };
    }
    else {
        local_cache = JSON.parse(local_cache);
    };
    var html = ``;
    for (var i = 0; i < local_cache.data_message.length; i++) {
        message = local_cache.data_message[i];
        if (message.ai != null) {
            html += `
            <div class="message ai">
                <p class="message-content">` + message.ai + `</p>
            </div>
            `;
        };
        if (message.user != null) {
            html += `
            <div class="message user">
                <p class="message-content user">` + message.user + `</p>
            </div>
        `;
        };
    };
    document.querySelector(".chat-box >  div:nth-child(1)").innerHTML = html;

    
    // 设置默认情况下滚动到div的底部
    var element = document.getElementById("chat-box");
    element.scrollTop = element.scrollHeight;
}

// 清空
function empty() {
    localStorage.removeItem('local_cache'); // 本地存储空间.删除.('local_cache')
    document.getElementsByClassName("chat-box")[0].innerHTML = '<div></div><div></div>';
    Update_message();   // 更新消息窗口 
}

// 更新聊天数据
function updateChatData(chatData, message_user, message_ai) {
    // 将 chatData 保存至本地缓存
    var local_cache = localStorage.getItem('local_cache');
    if (local_cache != null) {
        local_cache = JSON.parse(local_cache);
        local_cache.data_message = chatData;
    }
    else {
        local_cache = { "data_message": chatData };
    }
    localStorage.setItem('local_cache', JSON.stringify(local_cache));

    // ==========
    // 更新消息窗口
    // ==========

    // 清空 输入框和消息的绑定（同步）
    document.querySelector(".chat-box >  div:nth-child(2)").innerHTML = '';
    // 更新用户消息
    document.querySelector(".chat-box >  div:nth-child(1)").innerHTML += `
        <div class="message user">
            <p class="message-content user">` + message_user + `</p>
        </div>
    `;

    // ==========
    // 更新 ai 消息
    // ==========

    html = document.querySelector(".chat-box >  div:nth-child(1)").innerHTML;
    // 定义函数 showText 逐字显示文本内容
    function showText(i, callback) {
        // 设置新内容
        document.querySelector(".chat-box >  div:nth-child(1)").innerHTML = html + `
        <div class="message ai">
            <p class="message-content ">` + message_ai.substr(0, i) + `</p>
        </div>
        `;
    
        // 使用 setTimeout 实现延时
        setTimeout(function () {
            // 递归调用函数
            if (i < message_ai.length) {
                showText(i + 1, callback);
            } else {
                callback();
            }
        }, 50);
    
        // 设置默认情况下滚动到div的底部
        var element = document.getElementById("chat-box");
        element.scrollTop = element.scrollHeight;
    }
    
    // 调用函数(showText)开始逐字显示文本内容
    showText(0, function() {
        // showText 执行完成后调用 localStorage.setItem()
        localStorage.setItem('sending_state', 'yes');
    });
}

// 发送
function sending() {
    var message_user = document.getElementById("message").value;
    // 输入的消息不为空 而且 发送状态（sending_state）为 yes
    if (message_user !== '' && localStorage.getItem('sending_state') === "yes") {
        var messages = document.getElementsByClassName("message-content");
        var chatData = [];
        var aiText = "";
        var userText = "";
        for (var i = 0; i < messages.length; i++) {
            if (messages[i].parentElement.classList.contains("ai")) {
                aiText = messages[i].innerHTML;
                chatData.push({ ai: aiText });
            } else if (messages[i].parentElement.classList.contains("user")) {
                userText = messages[i].innerHTML;
                chatData.push({ user: userText });
            }
        };

        // 清空 消息输入框
        document.getElementById("message").value = "";
        localStorage.setItem('sending_state', "no");

        $.ajax({
            type: "POST",
            url: "/api",
            contentType: "application/json",
            data: message_user,
            success: function (response) {
                // 处理请求成功后返回的数据
                var message_ai = (response.ai.replace(/\\n/g, "<br>")).replace(/\n/g, "<br>");
                chatData.push({ ai: message_ai });
                updateChatData(chatData, message_user, message_ai);
            },
            error: function () {
                // 处理请求失败情况
                var message_ai = "请求失败，请稍后重试";
                chatData.push({ ai: message_ai });
                updateChatData(chatData, message_user, message_ai);
            }
        });
        
    }
}