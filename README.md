## Requisitos
### Instalación de python3
https://www.python.org/downloads/

### Instalación de pip3
Descarga el archivo de instalación de pip3 con el siguiente comando en la terminal:

```curl -s https://bootstrap.pypa.io/get-pip.py | python```

### Instalación de dependencias
Use el siguiente comando. En caso de que falle, use el segundo:

```
pip install tabulate xlrd
pip3 install tabulate xlrd
```

## Uso del script
```
user@local: $ python pairings.py
[*] Usage: python pairings.py <path_to_xls_file_with_pairings>
[!] You must specify xls file as an argument
```

Ejemplo: python pairings.py C:\Users\Username\Downloads\Pairings_del_mes.xls

Es posible que, en vez de python3, deba usar python, dependiendo de su sistema operativo.
