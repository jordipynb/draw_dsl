# Proyecto de Compilación
### Integrantes:
* Dianelys Cruz Mengana C-311
* Jordan Pla González C-311
* Leandro Hernández Nuñez C-312

### Acerca de DRAW
El objetivo del DSL implementado es proveer un lenguaje que permita diseñar y dibujar figuras planas, en particular figuras que siguen determinados patrones, como es el caso de los fractales, y en su caso especial, los árboles.  
Para definir figuras es necesario especificar su identificador <nombre> y el color que se usará para dibujarla (en caso de no definirse, se dibuja con el color: negro). La definición de una figura se divide en dos secciones: Conjunto de Reglas (opcionales) y Axioma (el cuerpo de ejecución de la figura desde la cual se puede acceder a las reglas). Ambas secciones pueden contener instrucciones que incluyen el llamado a reglas (que estén definidas en el contexto de la figura, permitiendo recursividad) u otras figuras creadas con anterioridad:  
- [x] left \<expression>: cambia la dirección del cursor hacia la izquierda, la cantidad de grados resultantes de evaluar **expression**.
- [x] right \<expression>: análoga a la instrucción anterior.
- [x] line \<expression>: dibuja una línea con la longitud resultante de evaluar **expression**.
- [x] jump \<expression1>,\<expression2>: cambia las coordenadas del cursor a (**expression1**,**expression2**).
- [x] push: guarda las coordenadas actuales en una pila. 
- [x] pop: devuele el cursor a las coordenadas que están en el tope de la pila.
- [x] call_shape \<shape_name>: pinta la figura especificada en **shape_name** (debe estar definida con anterioridad).
- [x] call_rule \<rule_name> (expression): ejecuta la regla especificada en **rule** del cuerpo de la figura donde se esta invocando con el argumento resultante de evaluar **expression**.
- [x] \<variable> = <expression>: asigna el resultado de evaluar **expression** a una **variable**. 
- [x] \<variable> = get_x: asigna a una variable el valor de las coordenadas actuales en **x**.
- [x] \<variable> = get_y: análoga a la instrucción anterior.
- [x] set_x \<expression>: cambia las coordenadas actuales de **x** por el resultado de evaluar **expression**.
- [x] set_y \<expression>: análoga a la instrucción anterior.

> En cuanto a las características de la gramática, podemos afirmar que la gramática no es ambigua, por lo que no fue necesario usar ninguna herramienta del generador de compiladores YACC para desambiguarla: como la utilización de la precedencia y restricciones de asociatividad. Dicha afirmación se puede comprobar ya que en el output del generador se puede percibir que para cada cadena válida se tiene una única derivación a la izquierda. Se tiene una gramática libre del contexto donde cada regla de producción es de la forma:    
> <p align="center"> V → w </p>    
> donde V es un no terminal y w es una cadena de terminales y/o no terminales. En el caso de este problema, dicha gramática tiene una naturaleza decidible habiendo encontrado un algoritmo de decisión u analizador para resolverlo (LALR).

### Arquitectura del Compilador
* Lexer: para la realización del lexer se utilizó la librería ```ply.py``` por la facilidad aportaba para su uso.
* Parser: igual que con el lexer se utilizó el proporcionado por la librería ```ply.py``` por la eficiencia del parser LALR.
* AST: para la construcción del ast se creó una jerarquía de clases que se puede encontrar en ```utils.py``` haciendo uso de estos nodos en las reglas y/o producciones de la gramática establecida
* Semantic:
* Interpreter: 

### Instalar los paquetes necesarios
```zsh
pip install -r requirements.txt
```

### Ejecutar el proyecto
```
python main.py
```
