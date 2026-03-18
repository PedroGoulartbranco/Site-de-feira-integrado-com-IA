let produtos_no_carrinho = []
let barra_lateral = document.getElementById("barra_lateral")
let overlay = document.getElementById("overlay")
let produto_atual = []
let quantidade = 1;
let lista_nomes_dos_produtos_carrinho = []
let total_a_pagar_carrinho = 0

function abrir_barra_adicionar_produto(id_produto) {
    produtos.forEach(produto => {
        if (produto.id == id_produto) {
            produto_atual = produto;
        }
    })
    quantidade = 1;
    barra_lateral.innerHTML = `
    <h2>Adicionar Produto</h2>
    <p>${produto_atual.name}</p>
    <img src="static/img/produtos/${produto_atual.img}" class="imagem" alt="${produto_atual.name}" style="object-fit: contain; width: 100%; height: 200px;">
    <p>Preço: R$${produto_atual.price}</p>
    <p>${produto_atual.descricao_Front}</p>
    
    <p>Quantidade no Carrinho: ${contar_quantidade_no_carrinho(produto_atual.name)}</p>
    <div class="d-flex align-items-center justify-content-center mb-3">
        <button type="button" class="botao_quantidade" onclick="aumentar_diminuir_quantidade('-', '${produto_atual.name}')">-</button>
        <h3 id="onde_mostra_quantidade" class="mb-0">${quantidade}</h3>
        <button type="button" class="botao_quantidade" onclick="aumentar_diminuir_quantidade('+', '${produto_atual.name}')">+</button>
    </div>

    <a href="#" class="btn btn-primary w-100" onclick="adicionar_carrinho('${produto_atual.name}')">Finalizar</a>
`;

    barra_lateral.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}

function aumentar_diminuir_quantidade(sinal, nome_produto) {
    let indice = produtos_no_carrinho.findIndex(pedido => pedido.nome == nome_produto)
    if (sinal == "+") {
        quantidade += 1
    } else {
        if (indice == -1) {
            if (quantidade > 0) {
                quantidade -= 1
            }
        } else {
            if (quantidade + produtos_no_carrinho[indice].quantidade > 0) {
                quantidade -= 1
            }
        }
    }
    h3_mostrar_quantidade = document.getElementById("onde_mostra_quantidade")
    h3_mostrar_quantidade.innerHTML = quantidade
}

function adicionar_carrinho(nome_produto) {
    produtos.forEach(produto => {
        if (produto.name == nome_produto) {
            produto_atual = produto;
        }
    })
    if (produtos_no_carrinho.length == 0 || !lista_nomes_dos_produtos_carrinho.includes(nome_produto)) {
        produtos_no_carrinho.push({
            "nome": nome_produto,
            "quantidade": quantidade,
            "preco": produto_atual.price,
            "preco_total": quantidade * parseFloat(produto_atual.price)
        })
        lista_nomes_dos_produtos_carrinho.push(nome_produto)
    } else {
        let indice = produtos_no_carrinho.findIndex(pedido => pedido.nome == nome_produto)
        quantidade = produtos_no_carrinho[indice].quantidade + (quantidade)
        produtos_no_carrinho[indice] = {
            "nome": nome_produto,
            "quantidade": quantidade,
            "preco": produto_atual.price,
            "preco_total": quantidade * parseFloat(produto_atual.price)
        }
    }

    fechar_barras_laterais()
}

function contar_quantidade_no_carrinho(nome_produto) {
    let indice = produtos_no_carrinho.findIndex(pedido => pedido.nome == nome_produto)
    if (indice == -1) {
        return 0;
    } else {
        return produtos_no_carrinho[indice].quantidade
    }
}

function diminuir_quantida_no_carrinho(nome_produto) {
    let indice = produtos_no_carrinho.findIndex(pedido => pedido.nome == nome_produto)
    if (produtos_no_carrinho[indice].quantidade > 0) {
        produtos_no_carrinho[indice].quantidade -= 1
        if (produtos_no_carrinho[indice].quantidade <= 0) {
            console.log("apagar")
            produtos_no_carrinho.splice(indice, 1)
            ver_carrinho(true)
            return
        }
        ver_carrinho(true)
    }
}

function calcular_preco_total_carrinho() {
    let preco_total_final = 0
    produtos_no_carrinho.forEach(produto => {
        preco_total_final += parseFloat(produto.preco_total)
    })
    total_a_pagar_carrinho = preco_total_final
}

function ver_carrinho(atualizar = false) {
    if (!atualizar) {
        barra_lateral.classList.toggle("ativa")
        overlay.classList.toggle("ativa")
    }
    let total_venda = 0
    barra_lateral.innerHTML = `
        <h2>Carrinho</h2>
        <h5> Produtos: </h5>
    `
    if (produtos_no_carrinho.length == 0) {
        barra_lateral.innerHTML += `
        <p> Nenhum Produto Adicionado</p>
        `
    } else {
        let texto_para_zap = ``
        produtos_no_carrinho.forEach(produto => {
            let preco_total_produto = parseFloat(produto.preco) * parseInt(produto.quantidade)
            total_venda += preco_total_produto
            barra_lateral.innerHTML += `
            <p>Nome: ${produto.nome}<br>
            Quantidade: ${produto.quantidade}<button type="button" class="botao_quantidade" onclick="diminuir_quantida_no_carrinho('${produto.nome}')">-</button><br>
            Preço Unitário: ${produto.preco}<br>
            Preço Total: R$${preco_total_produto}</p>
            <hr>
            `
            texto_para_zap += `%0ANome: ${produto.nome}%0AQuantidade: ${produto.quantidade}%0APreço Unitário: ${produto.preco}%0APreço Total: R$${preco_total_produto}`
        })
        texto_para_zap += `%0AValor Total: R$${total_venda.toFixed(4)}`
        barra_lateral.innerHTML += `
        <h5>Valor Total: R$<span id="mostrar_valor_total">${total_venda.toFixed(4)}</span></h5>
         <a href="https://wa.me/?text=${texto_para_zap}"" target="_blank"class="btn btn-success w-100">Mandar Para Whatsapp</a>
        `
    }
}

function fechar_barras_laterais() {
    console.log("fechou")
    barra_lateral.classList.toggle("ativa")
    overlay.classList.toggle("ativa")
}