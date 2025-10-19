# Projeto Análise de Vulnerabilidades Metasploitable 2 com Kali Linux (Pentest)

## Qual é o objetivo do repositório?

Este repositório documenta **passo a passo** a montagem de um laboratório de Pentest/testes de invasão realizados contra a VM vulnerável **Metasploitable2**, utilizando o **Kali Linux** como máquina atacante.

- Escopo: configuração de duas VMs no VirtualBox em rede host-only, reconhecimento de serviços, ataques de força bruta e password spraying, validação de acessos, e recomendações de mitigação.
- Resultados esperados: demonstração reprodutível dos passos, comandos, wordlists utilizadas e análise de riscos e correções aplicáveis.

## Ambiente e Topologia
- Hypervisor: Oracle VirtualBox.
- VM Atacante: Kali Linux (última versão estável disponível no laboratório).
- VM Alvo: Metasploitable2.
- Rede: Host-only / Internal Network para isolamento do laboratório.
- Endereços:
- Kali: 192.168.56.101;
- Metasploitable2: 192.168.56.102.
  
## O que é Metasploitable 2?

Metasploitable 2 é uma máquina virtual vulnerável, mantida pela Rapid7, projetada para fins educacionais em segurança ofensiva.  
**Atenção:** nunca exponha esta VM à internet, use apenas em ambientes isolados.

Como usar este repositório
1. Instale o VirtualBox.  
2. Baixe as imagens do [Kali Linux](https://www.kali.org/get-kali/#kali-platforms) e [Metasploitable2](https://www.rapid7.com/products/metasploit/metasploitable/).  
3. Configure a rede host-only.  
4. Siga os tutoriais de reconhecimento, exploração e mitigação.

## Conteúdo
- Reconhecimento de serviços (`nmap`)  
- Ataques de força bruta (`hydra`)  
- Password spraying  
- Validação de acessos

---
  
**ATENÇÃO: Este projeto é apenas para fins educacionais do Santander CyberSec Bootcamp.**

## Configuração do Ambiente

### Kali Linux

<img width="1189" height="619" alt="image" src="https://github.com/user-attachments/assets/a3d012da-a743-4ae0-a3d8-b4bd7d5679b4" />


### Metasploitable 2

<img width="1185" height="691" alt="image" src="https://github.com/user-attachments/assets/304d86d8-f664-4edf-8c55-66a2bdf68d3f" />


## Reconhecimento das portas com Nmap

Para reconhecimento padrão vamos executar o comando `nmap` [endereço ip do metaspliotable2]. 

Exemplo: 

```bash
nmap 192.168.56.102
```

<img width="762" height="583" alt="image" src="https://github.com/user-attachments/assets/89c0c365-2b8f-4040-b4ea-7f4c3489d7d2" />


Vamos focar nas portas 21, 22, 80, 445 e 139 com o comando:

```bash
nmap -sV -p 21,22,80,445,139 192.168.56.102
```

<img width="751" height="687" alt="image" src="https://github.com/user-attachments/assets/c822f90e-314c-4386-9638-23e1e667ce36" />


## Ataque de força bruta no serviço ftp

Pode-se identificar a porta 21 (FTP), onde a mesma é utilizada para tranferência de arquivos. Nesse protocolo é possível realizar o download ou upload de arquivos do computador.

### Reconhecimento da porta utilizando o Nmap

<img width="751" height="687" alt="image" src="https://github.com/user-attachments/assets/cebbd601-62d1-48ac-8a5e-e22ed1c4a6d5" />


### Criação das wordlists

Nesta etapa criamos duas wordlists. Uma lista com os nome de usuários e outra com as possíveis senhas. Segue abaixo os comandos para a criação das listas:

Criação da lista de usuários:
```bash
echo -e "user\nmsfadmin\nadmin\nroot" > users.txt
```

Criação da lista de senhas:
```bash
echo -e "123456\npassword\nqwerty\nmsfadmin" > pass.txt
```

### Medusa: Ataque de brute force utilizando as wordlists criadas

Nesta etapa vamos utilizar a ferramenta `Medusa` para realizar um ataque de força bruta utilizando as listas na porta 21 do serviço `ftp`. Segue o comando abaixo:

```bash
medusa -h 192.168.56.4 -U users.txt -P pass.txt -M ftp -t 6
```
<img width="692" height="908" alt="image" src="https://github.com/user-attachments/assets/ae8d012c-2512-4e1f-8985-dedefe096ca4" />

## Ataque em formulários em aplicações web (DVWA)

Os ataques de força bruta também podem ser testados em aplicações web que possuem formulários de login. Com isso, um atacante que possuir uma lista de usuários e lista de senhas vazadas conseguem utilizar ferramentas para estabelecer o acesso com tentativas e erros.

### Reconhecimento do comportamento do formulário

Para identificar a requisição do formulário é necessário utilizar a ferramenta do navegador chamado de `DevTools`´, geralmente podemos abrir com a tecla `F12` do teclado. Dessa forma, é possível visualizar quais são os campos usados na requisição, e precisamos deles para utilizar na ferramenta de força bruta. Segue abaixo o reconhecimento.

**Identificação dos campos da requisição**

<img width="1357" height="561" alt="Captura de tela 2025-10-14 131331" src="https://github.com/user-attachments/assets/fc441b4e-caf7-4b7b-a095-11012200ed76" />

Na imagem, podemos ver na aba `Request/Requisição` os campos necessárois no formulário para realizar o login, sendo eles: username, password e Login.

### Criação das wordlists

Criação da lista de usuários:
```bash
echo -e "user\nmsfadmin\nadmin\nroot" > users.txt
```

Criação da lista de senhas:
```bash
echo -e "123456\npassword\nqwerty\nmsfadmin" > pass.txt
```

### Ataque de força bruta no formulário de Login

Nesta etapa utilizaremos o `Medusa` para atacar a aplicação web utilizando as wordlists criadas. Para esse ataque é usado os campos do reconhecimento do formulário com a ajuda do `DevTools`. Com todas essa informações podemos seguir para o comando:

```bash
medusa -h 192.168.56.102 -U users.txt -P pass.txt -M http \
-m PAGE:'/dvwa/login.php' \
-m FORM:'username=^USER^&password=^PASS^&Login=Login' \
-m 'FAIL=Login failed' -t 6
```

---

<img width="1447" height="422" alt="image" src="https://github.com/user-attachments/assets/dc1db95c-6de0-4744-bad8-07250d8162ae" />


---

**Utilizando a ferramenta Hydra**

Essa é outra ferramenta poderosa de brute force, com ela podemos utilizar as flags passando as wordlists e o formulário da aplicação. Veja abaixo o comando e o resultado com o hydra.

Comando:
```bash
hydra -L users.txt -P pass.txt 192.168.56.102 http-post-form "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed" -V
```

<img width="1743" height="475" alt="image" src="https://github.com/user-attachments/assets/5a914b22-2ce0-4960-a1fc-03ddbaf62ebe" />


---

O usuário e senha encontrados foram, admin e password.

