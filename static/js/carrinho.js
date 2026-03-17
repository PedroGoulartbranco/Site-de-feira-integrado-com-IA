let produtos_no_carrinho = []
let barra_lateral_adicionar_produto = document.getElementById("barra_lateral_adicionar_produto")
let overlay = document.getElementById("overlay")
let produto_atual = []
let quantidade = 1;

function abrir_barra_adicionar_produto(id_produto) {
    quantidade = 1;
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
    <p>No Carrinho: </p>
    <span>
        <button type="button" class="btn btn-secondary" onclick="aumentar_diminuir_quantidade('+')">+</button>
        <h3 id="onde_mostra_quantidade">${quantidade}</h3>
        <button type="button" class="btn btn-secondary" onclick="aumentar_diminuir_quantidade('-')">-</button>
    </span>
    `

    barra_lateral_adicionar_produto.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}

function aumentar_diminuir_quantidade(sinal) {
    if (sinal == "+") {
        quantidade += 1
    } else {
        if (quantidade > 0) {
            quantidade -= 1
        }
    }
    h3_mostrar_quantidade = document.getElementById("onde_mostra_quantidade")
    h3_mostrar_quantidade.innerHTML = quantidade
}

function adicionar_carrinho(produto, quantidade) {
    produtos_no_carrinho.push({
        "nome": produto.name,
        "quantidade": quantidade
    })
}

function contar_quantidade_no_carrinho(id_produto) {
    let total = 0;
    
}

function fechar_barras_laterais() {
    console.log("fechou")
    barra_lateral_adicionar_produto.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}