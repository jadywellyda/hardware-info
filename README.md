# 🖥️ PC Info

Script simples em Python que exibe informações do seu computador (sistema operacional, CPU, memória RAM, discos e rede).

## 📋 O que ele mostra

- Sistema operacional, hostname, processador e usuário
- CPU: núcleos físicos/lógicos, uso atual e frequência
- Memória RAM: total, disponível, uso percentual e swap
- Discos: dispositivo, ponto de montagem, sistema de arquivos, uso livre/total
- Rede: hostname, IP local e interfaces

## 🚀 Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/pc-info.git
cd pc-info
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o script

**Modo interativo (exibe no terminal):**

```bash
python pc_info.py
```

**Salvar em arquivo de texto:**

```bash
python pc_info.py --salvar-txt relatorio.txt
```

**Salvar em JSON:**

```bash
python pc_info.py --salvar-json info.json
```

**Salvar em ambos sem exibir no terminal:**

```bash
python pc_info.py --salvar-txt relatorio.txt --salvar-json info.json --apenas-saida
```

**Ajuda:**

```bash
python pc_info.py --help
```

Saída esperada (modo interativo):

```
==================================================
 Sistema
==================================================
  Sistema: Windows
  Nome do nó (hostname): DESKTOP-ABC
  Versão: 10.0.19045
  Máquina: AMD64
  Processador: Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
  Usuário: fulano
  Data/Hora: 24/11/2026 10:30:00
...
```

## 📦 Requisitos

- Python 3.8 ou superior
- [psutil](https://pypi.org/project/psutil/) (instalado via `requirements.txt`)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuição

Pull requests são bem-vindos! Para mudanças maiores, abra uma issue primeiro para discutir o que você gostaria de alterar.

---

Feito com ❤️ para quem quer aprender sobre o próprio PC.
