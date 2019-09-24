# Guia de contribuição

## Guia de estilo

Todo código python deve serguir o guia de estilo oficial do PythonBrasil, [GuiaDeEstilo](https://wiki.python.org.br/GuiaDeEstilo)


## Política de commits 

A descrição dos commits deve ser especificada em inglês e ser curta e objetiva, representando qual o objetivo do commit. A mensagem deve estar acompanhada do número da issue relacionada, como no exemplo abaixo:
```
git commit -m'#X my message'
```
Onde X representa o número da issue relacionada.

## Política de Branches

### Branch master
A branch master é a branch estável do projeto, onde estará o código de produção. Commits e pushes para essa branch estarão bloqueados. Somente serão aceitos pull requests para essa branch oriundos da branch devel.

### Branch devel
A branch devel será a branch de desenvolvimento, na qual será unificado novas funcionalidades e correções no código visando gerar uma nova versão estável. As branchs de desenvolvimento das funcionalidades deverão ser criadas sempre a partir da branch devel. Uma vez que as funcionalidades estejam concluídas deve ser aberto o Pull Request para a branch devel.

## Nomenclatura de Branches
Sempre que uma equipe de desenvolvimento for começar a trabalhar em algum Caso de Uso ou História de Usuário, deve-se criar a branch a partir da branch devel, com o padrão definido abaixo:

### GERAL
Os nomes das branchs devem ser criados em inglês e devem ser curtos e claros.

### PARA FEATURES
Nome da branch prefixada com feature acompanhado com a issue relacionada:
```
feature/x-branch_name
```

### PARA REFATORAÇÃO DE CÓDIGO
Branchs com o objetivo de realizar alterações em funcionalidades já implementadas devem ser prefixadas com refactor acompanhado com a issue:
```
refactor/x-branch_name
```

### PARA CORREÇÃO DE CÓDIGO
Branchs com o objetivo de consertar algum problema técnico relacionado a uma ou algumas funcionalidades devem ser prefixadas com bugfix acompanhado com a issue relacionda:
```
bugfix/x-branch_name
```

### PARA PROBLEMAS CRÍTICOS EM PRODUÇÃO
Branchs com o objetico de corrigir alguma falha grave relacionadas a funcionalidades que já estão em produção devem ser prefixadas com hotfix acompanhado com a issue relacionada:
```
hotfix/x-branch_name
```

### PARA LANÇAMENTO DE VERSÃO
Branchs com o objetivo de realizar o lançamento da versão do código para produção
```
release/stable-x.x
```

Onde x.x é o número da versão

## Política de Issues
As issues devem possuir um nome simples, em portugês e que descreva claramente os principais objetivos
A descrição deve ser o mais detalhada possível, para melhor acompanhamento e entendimento de todo o processo e objetivos da issue.
As issues devem ser identificadas com as labels referentes. Ajuda o nosso trabalho na hora de mapear quais são as demandas de cada área do projeto.

### Para novas funcionalidades
As issues devem ser acompanhadas de uma lista de critérios de aceitação que garantem que o ao implementar o objetivo será atendido, tanto em termos de funcionalidade, usabilidade, design e qualidade de código;
```
US - Nome da Issue
```
### Para histórias técnicas
```
TS - Nome da Issue
```

## Políticas de Pull Requests
Pull Requests originados de branchs classificadas como feature, documentation e bugfix devem ser abertos para a branch devel.
Pull Requests em progresso
Pull Requests que ainda não estão prontos para serem aceitos devem conter a sinalização WIP - Work in Progress logo no início do nome. Exemplo:


WIP: my pull request

Condições para aprovação do Pull Request
Para que o pull request seja aceito na branch devel, deve seguir as seguintes condições:

Funcionalidade, correção ou refatoração completa;
Build de integração aceito;
Manter a cobertura do código há uma porcentagem definida;
Estar de acordo com as métricas de qualidade de código descritas no plano de qualidade da issue.
