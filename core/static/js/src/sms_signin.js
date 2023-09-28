document.addEventListener('DOMContentLoaded', function () {
    // 获取发送短信按钮和消息框的元素
    const sendSmsButton = document.getElementById('sendSmsButton');
    const messageBox = document.getElementById('messageBox');

    // 添加发送短信按钮的点击事件
    sendSmsButton.addEventListener('click', function () {
        const phoneNumber = document.getElementById('phonenumber').value;
        if (!phoneNumber) {
            messageBox.textContent = '请先填写手机号';
            return;
        }

        // 发送 AJAX 请求
        fetch('/sms_sign_in/', {
            method: 'POST',
            body: JSON.stringify({ phonenumber: phoneNumber }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // 获取 CSRF Token 的方法需要根据实际情况实现
            },
        })
        .then(response => response.json())
        .then(data => {
            messageBox.textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            messageBox.textContent = '短信验证码发送失败，请稍后重试。';
        });
    });

    // 获取 CSRF Token 的函数
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});