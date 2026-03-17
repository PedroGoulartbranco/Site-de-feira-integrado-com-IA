let produtos_no_carrinho = []
let barra_lateral_adicionar_produto = document.getElementById("barra_lateral_adicionar_produto")

function adicionar_no_carrinho(id_produto) {
    barra_lateral_adicionar_produto.classList.toggle("ativa")
}