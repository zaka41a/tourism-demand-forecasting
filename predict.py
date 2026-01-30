#!/usr/bin/env python3
"""
Prediction script for Tourism Demand Forecasting.

Usage:
    python predict.py --temp 25 --holiday 1 --price 90 --month 7 --dow 5
    python predict.py --interactive
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

from src.model import load_model
from config import MODEL_SAVE_PATH


def predict_single(model, temperature, is_holiday, price, month, day_of_week):
    """Make a single prediction."""
    import numpy as np

    # Create input with all required features
    input_data = pd.DataFrame({
        "temperature": [temperature],
        "is_holiday": [is_holiday],
        "price": [price],
        "month": [month],
        "day_of_week": [day_of_week],
        "quarter": [(month - 1) // 3 + 1],
        "is_weekend": [1 if day_of_week >= 5 else 0],
        "week_of_year": [1],  # Default value
        "month_sin": [np.sin(2 * np.pi * month / 12)],
        "month_cos": [np.cos(2 * np.pi * month / 12)],
        "day_sin": [np.sin(2 * np.pi * day_of_week / 7)],
        "day_cos": [np.cos(2 * np.pi * day_of_week / 7)],
        "bookings_lag_7": [100],  # Assumed value (historical avg)
        "bookings_lag_30": [100],  # Assumed value (historical avg)
        "bookings_rolling_7": [100]  # Assumed value (historical avg)
    })

    prediction = model.predict(input_data)[0]
    return prediction


def interactive_mode(model):
    """Interactive prediction mode."""
    print("\n" + "="*60)
    print("🌍 Tourism Demand Forecasting - Interactive Prediction")
    print("="*60 + "\n")

    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
              "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    while True:
        try:
            print("\n📋 Entrez les paramètres de prédiction:\n")

            # Temperature
            temp = float(input("🌡️  Température (°C) [-5 à 40]: "))
            if not -5 <= temp <= 40:
                print("⚠️  Température hors limite. Utilisation de 20°C par défaut.")
                temp = 20

            # Holiday
            holiday_input = input("🎉 Jour férié? (o/n): ").lower()
            is_holiday = 1 if holiday_input in ['o', 'oui', 'y', 'yes'] else 0

            # Price
            price = float(input("💰 Prix (€) [50 à 150]: "))
            if not 50 <= price <= 150:
                print("⚠️  Prix hors limite. Utilisation de 90€ par défaut.")
                price = 90

            # Month
            print("\n📅 Mois:")
            for i, m in enumerate(months, 1):
                print(f"  {i:2d}. {m}")
            month = int(input("\nChoisissez le mois (1-12): "))
            if not 1 <= month <= 12:
                print("⚠️  Mois invalide. Utilisation de Juillet par défaut.")
                month = 7

            # Day of week
            print("\n📆 Jour de la semaine:")
            for i, d in enumerate(days):
                print(f"  {i}. {d}")
            dow = int(input("\nChoisissez le jour (0-6): "))
            if not 0 <= dow <= 6:
                print("⚠️  Jour invalide. Utilisation de Samedi par défaut.")
                dow = 5

            # Prediction
            prediction = predict_single(model, temp, is_holiday, price, month, dow)

            # Display result
            print("\n" + "="*60)
            print("📊 RÉSULTAT DE LA PRÉDICTION")
            print("="*60)
            print(f"\n  Température:    {temp}°C")
            print(f"  Jour férié:     {'Oui' if is_holiday else 'Non'}")
            print(f"  Prix:           {price}€")
            print(f"  Mois:           {months[month-1]}")
            print(f"  Jour:           {days[dow]}")
            print(f"\n  🎯 Réservations prédites: {prediction:.0f}")
            print("="*60 + "\n")

            # Interpretation
            if prediction < 80:
                print("  📉 Demande FAIBLE - Période creuse")
            elif prediction < 150:
                print("  📊 Demande MODÉRÉE - Période normale")
            else:
                print("  📈 Demande ÉLEVÉE - Période de pointe")

            # Continue?
            continue_pred = input("\n\nFaire une autre prédiction? (o/n): ").lower()
            if continue_pred not in ['o', 'oui', 'y', 'yes']:
                print("\n✅ Merci d'avoir utilisé le système de prédiction!")
                break

        except ValueError:
            print("\n❌ Erreur: Veuillez entrer des valeurs numériques valides.")
        except KeyboardInterrupt:
            print("\n\n✅ Au revoir!")
            break
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")


def main():
    """Main prediction function."""
    parser = argparse.ArgumentParser(
        description="Tourism Demand Forecasting - Make Predictions"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=MODEL_SAVE_PATH,
        help="Path to trained model file"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--temp",
        type=float,
        help="Temperature in Celsius"
    )
    parser.add_argument(
        "--holiday",
        type=int,
        choices=[0, 1],
        help="Is holiday? (0=no, 1=yes)"
    )
    parser.add_argument(
        "--price",
        type=float,
        help="Price in euros"
    )
    parser.add_argument(
        "--month",
        type=int,
        choices=range(1, 13),
        help="Month (1-12)"
    )
    parser.add_argument(
        "--dow",
        type=int,
        choices=range(0, 7),
        help="Day of week (0=Monday, 6=Sunday)"
    )

    args = parser.parse_args()

    # Check if model exists
    if not Path(args.model).exists():
        print(f"❌ Model file not found: {args.model}")
        print(f"\n💡 Train a model first:")
        print(f"   python train.py")
        sys.exit(1)

    # Load model
    print(f"Loading model from: {args.model}")
    try:
        model, scaler = load_model(args.model)
        print("✅ Model loaded successfully!\n")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        sys.exit(1)

    # Interactive or command-line mode
    if args.interactive:
        interactive_mode(model)
    else:
        # Check if all parameters are provided
        if None in [args.temp, args.holiday, args.price, args.month, args.dow]:
            print("❌ Error: All parameters required in CLI mode")
            print("\nUsage:")
            print("  python predict.py --temp 25 --holiday 1 --price 90 --month 7 --dow 5")
            print("\nOr use interactive mode:")
            print("  python predict.py --interactive")
            sys.exit(1)

        # Make prediction
        prediction = predict_single(
            model, args.temp, args.holiday, args.price, args.month, args.dow
        )

        # Display result
        print("="*60)
        print("📊 PRÉDICTION")
        print("="*60)
        print(f"Temperature: {args.temp}°C | Holiday: {args.holiday} | Price: {args.price}€")
        print(f"Month: {args.month} | Day: {args.dow}")
        print(f"\n🎯 Predicted bookings: {prediction:.0f}")
        print("="*60)


if __name__ == "__main__":
    main()
