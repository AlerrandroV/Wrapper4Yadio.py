# Yadio API Não Oficial

Uma biblioteca Python não oficial para interagir com a API do Yadio.io, fornecendo cotações de criptomoedas, conversões, dados históricos e análises de mercado. Ela foi criada para minimizar ainda mais o uso de código para fazer as requisições. Esta biblioteca é de código aberto, livre para qualquer um usar como quiser.

---
## Glossário
- [Instalação](#instalação)
- [Começando](#começando)
- [Funcionalidades Padrão](#funcionalidades-padrão)
    - [Cotações para todas as moedas](#cotações-para-todas-as-moedas)
    - [Converter Valores](#converter-valores)
    - [Cotação Específica](#cotação-específica)
    - [Moedas Suportadas](#moedas-suportadas)
    - [Corretoras Suportadas](#corretoras-suportadas)
    - [Dados Históricos](#dados-históricos)
    - [Comparar valores de uma mesma moeda](#comparar-valores-de-uma-mesma-moeda)
    - [Anúncios de mercado](#anúncios-de-mercado)
    - [Estatísticas de mercado](#estatísticas-de-mercado)
    - [Status Ping](#status-ping)
- [Funcionalidades Extras](#funcionalidades-extras)
    - [Volatilidade](#volatilidade)
    - [Cotação às 0h](#cotação-às-0h)
    - [Variação do Dia](#variação-do-dia)
    - [Valores Extremos](#valores-extremos)
- [Boas Práticas](#boas-práticas)
- [Aviso Importante](#aviso-importante)
- [Contato](#contato-para-sugestão)
- [Doações](#doações)
- [Licença](#licença)

---
## Instalação

```bash
pip install requests pytz requests
```

---
## Começando

```python
from yadio_api import (
    exrates, convert, rate, currencies,
    today, hist, compare, ads, stats,
    ping, midnight_price, daily_price_var,
    min_price, max_price, volatility
)
```

---
## Funcionalidades Padrão

* **Obter cotações de uma moeda para todas as outras**
```python
btc_rates = exrates('BTC')
print(btc_rates)  # Exibe todas as cotações do Bitcoin
```

* **Converter valores**
```python
conversion = convert(1, 'BTC', 'USD')
print(f"1 BTC = {conversion['result']} USD")  # 1 BTC = X USD
```

* **Taxa de câmbio específica**
```python
exchange_rate = rate('BTC', 'BRL')
print(f"BTC/BRL: {exchange_rate['rate']}")  # Taxa atual Bitcoin para Real
```

* **Lista de moedas suportadas pelo Yadio**
```Python
supported_currencies = currencies()
print(f"Moedas Suportadas: {currencies}") # Mostra as moedas suportadas pela API
```

* **Lista de corretoras suportadas pelo Yadio**
```Python
supported_exchanges = exchanges()
print(f"Corretoras Suportadas: {exchanges}") # Mostra as corretoras suportadas pela API
```

* **Dados históricos**
```python
last_24h = today(24, 'BTC')  # Últimas 24 horas
historical = hist(30, 'BTC')  # Últimos 30 dias
```

* **Compare os dados de uma mesma cotação em dias diferentes**
```Python
comparison = compare(2, 'BRL')
print(f"Comparação dos últimos 2 días: {comparison}") # Mostra os dados dos 2 dias anteriores
```

* **Anúncios de compra e venda de Bitcoin**
```Python
buy_ads = ads('BRL', 'buy', 5) # Exibe 5 ofertas de compra de Bitcoin por BRL
sell_ads = ads('BRL', 'sell', 5) # Exibe 5 ofertas de compra de Bitcoin por BRL
```

* **Estatísticas de compra e venda de Bitcoin**
```Python
buy_stats = stats('BRL', 'buy') # Exibe estatísticas de compra de Bitcoin por BRL
sell_stats = stats('BRL', 'sell') # Exibe estatísticas de compra de Bitcoin por BRL
```

* **Ping**
```Python
status_api = ping()
print(f"Status: {status_api}")
```

---
## Funcionalidades Extras

* **Volatilidade**
```python
vol = volatility(24, 'BRL', 'America/Sao_Paulo')
print(f"Variação: {vol * 100:.2f}%")  # Volatilidade nas últimas 24h
```

* **Preço na meia-noite**
```python
opening_price = midnight_price('BRL', 'America/Sao_Paulo') # O fuso-horário é opcional
print(f"Preço de abertura: {opening_price}")
```

* **Variação em relação à meia noite**
```Python
variation = daily_price_var('BRL', 'America/Sao_Paulo')
print(f"Variação: {variation * 100:.2f}%") # Variação do dia em porcentagem
```

- **Valores extremos**
```Python
min_price = min_price(5, 'BRL') # Cotação mais baixa em BRL das últimas 5 horas
max_price = max_price(5, 'BRL') # Cotação mais alta em BRL das últimas 5 horas
print(f"Menor Contação: R${min_price['price']}")
print(f"Maior Contação: R${max_price['price']}")
```

---
## Boas Práticas

1. **Tratamento de Erros**
```python
if response := convert(100, 'USD', 'BTC'):
    # Processar resposta
else:
    # Tratar erro
```

2. **Limites de Requisição**
- Respeite os limites da API (evite chamadas excessivas)
- Considere implementar cache local para dados estáticos

3. **Tipos de Moeda**
- Sempre use códigos oficial (ISO 4217 para fiat)
- Valide moedas com `currencies()` antes de usar

4. **Fuso Horário**
- Especifique timezone quando necessário:
```python
midnight_price('BRL', 'America/Sao_Paulo')
```

5. **Validação de Entrada**
```python
try:
    rate = convert('um', 'BTC', 'USD')  # Erro!
except ValueError as e:
    print(e)
```

---
## Avisos Importantes

- Não afiliado ao Yadio.io
- Dados são atualizados a cada 5 minutos
- Sempre verifique a documentação oficial para alterações na API

---
## Contato para Sugestão
**Email**: v.alerrandro.t@hotmail.com

---
## Doações
O projeto é livre para todos de forma gratuita, mas se for usar a biblioteca para fins lucrativos, considere uma doação. Serei muito grato ;)

* **🔗 OnChain**: `bc1q7relhks9wvzzlky2vwfm4t8f8vhn05jx4uhgs6`
* **⚡ Lightning**: `alerrandrov@blink.sv`
* **❖ PIX**: `v.alerrandro.t@hotmail.com`

---
## Licença

Faça o que sua criatividade mandar!

> Bitcoin é liberdade!

**Nota:** Este projeto não tem qualquer afiliação com o Yadio.io. A API pública do Yadio é utilizada conforme disponibilidade documentada publicamente.
