# Projeto Arthur Dias — Dashboard Kommo + Playbook CS

## Contexto do usuário

Trabalho como **CS (Customer Success)** na Power Mídias para o cliente **Arthur Dias Implantodontista**. Recém iniciei no cargo. Uso o Kommo CRM + playbook interno da empresa para acompanhar funil, agendamentos e direcionar a clínica.

## Stack do projeto

Pasta: `C:\Users\Pichau\source\repos\kommo`

- `dashboard.html` — interface do dashboard (HTML/JS puro)
- `server.py` — proxy Python simples que serve o HTML e faz chamadas à API Kommo (evita CORS)
- `.env` — credenciais Kommo (token, client_id, secret, domain)
- `investigate.py` — script auxiliar usado para debug/exploração da API
- `Playbook CS Power.docx` — playbook oficial da empresa

**Rodar:** `python server.py` → abrir `http://localhost:8080`

## Conta Kommo

- Domínio: `arthurdiasimplantodontista.kommo.com`
- Pipeline principal: "Funil de vendas" (ID `10858199`)
- Token de longa duração no `.env` (expira em ~dias, renovar em Configurações → Integrações)

### Etapas do funil (ID → nome)

| ID | Nome |
|---|---|
| 83266131 | Leads de entrada |
| 83266279 | Novo Lead |
| 83266283 | Cadência ligações |
| 83266287 | Follow Agendamento |
| 83266291 | Agendado |
| 83266295 | Follow Up No Show |
| 83267367 | Consulta [PT] |
| 83267371 | Controle de Exames |
| 83267375 | Follow Up Exames |
| 83267379 | Proposta Feita |
| 83267383 | Follow Up Proposta |
| 142 | Ganha |
| 143 | Perdida |

## Metas do Playbook

| Etapa | Métrica | Meta |
|---|---|---|
| Captação | CPL | < R$30 |
| Agendamento | Leads → Agendados | ≥ 33% |
| Comparecimento | Agendados → Consulta [PT] | ≥ 50% |
| Fechamento | Consulta [PT] → Ganha | ≥ 30% |
| Meta mensal | Fechamentos/mês | ≥ 7 |

## Funcionalidades atuais do dashboard

- **Filtro de período** (7/30 dias/Todos/Personalizado) — afeta funil, cards e tabela
- **Toggle "Apenas ativos"** — esconde Ganha/Perdida
- **Painel de Validação** — 4 semáforos (verde/amarelo/vermelho) com as metas do playbook + alertas automáticos
- **Cards resumo** — total, agendados, ganhos, perdidos, novos hoje, tarefas pendentes, valor total
- **Funil de Vendas** — barras por etapa
- **Agendamentos & Tarefas** — com filtro pendentes/concluídas/todas + paginação
- **Leads** — com filtro todos/agendados/novos/ganhos/perdidos + paginação (25/pág)

Removidos por performance: seção de Eventos ("Atividade Recente") e coluna de Telefone.

## Diagnóstico atual (semana 12/04–18/04)

**Entrada de leads:** OK (32 leads novos, ~4-5/dia)

**🔴 Gargalo crítico:**
- 29 de 32 leads (91%) empacaram em "Follow Agendamento"
- Taxa de agendamento: **5%** (meta: 33%)
- Zero consultas e zero fechamentos

**🔴 Situação histórica (base completa 1739 leads):**
- **948 leads** acumulados em Follow Agendamento (cemitério)
- **429** em Cadência ligações
- **215** Perdidas
- Apenas **15** Ganhas no histórico total

**Pelo playbook:** problema de execução da CRC (não marketing — volume entrando é OK).

## Roteiro de CS sugerido

### 🔴 URGENTE — Esta semana

**1. Limpar backlog de 948 leads em Follow Agendamento**
Força-tarefa de 1 semana com a CRC: retomar contato agressivo ou marcar Perdida. Meta: zerar leads parados >30 dias.

**2. Medir tempo até 1º contato**
Indicador #1 que resolve 80% dos problemas — usa eventos da API Kommo (não implementado ainda).

