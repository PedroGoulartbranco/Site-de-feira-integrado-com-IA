let pesquisa = document.getElementById("barra_pesquisa")
let botao_pesquisar = document.getElementById("botao_pesquisar")


botao_pesquisar.addEventListener("click", function(event){
    event.preventDefault(); //Não recarrega a pagina
    usuario_digitou = pesquisa.value
    console.log(usuario_digitou)

    fetch('http://127.0.0.1:5000/pesquisar', {
    method: 'POST',
    headers: {

        'Content-Type': 'application/json'

    },
    body: JSON.stringify(
        {pesquisa: usuario_digitou}
    )

    })

    .then(response => response.json())

    .then(data => {
        
    })

    .catch(error => console.log(error));
})