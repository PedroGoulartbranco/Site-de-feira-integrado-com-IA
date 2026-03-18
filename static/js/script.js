let pesquisa = document.getElementById("barra_pesquisa");
let botao_pesquisar = document.getElementById("botao_pesquisar");
let filtros = ["nenhum"];
let atributos = ["nenhum"];
let mostrar_filtros = document.getElementById("filtros");
let produtos = [];
let nomes = ["nenhum"];
let div_mostrar_filtros = document.getElementById("mostrar_filtros");
let div_mostrar_atualizando_produtos = document.getElementById("carregamento")
let div_de_produtos_tela = document.getElementById("produtos")

mostrar_filtros.innerHTML = filtros; //Limpa os filtros

botao_pesquisar.addEventListener("click", function (event) {
  event.preventDefault(); //Não recarrega a pagina
  usuario_digitou = pesquisa.value;
  console.log(usuario_digitou);

  if (usuario_digitou.trim() != "") {
    div_mostrar_atualizando_produtos.style.display = "flex"
    div_de_produtos_tela.innerHTML = ""
    fetch("/pesquisar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ pesquisa: usuario_digitou }),
  })
    .then((response) => response.json())

    .then((data) => {
      atualizar_filtro(data.filtros, data.atributos, data.nomes);
      filtros = data.filtros;
      atributos = data.atributos;
      nomes = data.nomes;
      console.log(nomes);
      mostrar_produtos(produtos);
    })

    .catch((error) => console.log(error));
  } else {
    pesquisa.style.placeholder = "Filtro Inteligente"
  }

});

function atualizar_filtro(filtros, atributos, nomes) {
  div_mostrar_filtros.innerHTML = ``;
  filtros.forEach((filtro) => {
    div_mostrar_filtros.innerHTML += `
            <button type="button" class="botao-filtro" onclick="remover('${filtro}')">${filtro}</button>
        `;
  });
  atributos.forEach((atributo) => {
    div_mostrar_filtros.innerHTML += `
            <button type="button" class="botao-filtro"" onclick="remover('${atributo}')">${atributo}</button>
    `;
  });
  nomes.forEach((nome) => {
    div_mostrar_filtros.innerHTML += `
            <button type="button" class="botao-filtro"" onclick="remover('${nome}')">${nome}</button>
    `;
  });
}

async function pegar_produtos() {

  await fetch("/pegar_produtos")
    .then((response) => response.json())

    .then((data) => {
      produtos = data.produtos;
    })

    .catch((error) => console.log(error));
}

function mostrar_produtos(produtos) {
  let div_produtos_mostrar = document.getElementById("produtos");
  div_produtos_mostrar.innerHTML = ``;
  let produtos_filtrados = [];
  let produto_esta_no_atributos = false;
  let produto_esta_no_filtro = false;
  let produto_esta_no_nome = false;

  if (!nomes.includes("nenhum")) {
    produtos_filtrados = produtos.filter((produto) => {
      produto_esta_no_nome = nomes.some(nome => {
        return produto.name.toUpperCase() === nome.toUpperCase();
      }
    );
    return produto_esta_no_nome;
    });
  } else if (filtros.includes("nenhum")) {
    if (atributos.includes("nenhum")) {
      produtos.forEach((produto) => {
        produtos_filtrados.push(produto);
      });
    } else {
      produtos_filtrados = produtos.filter((produto) => {
        produto_esta_no_atributos = produto.atributos.some((atributo) =>
          atributos.includes(atributo),
        );
        return produto_esta_no_atributos;
      });
    }
  } else {
    if (atributos.includes("nenhum")) {
      produtos_filtrados = produtos.filter((produto) => {
        produto_esta_no_filtro = produto.filtros.some((filtro) =>
          filtros.includes(filtro),
        );

        return produto_esta_no_filtro;
      });
    } else {
      produtos_filtrados = produtos.filter((produto) => {
        produto_esta_no_filtro = produto.filtros.some((filtro) =>
          filtros.includes(filtro),
        );
        produto_esta_no_atributos = produto.atributos.some((atributo) =>
          atributos.includes(atributo),
        );

        return produto_esta_no_filtro && produto_esta_no_atributos;
      });
    }
  }
  div_mostrar_atualizando_produtos.style.display = "none"
  produtos_filtrados.forEach((produto) => {
      div_produtos_mostrar.innerHTML += `
      <div class="col-12 col-md-6 col-lg-4 col-xl-3 d-flex justify-content-center p-2">
        <div class="card h-100 w-100 shadow-sm"> 
            <img src="static/img/produtos/${produto.img}" class="card-img-top p-3" alt="${produto.name}" style="height: 200px; object-fit: contain;">
            
            <div class="card-body d-flex flex-column">
                <h5 class="card-title h6 fw-bold" style="min-height: 2.5rem;">${produto.name}</h5>
                <p class="card-text small text-muted mb-2">
                    Filtros: ${produto.filtros}<br>
                    Atributos: ${produto.atributos}
                </p>
                <div class="mt-auto">
                    <p class="fw-bold fs-5 mb-2">
                        R$ ${produto.price}
                    </p>
                    <a href="#" class="btn btn-primary w-100" onclick="abrir_barra_adicionar_produto('${produto.id}')">Adicionar no Carrinho</a>
                </div>
            </div>
        </div>
    </div>`;
    });
}

function remover(nome) {
  if (nome != "nenhum") {
    if (filtros.includes(nome)) {
      console.log("chamou filtro");
      filtros = filtros.filter((filtro) => filtro != nome);
    }
    if (atributos.includes(nome)) {
      atributos = atributos.filter((atributo) => atributo != nome);
    }
    if (nomes.includes(nome)) {
      nomes = ["nenhum"]
    }
    if (filtros.length == 0) {
      filtros = ["nenhum"]
    } 
    if (atributos.length == 0) {
      atributos = ["nenhum"]
    }
    atualizar_pagina();
  }
}

async function atualizar_pagina() {
  atualizar_filtro(filtros, atributos, nomes);
  await pegar_produtos();
  mostrar_produtos(produtos);
}

//Chama essas duas funções toda vez que a pagina é reiniciada
document.addEventListener("DOMContentLoaded", async function () {
  atualizar_pagina();
});
