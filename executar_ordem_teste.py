import MetaTrader5 as mt5
import sys

# 1. Inicializa conexão
if not mt5.initialize():
    print(f"ERRO: Falha ao inicializar MT5: {mt5.last_error()}")
    sys.exit(1)

# 2. Verifica conexão
info = mt5.account_info()
if info is None:
    print("ERRO: Sem conta logada. Faça login no MT5.")
    mt5.shutdown()
    sys.exit(1)

print(f"Conectado: Conta {info.login} | Saldo: {info.balance} {info.currency}")

# 3. Escolhe o símbolo (XAUUSD-ECN é o que funciona)
symbol = "XAUUSD-ECN"
if not mt5.symbol_select(symbol, True):
    print(f"ERRO: Símbolo {symbol} não disponível")
    mt5.shutdown()
    sys.exit(1)

# 4. Pega preço atual
tick = mt5.symbol_info_tick(symbol)
if tick is None:
    print(f"ERRO: Sem cotação para {symbol}")
    mt5.shutdown()
    sys.exit(1)

print(f"Preço atual {symbol}: Bid={tick.bid} | Ask={tick.ask}")

# 5. Monta ordem BUY 0.01 (volume mínimo para teste)
volume = 0.01
price = tick.ask
sl = round(price - 10.0, 2)   # Stop Loss 10 pontos abaixo
tp = round(price + 20.0, 2)   # Take Profit 20 pontos acima

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": volume,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": sl,
    "tp": tp,
    "deviation": 20,
    "magic": 20261109,
    "comment": "teste_claude",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

print(f"Enviando ordem: BUY {volume} {symbol} @ {price} | SL={sl} | TP={tp}")

# 6. Envia ordem
result = mt5.order_send(request)

if result is None:
    print(f"ERRO: order_send retornou None: {mt5.last_error()}")
elif result.retcode != mt5.TRADE_RETCODE_DONE:
    print(f"ERRO: Ordem rejeitada. Retcode={result.retcode} | {result.comment}")
    print(f"Request enviado: {request}")
else:
    print(f"✅ ORDEM EXECUTADA COM SUCESSO!")
    print(f"   Ticket: {result.order}")
    print(f"   Preço: {result.price}")
    print(f"   Volume: {result.volume}")

mt5.shutdown()