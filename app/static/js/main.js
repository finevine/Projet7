const IMG_PATH= "/static/img"

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
  append_message('Oui ! '.concat(api_answer.title),'bot')
  setTimeout(function(){
    append_message("C'est au ".concat(api_answer.formatted_address),'bot')
  }, 500);
  setTimeout(function(){
    append_message("Et d'ailleurs sais tu que : ".concat(api_answer.story),'bot')
  }, 1000);
}

function append_message(text, from) {
  var message = document.createElement("div");
  var img_cont = document.createElement("div");
  img_cont.className = 'img_cont_msg';
  var img = document.createElement("img");
  img.className = 'img_cont_msg rounded-circle user_img_msg';
  img_cont.appendChild(img);
  var message_text = document.createElement('div');

  switch (from) {
    case "bot":
      message.className = 'd-flex justify-content-start mb-4';
      img.setAttribute("src", IMG_PATH + "/grandpy.jpg");
      img.setAttribute("alt", "Bot");
      message_text.className = 'msg_cotainer';
      message.appendChild(img_cont);
      message.appendChild(message_text);
      break;
    case "user":
      message.className = 'd-flex justify-content-end mb-4';
      img.setAttribute("src",  IMG_PATH + "/avatar_generic.jpg");
      img.setAttribute("alt", "User");
      message_text.className = 'msg_cotainer_send';
      message.appendChild(message_text);
      message.appendChild(img_cont);
        break;
    default:
      var message = '';
  }
  message_text.innerHTML = text;
  var chat = document.getElementById('chat_body');
  chat.appendChild(message); 
  chat.scrollTop = chat.scrollHeight;
}
