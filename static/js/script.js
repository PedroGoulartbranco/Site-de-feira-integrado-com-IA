let pesquisa = document.getElementById("barra_pesquisa")
let botao_pesquisar = document.getElementById("botao_pesquisar")
let filtros = ['nenhum']
let mostrar_filtros = document.getElementById("filtros")
let produtos = []

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
        filtros = data.filtros
        mostrar_produtos(produtos)
    })

    .catch(error => console.log(error));
})

function atualizar_filtro(filtros) {
    mostrar_filtros.innerHTML= filtros
}

async function pegar_produtos() {
    await fetch('http://127.0.0.1:5000/pegar_produtos')
    
        .then(response => response.json())
    
        .then(data => {
            produtos = data.produtos
        })
    
        .catch(error => console.log(error));
}

function mostrar_produtos(produtos) {
    let div_produtos_mostrar = document.getElementById("produtos")
    div_produtos_mostrar.innerHTML = ``
    let filtro_ativado = false
    let produtos_filtrados = []

    if (filtros.includes("nenhum")) {
        produtos.forEach(produto => {
            div_produtos_mostrar.innerHTML += `
            <div class="card" style="width: 18rem">
                <img src="static/img/produtos/${produto.img}" class="card-img-top" alt="...">
                <div class="card-body">
                    <h5 class="card-title">${produto.name}</h5>
                    <p class="card-text">
                        Produto
                    </p>
                    <a href="#" class="btn btn-primary">Adicionar no Carrinho</a>
                </div>
            </div>`
    }) } else {
        produtos_filtrados = produtos.filter(produto => {
                return produto.filtros.some(filtro => filtros.includes(filtro))
            })
            produtos_filtrados.forEach(produto => {
                div_produtos_mostrar.innerHTML += `
                <div class="card" style="width: 18rem">
                    <img src="static/img/produtos/${produto.img}" class="card-img-top" alt="...">
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
    };


document.addEventListener("DOMContentLoaded", async function() {
    await pegar_produtos();
    mostrar_produtos(produtos)
});