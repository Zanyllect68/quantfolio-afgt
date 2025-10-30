# Optimización de Markowitz

## Concepto
El modelo busca minimizar la varianza del portafolio para un nivel de retorno esperado.

### Fórmula
Min: wᵀΣw  
Sujeto a:  
∑wᵢ = 1  
∑wᵢμᵢ = μp  

### Notas personales
- Probar restricción de no short-selling (wᵢ ≥ 0)
- Comparar resultados con modelo de riesgo paritario
- Implementar versión con PyPortfolioOpt
