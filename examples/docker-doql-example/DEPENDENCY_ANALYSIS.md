# DOQL - Analiza Zależności

## Co przechowuje format app.doql.less

Format `app.doql.less` **zawiera** informacje o zależnościach w różnych warstwach:

### 1. Hardware → Service Zależności
```less
service[name="web-api"] {
  instance: [app-server-1, app-server-2];
}
```
Pole `instance` pokazuje, które usługi działają na którym hardware.

### 2. Network → Service Zależności
```less
network[name="backend"] {
  services: [load-balancer, app-server-1, app-server-2, ...];
}
```
Lista usług w sieci pokazuje łączność sieciową.

### 3. Volume → Service Zależności
```less
volume[name="db-data"] {
  service: database;
  path: /var/lib/postgresql/data;
}
```
Woluminy pokazują, które usługi używają trwałego storage.

### 4. Workflow → Service Zależności
```less
workflow[name="health-check"] {
  step-2: run cmd=docker compose exec app-server-1 curl ...;
  step-3: run cmd=docker compose exec database pg_isready ...;
}
```
Workflow pokazuje operacyjne zależności między usługami.

### 5. Interface → Service Zależności
```less
interface[type="postgresql"] {
  port: 5432;
  service: database;
}
```
Interfejsy pokazują punkty komunikacji usług.

## Brakujące informacje o zależnościach

Format NIE zawiera:
- ❌ Zależności w kodzie (importy modułów, wywołania funkcji)
- ❌ Zależności bibliotek (package.json, requirements.txt, Cargo.toml)
- ❌ Zależności środowiskowe (zmienne środowiskowe)
- ❌ Zależności danych (schematy baz danych, struktury API)
- ❌ Zależności czasowe (kolejność uruchamiania)
- ❌ Zależności warunkowe (if/else w konfiguracji)

## Czy DOQL automatycznie wykrywa zależności?

**Nie mam pewności.** Z dostępnych informacji wynika, że:

1. DOQL jest instalowany przez pip: `pip install doql`
2. Jest używany w ekosystemie: SUMD → DOQL → taskfile → testql
3. Generuje pliki `app.doql.less`

Jednak:
- Nie znalazłem dokumentacji DOQL
- Nie znalazłem kodu źródłowego DOQL
- Przykłady pokazują ręczne generowanie (run-doql.sh używa `cat > app.doql.less`)

## Rekomendacja

Aby DOQL wykrywał zależności, potrzebowałby:

1. **Analiza kodu źródłowego** - parsing plików w różnych językach
2. **Analiza konfiguracji** - docker-compose.yml, package.json, itp.
3. **Analiza runtime** - monitorowanie połączeń sieciowych
4. **Analiza logów** - wykrywanie wzorców komunikacji

**Obecny format** app.doql.less jest **deklaratywny** - wymaga ręcznego zdefiniowania zależności, nie automatycznego wykrywania.

## Wnioski

Format `app.doql.less`:
- ✅ **Może przechowywać** informacje o zależnościach infrastrukturalnych
- ✅ **Jest strukturą** do mapowania zależności
- ❌ **Nie automatycznie wykrywa** zależności (brak dowodów)
- ❌ **Nie analizuje kodu** źródłowego

Do pełnego wykrywania zależności AI/LLM potrzebny byłby:
- Parser kodu dla każdego języka
- Analiza AST (Abstract Syntax Tree)
- Wykrywanie wywołań funkcji
- Analiza importów modułów
- Rekonstrukcja grafu zależności
