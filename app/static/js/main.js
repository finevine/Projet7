const IMG_PATH= "/static/img"


var clear_messageToSend = function() {
  document.getElementById("messageToSend").value = "";
}


function send_question () {
  var question = document.getElementById("messageToSend").value;
  get_answer(question);
}


function hello(){
  const name = document.querySelector("meta[name='user_name']").getAttribute('content');
  console.log(name);
  setTimeout(function(){
    var intro = "Salut ".concat(name).concat(". C'est chouette de te parler ! Je connais plein d'anecdote en géographie dans le monde entier: y'a qu'à demander !");
    append_message(intro, 'bot', false);
  }, 200);
}


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
    append_message(question, 'user', false)
    clear_messageToSend();
  }


function bot_says(api_answer) {
  var chat = document.getElementById('chat_body');
  const address = [
    "Oui, ça je connais, voilà où ça se trouve : ",
    "Alors, si mes souvenirs sont bon c'est là : ",
    "Ça remonte à y'a longtemps mais je crois que c'est ici : ",
    "Oui oui oui ! Voilà où c'est : ",
    "Bien sûr mon petit, voici l'adresse : ",
    "Of course my dear : ",
    "De mon temps c'était là : ",
    "Fouilla, tu m'en demandes beaucoup ! ",
    "Regarde donc le bottin ! Mais attend voir je crois savoir : "
  ]
  // Bot speaks here (address, map, stories...)
  var intro_address = address[Math.floor(Math.random() * address.length)]
  append_message(intro_address.concat(api_answer.formatted_address),'bot', false);

  setTimeout(function(){
    append_message(api_answer.img, 'bot', true);
  }, 1500);

  const stories = [
    "Et alors voilà que ",
    "À ce sujet, sais tu que : ",
    "De mon temps tout le monde savait que : ",
    "Retiens bien ça : ",
    "Si tu demandais à ton père, il te dirait que : ",
    "Attends voir tu connais celle-là ? ",
    "Si on t'en parle, tu pourrais te rappeler de ça ? ",
    "J'ai une mémoire d'éléphant ! Sais-tu que : ",
    "Je suis sûr que tu ne savais pas que : "
  ]
  // Bot speaks here (address, map, stories...)
  var intro_stories = stories[Math.floor(Math.random() * stories.length)];

  setTimeout(function(){
    append_message(intro_stories.concat(api_answer.stories),'bot', false);
    var chat = document.getElementById('chat_body');
    chat.scrollTop = chat.scrollHeight;
  }, 2500);
}


function append_message(text, from, map) {
  var message = document.createElement("div");

  var loader = document.createElement("div");
  loader.className = "loader";
  var spin = document.createElement("div");
  spin.appendChild(loader);

  var img = document.createElement("img");
  img.className = 'img_cont_msg rounded-circle user_img_msg';

  var img_cont = document.createElement("div");
  img_cont.className = 'img_cont_msg';
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

  var chat = document.getElementById('chat_body');
  chat.appendChild(message); 
  if (from == "bot"){
    message_text.appendChild(spin)
    setTimeout(function(){
      spin.innerHTML = " ";
      if (map == true) {
        var image = document.createElement("IMG");
        image.setAttribute("src", text);
        image.setAttribute("width", "300");
        image.setAttribute("height", "200");
        image.setAttribute("alt", "Je n'ai pas retrouvé la carte, désolé");
        message_text.appendChild(image);
        var chat = document.getElementById('chat_body');
        chat.scrollTop = chat.scrollHeight;
      } else {
        message_text.textContent = text;
      };
      var chat = document.getElementById('chat_body');
      chat.scrollTop = chat.scrollHeight;
    }, 1000);
  } else {
    message_text.textContent = text;
  }

  chat.scrollTop = chat.scrollHeight;
}
