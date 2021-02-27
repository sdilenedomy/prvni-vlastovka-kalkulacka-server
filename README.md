# Server pro kalkulačku půjček První vlaštovky

## O serveru
Server je napsaný v Pythonu a používá framework Django. Obsahuje dvě aplikace, `language_switcher` a `loans`.

### Language switcher
Přidává možnost uživatelovi přepnout jazyk v administračním prostředí pomocí vlaječek v navigaci. Samotné překlady jsou ve složkách jednotlivých aplikací, pro aplikaci pro správu půjček je to v `loans/locale`.

Jazyky lze přidat úpravou `LANGUAGES` v settings.py a přidáním příslušené vlaječky do `language_switcher/static/img`.

### Loans
Aplikace pro správu půjček přidává do administračního prostředí (url `/admin`) nabídky a přijeté půjčky. Nabídku mohou uživatelé s oprávněním `accept_loanoffer` nahráním souboru s podepsanou smlouvou přijmout a přesunout ji tak mezi přijaté půjčky. Smlouvy jsou potom uživatelům s oprávněním k zobrazování přijatých půjček dostupné na adrese `/media/contracts/filename-smlouvy` nebo skrz administrační rozhraní.

Na endpoint `/api` je možné bez autentifikace odeslat POST request a přidat tak nabídku na půjčku. 

## Deployment

### Neverzované soubory

#### key.txt
Soubor settings.py načítá `SECRET_KEY` ze souboru `key.txt` z kořenového adresáře projektu. Klíč je možné vygenerovat takto:

`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > key.txt`

### settings.py
Před nasazením do produkce je možné zkontrolovat settings.py automaticky pomocí

`python manage.py check --deploy`

Checklist všech potřebných nastavení lze najít v Django [dokumentaci](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/).

Dokumentaci k propojení s HTTP serverem lze najít [zde](https://docs.djangoproject.com/en/3.1/howto/deployment/).
