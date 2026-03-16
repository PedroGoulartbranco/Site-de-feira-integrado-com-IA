let pesquisa = document.getElementById("barra_pesquisa")
let botao_pesquisar = document.getElementById("botao_pesquisar")
let filtros = ['nenhum']
let atributos = ['nenhum']
let mostrar_filtros = document.getElementById("filtros")
let produtos = []

mostrar_filtros.innerHTML = filtros


botao_pesquisar.addEventListener("click", function (event) {
    event.preventDefault(); //Não recarrega a pagina
    usuario_digitou = pesquisa.value
    console.log(usuario_digitou)

    fetch('http://127.0.0.1:5000/pesquisar', {
        method: 'POST',
        headers: {

            'Content-Type': 'application/json'

        },
        body: JSON.stringify(
            { pesquisa: usuario_digitou }
        )

    })

        .then(response => response.json())

        .then(data => {
            atualizar_filtro(data.filtros, data.atributos)
            filtros = data.filtros
            atributos = data.atributos
            mostrar_produtos(produtos)
        })

        .catch(error => console.log(error));
})

function atualizar_filtro(filtros, atributos) {
    mostrar_filtros.innerHTML = `${filtros} | ${atributos}`
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
    let produtos_filtrados = []

    if (filtros.includes("nenhum")) {
        produtos.forEach(produto => {
            div_produtos_mostrar.innerHTML += `
            <div class="card" style="width: 18rem">
                <img src="static/img/produtos/${produto.img}" class="card-img-top" alt="...">
                <div class="card-body">
                    <h5 class="card-title">${produto.name}</h5>
                    <p class="card-text">
                        Produto<br>
                        Filtros: ${produto.filtros} <br>
                        Atributos: ${produto.atributos}
                    </p>
                    <a href="#" class="btn btn-primary">Adicionar no Carrinho</a>
                </div>
            </div>`
        })
    } else {
        produtos_filtrados = produtos.filter(produto => {
            produto_esta_no_filtro = produto.filtros.some(filtro => filtros.includes(filtro));
            produto_esta_no_atributos = produto.atributos.some(atributo => atributos.includes(atributo));

            return produto_esta_no_filtro && produto_esta_no_atributos
        })
        console.log(produtos_filtrados)
        produtos_filtrados.forEach(produto => {
            div_produtos_mostrar.innerHTML += `
                <div class="card" style="width: 18rem">
                    <img src="static/img/produtos/${produto.img}" class="card-img-top" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">${produto.name}</h5>
                        <p class="card-text">
                            Produto<br>
                            Filtros: ${produto.filtros} <br>
                            Atributos: ${produto.atributos}
                        </p>
                        
                        <a href="#" class="btn btn-primary">Adicionar no Carrinho</a>
                    </div>
                </div>`
        });
    }
};


document.addEventListener("DOMContentLoaded", async function () {
    await pegar_produtos();
    mostrar_produtos(produtos)
});