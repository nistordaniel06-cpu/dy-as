# Instalare DY-AS

Pe o mașină Linux cu Docker și Docker Compose, clonează repository-ul. Configurează un subdomeniu de test al cărui DNS indică IP-ul serverului și permite conexiuni HTTP și HTTPS. Din rădăcina proiectului rulează:

```sh
STORE_HOST=test.exemplu.ro ADMIN_EMAIL=administrator@exemplu.ro bash deploy/start.sh
```

Înlocuiește ambele valori. Salvează parola afișată în terminal. Deschide /wp-admin și importă catalog.csv și catalog-scule.csv din Produse → Import. Sculele se importă ca schițe. Configurează tarifele de livrare, datele comerciantului și contul de test al extensiei Stripe. Verifică de pe telefon o comandă fără cont și primirea confirmării de plată înainte de lansare. Datele rămân în volume Docker. Păstrează copii externe ale bazei de date și fișierelor înainte de actualizări.