### 🟡 MÉDIO PRAZO — 2 semanas

**3. Relatório semanal padronizado**
Toda segunda, print do dashboard + 3 pontos: bateu meta / não bateu (diagnóstico) / ação da semana.

**4. Shadow da CRC**
Pedir acesso ao WhatsApp / ouvir ligações. Números não revelam execução.

**5. Calibrar expectativa com o dono**
Perguntar média histórica de fechamentos/mês antes da Power. Se 15 Ganhas no total, pode ser ciclo longo OU funil nunca validou.

### 🟢 LONGO PRAZO — 1º mês

**6. Enriquecer dados no Kommo**
- UTM_campaign (qual criativo gera lead)
- Motivo de perda padronizado
- Valor real (não fixo em R$14k)

**7. SalesBot para alertas automáticos**
- Lead novo sem contato em 1h
- Lead sem tarefa há >3 dias

## Rotina diária proposta (baseada no playbook)

| Horário | Ação |
|---|---|
| 08:00 | Abrir dashboard → painel validação + novos leads |
| 08:10 | 1ª mensagem do dia no grupo (script do playbook) |
| 09:00–12:00 | Roleplays CRC/Avaliador, onboarding |
| 13:00 | 2ª mensagem: verificar chamados + taxas |
| 14:00–17:00 | Roleplays + alinhamentos |
| 17:00–18:00 | 3ª mensagem: fechar dia, tarefas vencidas |

**Recorrências:**
- Sexta: verificar conteúdo e scripts
- Sábado 08-12h: diagnóstico semanal do funil
- Segunda: enviar direcionamento semanal
- Mensal (dia 3-6): reunião de resultados

## Scripts prontos do playbook (para copiar)

### Taxa de agendamento < 33% (problema CRC)
```
🚨 % de agendamento abaixo de 33%, mesmo com leads qualificados.
Consequência: meta de agendamentos, avaliações e vendas não serão realizadas.
Precisam aumentar velocidade, quantidade de contatos e qualidade do script.
Mais de 33% do agendamento está ligado ao processo e script da CRC.
@Dono/Gestor @CRC @Dentista Âncora @Avaliador
```

### Proposta de roleplay
```
Vamos marcar um roleplay com a CRC para ajustar o script de agendamento.
Qual melhor horário: [opção 1] ou [opção 2]?
```

### Poucos leads / queda
```
🚨 Baixo número de leads diários identificado.
Isso limita agendamentos, avaliações e FECHAMENTOS.
Precisamos da gravação dos vídeos enviados para subir novos anúncios.
Apenas validando 1 novo anúncio a campanha melhora a performance.
@Gestor-tráfego vai enviar mais scripts também.
@Dono/Gestor @CRC @Dentista Âncora @Avaliador
```

## Próximos passos técnicos (para retomar)

1. **Implementar "Tempo até 1º contato"** no dashboard (usa `/events` API)
2. **Cache local** — salvar leads em JSON para reduzir de ~10s para ~2s de carga
3. **Integração com Google Sheets** — comparar dados Kommo com planilha interna
4. **Alertas customizados** — ex: leads sem tarefa há >X dias
5. **Vista de "Leads parados"** — agrupados por etapa com dias parados

## Limitações conhecidas dos números

| Limitação | Impacto |
|---|---|
| Leads "Perdida" perdem histórico de etapa original | Subestima taxas reais |
| Leads recentes ainda podem avançar no funil | Taxa de fechamento artificialmente baixa em período curto |
| Sem distinção de origem (anúncio vs outros) | Playbook valida só leads de anúncio — não conseguimos filtrar |
| Valor fixo R$14.000 em quase todos os leads | Valor total não reflete vendas reais |

## Validação feita (dados confiáveis)

Comparado com Kommo em 12/04–18/04:
- ✅ Total ativos: 32 = 32
- ✅ Novo Lead: 1 = 1
- ✅ Follow Agendamento: 29 = 29
- ✅ Agendado: 2 = 2
- ✅ Valor total: R$ 448.000 = R$ 448.000

Base está 100% fiel ao Kommo.
