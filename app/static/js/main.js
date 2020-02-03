function get_answer(question) {
    var xhr = new XMLHttpRequest(),
        method = "GET",
        url = "/answer?question=" + question;

    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if(xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            answer = JSON.parse(xhr.responseText);
            bot_says(answer);
        }
    };
    xhr.send();
    // append_user_message(question);
    append_message(question, 'user')
    clear_messageToSend();
  }

var clear_messageToSend = function() {
  document.getElementById("messageToSend").value = "";
}

function bot_says(api_answer) {
  // Bot speaks here (address, map, stories...)
  append_message(api_answer.formatted_address, 'bot')
}

function append_message(message, from) {
  switch (from) {
    case "bot":
      // create element div pour éviter mélange html js
      var htmlcode = `<div class="d-flex justify-content-start mb-4">
          <div class="img_cont_msg">
              <img src="/static/img/grandpy.jpg" class="img_cont_msg rounded-circle user_img_msg">
          </div>
          <div class="msg_cotainer">`
              + message + 
              `<span class="msg_time">{{ time }}</span>
          </div>
      </div>`;
      break;
    case "user":
      var htmlcode = `<div class="d-flex justify-content-end mb-4">
      <div class="msg_cotainer_send">`
          + message + 
          `<span class="msg_time_send">{{ time }}</span>
      </div>
      <div class="img_cont_msg">
          <img src="/static/img/avatar_generic.jpg" class="rounded-circle user_img_msg">
      </div>
      </div>`;
        break;
    default:
      var htmlcode = '';
  }
  var chat = document.getElementById('chat_body');
  chat.insertAdjacentHTML('beforeend', htmlcode); 
  chat.scrollTop = chat.scrollHeight;
}
