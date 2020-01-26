function get_answer(question) {
    var xhr = new XMLHttpRequest(),
        method = "GET",
        url = "/answer/" + question;

    xhr.open(method, url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            answer = xhr.responseText;
            append_bot_message(answer);
        }
    };
    xhr.send();
    append_user_message(question);
    clear_messageToSend();
  }

  var clear_messageToSend = function() {
    document.getElementById("messageToSend").value = "";
  }
  
  function add_message(htmlcode) {
    var d1 = document.getElementById('chat_body');
    d1.insertAdjacentHTML('beforeend', htmlcode);
  }

  function append_user_message(message) {
    var htmlcode = `<div class="d-flex justify-content-end mb-4">
                <div class="msg_cotainer_send">`
                    + message + 
                    `<span class="msg_time_send">{{ time }}</span>
                </div>
                <div class="img_cont_msg">
                    <img src="/static/img/avatar_generic.jpg" class="rounded-circle user_img_msg">
                </div>
            </div>`;
    
    var chat = document.getElementById('chat_body');
    chat.insertAdjacentHTML('beforeend', htmlcode); 
    chat.scrollTop = chat.scrollHeight;
  }

  function append_bot_message(message) {
    var htmlcode = `<div class="d-flex justify-content-start mb-4">
                        <div class="img_cont_msg">
                            <img src="/static/img/grandpy.jpg" class="img_cont_msg rounded-circle user_img_msg">
                        </div>
                        <div class="msg_cotainer">`
                            + message + 
                            `<span class="msg_time">{{ time }}</span>
                        </div>
                    </div>`;
    var chat = document.getElementById('chat_body');
    chat.insertAdjacentHTML('beforeend', htmlcode); 
    chat.scrollTop = chat.scrollHeight;
  }