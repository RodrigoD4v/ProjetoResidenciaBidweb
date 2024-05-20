function runScan() {
  var url = document.getElementById('url-input').value;
  var csrftoken = getCookie('csrftoken');
  var username = "{{ user.username }}";

  fetch('/run_scan/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrftoken
      },
      body: 'url=' + encodeURIComponent(url) + '&username=' + encodeURIComponent(username)
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Erro na resposta da rede.');
      }
      return response.blob();
  })
  .then(blob => {
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'report.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      alert('Scan concluído! O relatório foi baixado.');
  })
  .catch(error => {
      console.error('Erro:', error);
      alert('Erro ao executar o scan: ' + error.message);
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
