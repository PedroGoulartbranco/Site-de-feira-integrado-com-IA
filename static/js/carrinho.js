let produtos_no_carrinho = []
let barra_lateral_adicionar_produto = document.getElementById("barra_lateral_adicionar_produto")
let overlay = document.getElementById("overlay")

function adicionar_no_carrinho(id_produto) {
    barra_lateral_adicionar_produto.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}

function fechar_barras_laterais() {
    console.log("fechou")
    barra_lateral_adicionar_produto.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}