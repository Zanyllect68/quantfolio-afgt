import  MetaTrader5 as mt5
import pandas as pd

path = r'C:\Program Files\RoboForex MT5 Terminal\terminal64.exe'
nombre = 67106046
contraseña = 'Sebas.123'
server = 'RoboForex-ECN'    
mt5.initialize(login=nombre, password=contraseña, server=server, path=path)

rates = mt5.copy_rates_from_pos('XAUUSD', mt5.TIMEFRAME_M1, 0,9999)
tabla_precios = pd.DataFrame(rates)
tabla_precios['time'] = pd.to_datetime(tabla_precios['time'], unit='s')
print(tabla_precios.head())

mt5.shutdown()
