let produtos_no_carrinho = []
let barra_lateral_adicionar_produto = document.getElementById("barra_lateral_adicionar_produto")
let overlay = document.getElementById("overlay")
let produto_atual = []

function adicionar_no_carrinho(id_produto) {
    produtos.forEach(produto => {
        if (produto.id == id_produto) {
            produto_atual = produto;
        }
    })
    barra_lateral_adicionar_produto.innerHTML = `
    <h2>Adicionar Produto</h2>
    <p>${produto_atual.name}</p>
    <img src="static/img/produtos/${produto_atual.img}" class="imagem" alt="${produto_atual.name}"  object-fit: contain;">
    <p>Preço: R$${produto_atual.price}</p>
    <p>${produto_atual.descricao_Front}</p>
    `

    barra_lateral_adicionar_produto.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}

function fechar_barras_laterais() {
    console.log("fechou")
    barra_lateral_adicionar_produto.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}