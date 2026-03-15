let pesquisa = document.getElementById("barra_pesquisa")
let botao_pesquisar = document.getElementById("botao_pesquisar")
let filtros = ['nenhum']
let mostrar_filtros = document.getElementById("filtros")
let produtos = []
let pegou_produtos = false

mostrar_filtros.innerHTML= filtros


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
        atualizar_filtro(data.filtros)
    })

    .catch(error => console.log(error));
})

function atualizar_filtro(filtros) {
    mostrar_filtros.innerHTML= filtros
}

async function pegar_produtos() {
    fetch('http://127.0.0.1:5000/pegar_produtos')
    
        .then(response => response.json())
    
        .then(data => {
            produtos = data.produtos
            console.log(produtos)
            pegou_produtos = true
        })
    
        .catch(error => console.log(error));
}

function mostrar_produtos(produtos) {
    console.log("oi")
    console.log(produtos)
    let div_produtos_mostrar = document.getElementById("produtos2")
    produtos.forEach(produto => {
        console.log(produto)
        div_produtos_mostrar.innerHTML += `
        <div class="card" style="width: 18rem">
            <img src="{{ url_for('static', filename='img/produtos/' + ${produto.img}) }}" class="card-img-top" alt="...">
            <div class="card-body">
                <h5 class="card-title">${produto.name}</h5>
                <p class="card-text">
                    Produto
                </p>
                <a href="#" class="btn btn-primary">Adicionar no Carrinho</a>
            </div>
        </div>`
        
    });
}

document.addEventListener("DOMContentLoaded", async function() {
    await pegar_produtos();
    mostrar_produtos(produtos)
});