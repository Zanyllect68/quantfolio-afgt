import MetaTrader5 as mt5
import pandas as pd

# Constantes para credenciales (mejor práctica: usar variables de entorno o config)
PATH = r'C:\Program Files\RoboForex MT5 Terminal\terminal64.exe'
LOGIN = 67106046
PASSWORD = 'Sebas.123'
SERVER = 'RoboForex-ECN'

# Inicializar MT5 con verificación
if not mt5.initialize(login=LOGIN, password=PASSWORD, server=SERVER, path=PATH):
    print("Error al inicializar MT5:", mt5.last_error())


orden_compra = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": "XAUUSD",
    "type": mt5.ORDER_TYPE_BUY,
    "volume": 0.01,
    "type_filling": mt5.ORDER_FILLING_FOK,
    "comment": "AFGT"
}

# Verificar resultado de order_send
result_compra = mt5.order_send(orden_compra)
if result_compra.retcode != mt5.TRADE_RETCODE_DONE:
    print("Error en orden de compra:", result_compra.comment)
else:
    print("Orden de compra enviada exitosamente")

orden_venta = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": "XAUUSD",
    "type": mt5.ORDER_TYPE_SELL,
    "volume": 0.01,
    "type_filling": mt5.ORDER_FILLING_FOK,
    "comment": "AFGT"
}
result_venta = mt5.order_send(orden_venta)
if result_venta.retcode != mt5.TRADE_RETCODE_DONE:
    print("Error en orden de venta:", result_venta.comment)
else:
    print("Orden de venta enviada exitosamente")

# Comentado para evitar envíos accidentales; descomentar solo para pruebas
for i in range(5):
     result = mt5.order_send(orden_venta)
     if result.retcode != mt5.TRADE_RETCODE_DONE:
         print(f"Error en venta {i+1}:", result.comment)

list_of_symb = ['XAUUSD','EURUSD','USDJPY']

for symbol in list_of_symb:
    orden_compra = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "type": mt5.ORDER_TYPE_BUY,
        "volume": 0.01,
        "type_filling": mt5.ORDER_FILLING_FOK,
        "comment": "AFGT"
    }
    result = mt5.order_send(orden_compra)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Error en compra para {symbol}:", result.comment)
    else:
        print(f"Orden de compra para {symbol} enviada exitosamente")


operaciones_abiertas = mt5.positions_get()
if operaciones_abiertas is None:
    print("No se pudieron obtener las posiciones abiertas:", mt5.last_error())
else:
    print(f"Total de posiciones abiertas: {len(operaciones_abiertas)}")
    for pos in operaciones_abiertas:
        print(pos)

df_positions = pd.DataFrame(list(operaciones_abiertas), columns = operaciones_abiertas[0]._asdict().keys())

print(df_positions)




lista_tickets = df_positions[df_positions['comment'] == "AFGT"]["ticket"].tolist()
print("Lista de tickets de posiciones abiertas:", lista_tickets)
for ticket in lista_tickets:
    pos = df_positions[df_positions['ticket'] == ticket].iloc[0]
    # Determinar tipo de orden de cierre basado en el tipo de posición (0=buy, 1=sell)
    order_type = mt5.ORDER_TYPE_SELL if pos['type'] == 0 else mt5.ORDER_TYPE_BUY
    orden_cierre = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": pos['symbol'],
        "type": order_type,
        "volume": pos['volume'],
        "position": ticket,  # Especificar el ticket de la posición a cerrar
        "type_filling": mt5.ORDER_FILLING_FOK,
        "comment": "Cierre AFGT"
    }
    result_cierre = mt5.order_send(orden_cierre)
    if result_cierre.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Error en orden de cierre para ticket {ticket}:", result_cierre.comment)
    else:
        print(f"Posición {ticket} cerrada exitosamente")

# Cerrar conexión
mt5.shutdown()

