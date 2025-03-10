# --------------------------------------- INFO ----------------------------------------------------------
#Prueba Técnica : Tarea 1 - Códica
#Postulante: David Fajardo
# ------------------------------------ LIBRERIAS ---------------------------------------------------------

import requests
import json
from typing import Dict, List
import freecurrencyapi

# ------------------------------------ FUNCIONES DEL PROGRAMA --------------------------------------------------------------
class CurrencyConverter:
    
    def __init__(self):
        self.api_key = 'fca_live_TBuczpLs8Pwu4T6zrSL80Nyb62cHO9d1QZJF23b2'  # API key, varia del usuario
        self.base_url = 'https://api.freecurrencyapi.com/v1'
        self.conversion_history: List[Dict] = []
        self.supported_currencies: Dict = self.get_supported_currencies()
        self.exchange_rates: Dict = self.get_exchange_rates()

    def get_supported_currencies(self) -> Dict:
        """Obtiene la lista de monedas soportadas."""
        try:
            url = f"{self.base_url}/currencies?apikey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()['data']
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener monedas soportadas: {e}")
            return {}

    def get_exchange_rates(self, base_currency: str = 'USD') -> Dict:
        """Obtiene las tasas de cambio actuales."""
        try:
            url = f"{self.base_url}/latest?apikey={self.api_key}&base_currency={base_currency}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()['data']
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener tasas de cambio: {e}")
            return {}

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convierte una cantidad de una moneda a otra."""
        if from_currency not in self.exchange_rates or to_currency not in self.exchange_rates:
            print("Moneda no válida.")
            return 0.0

        # Conversión usando USD como moneda base
        usd_amount = amount / self.exchange_rates[from_currency]
        converted_amount = usd_amount * self.exchange_rates[to_currency]
        
        conversion_info = {
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': round(converted_amount, 2)
        }
        self.conversion_history.append(conversion_info)
        
        return round(converted_amount, 2)

    def display_currencies(self):
        """Muestra la lista de monedas soportadas."""
        print("\n--- Monedas Soportadas ---")
        for code, info in self.supported_currencies.items():
            print(f"{code}: {info['name']}")

    def display_exchange_rates(self, base_currency: str = 'USD'):
        """Muestra las tasas de cambio."""
        print(f"\n--- Tasas de Cambio (Base: {base_currency}) ---")
        for currency, rate in self.exchange_rates.items():
            print(f"1 {base_currency} = {rate} {currency}")

    def display_conversion_history(self):
        """Muestra el historial de conversiones."""
        if not self.conversion_history:
            print("\nNo hay conversiones realizadas.")
            return

        print("\n--- Historial de Conversiones ---")
        for conversion in self.conversion_history:
            print(f"{conversion['amount']} {conversion['from_currency']} = "
                  f"{conversion['converted_amount']} {conversion['to_currency']}")

    def validate_currency(self, currency_code: str) -> bool:
        """Valida si el código de moneda existe."""
        return currency_code in self.supported_currencies

    def validate_amount(self, amount: str) -> bool:
        """Valida que el monto sea un número válido."""
        try:
            float_amount = float(amount)
            return float_amount > 0
        except ValueError:
            return False

    def run(self):
        """Menú principal de la aplicación."""
        while True:
            print("\n--- Convertidor de Divisas Códica---")
            print("1. Mostrar Monedas Soportadas")
            print("2. Mostrar Tasas de Cambio")
            print("3. Realizar Conversión")
            print("4. Ver Historial de Conversiones")
            print("5. Salir")

            opcion = input("Seleccione una opción (1-5): ")

            if opcion == '1':
                self.display_currencies()
            elif opcion == '2':
                self.display_exchange_rates()
            elif opcion == '3':
                from_currency = input("Ingrese moneda de origen (código): ").upper()
                if not self.validate_currency(from_currency):
                    print("Moneda de origen no válida.")
                    continue

                to_currency = input("Ingrese moneda de destino (código): ").upper()
                if not self.validate_currency(to_currency):
                    print("Moneda de destino no válida.")
                    continue

                amount_str = input("Ingrese monto a convertir: ")
                if not self.validate_amount(amount_str):
                    print("Monto no válido.")
                    continue

                amount = float(amount_str)
                result = self.convert_currency(amount, from_currency, to_currency)
                print(f"\n{amount} {from_currency} = {result} {to_currency}")

            elif opcion == '4':
                self.display_conversion_history()
            elif opcion == '5':
                print("Gracias por usar el Convertidor de Divisas Códica. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 5.")

# -------------------------------------- MAIN ------------------------------------------------------------------

def main():
    converter = CurrencyConverter()
    converter.run()

if __name__ == "__main__":
    main()