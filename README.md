# Quadratic Assignment Problem (QAP) Optimization

Projekat rešava problem kvadratne dodele (QAP) korišćenjem dve metode:
1. **Brute Force** (Egzaktna metoda) - za male instance problema.
2. **Genetski Algoritam** (Metaheuristika) - za veće, kompleksnije probleme.

Projekat poredi performanse oba pristupa na standardnim QAPLIB podacima.

## Struktura projekta
- `src/`: Izvorni kod (genetski algoritam, brute force logika).
- `data/`: Ulazni podaci (matrice protoka i rastojanja).
- `results/`: Grafici konvergencije i rezultati.

## Kako pokrenuti
Potreban je Python 3 i biblioteke:
```bash
pip install numpy matplotlib