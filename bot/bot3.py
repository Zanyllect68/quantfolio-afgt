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

rates = mt5.copy_rates_from_pos('USDJPY', mt5.TIMEFRAME_M1, 0,9999)
tabla_precios = pd.DataFrame(rates)
print(tabla_precios.head())

# --- Cálculo de percentiles ---

percentiles_todos = tabla_precios[['close', 'tick_volume']].quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
print("\nPercentiles de 'close' y 'tick_volume':")
print(percentiles_todos)

def orden_compra():
    orden_compra = {
         "action": mt5.TRADE_ACTION_DEAL,
         "symbol": "USDJPY",
         "type": mt5.ORDER_TYPE_BUY_LIMIT,
         "volume": 0.01,
         "type_filling": mt5.ORDER_FILLING_FOK,
         "comment": "AFGT"
         }

    result = mt5.order_send(orden_compra)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Error en orden de compra:", result.comment)
    else:
        print("Orden de compra enviada exitosamente")

ultimo_close = tabla_precios['close'].iloc[-1]
if ultimo_close == percentiles_todos.loc[0.05, 'close']:
    orden_compra()
    print("Condición de compra cumplida: close < percentil 5%")
else:
    print("Condición de compra no cumplida")
