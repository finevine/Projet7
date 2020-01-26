function get_answer(question) {
    var xhr = new XMLHttpRequest(),
        method = "GET",
        url = "/answer/" + question;

    xhr.open(method, url, true);
    xhr.onreadystatechange = function () {
        if(xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            document.getElementById("messageToSend").value = "";
        }
    };
    xhr.send();
  }

  