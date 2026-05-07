---
title: "Interpretación de movimientos de stock en farmacia comunitaria"
document_id: "04_interpretacion_movimientos_stock"
version: "1.0"
domain: "Optimización de stock en farmacia comunitaria"
use_in_rag: true
contains_real_data: false
---

# Interpretación de movimientos de stock en farmacia comunitaria

## 1. Qué es un movimiento de stock

Un movimiento de stock es cualquier evento registrado en el sistema de gestión que modifica, confirma o corrige el inventario de un producto. Puede representar una salida, una entrada, una regularización, un recuento, una devolución o una anulación. En términos logísticos, cada movimiento ayuda a reconstruir qué ha pasado con las unidades disponibles de una referencia a lo largo del tiempo.

Un movimiento de stock suele contener varios elementos: fecha, producto, tipo de movimiento, unidades asociadas al movimiento, stock anterior, stock posterior o stock resultante, y en algunos casos información adicional sobre el origen del registro. No todos los sistemas muestran todos estos campos, pero para interpretar bien el inventario conviene distinguirlos.

La diferencia más importante es la que existe entre unidades del movimiento, stock anterior, stock posterior y delta. Las unidades del movimiento son el número que aparece asociado a un evento. El stock anterior es el inventario disponible antes del movimiento. El stock posterior es el inventario que queda después del movimiento. El delta es la variación real entre stock posterior y stock anterior.

La regla conceptual básica es:

```text
Delta = stock posterior - stock anterior
```

Ejemplo sencillo: si antes de un movimiento había 10 unidades y después quedan 7, el delta es -3. Eso indica una salida neta de 3 unidades. Si antes había 10 y después quedan 15, el delta es +5. Eso indica una entrada neta o corrección positiva de 5 unidades.

La advertencia principal es que no siempre las unidades del movimiento equivalen directamente al delta real. En algunos tipos de movimiento, especialmente modificaciones manuales o recuentos, el campo de unidades puede representar el stock fijado o el valor resultante, no necesariamente la cantidad que ha entrado o salido. Por eso, FarmaStock AI debe interpretar cada movimiento según su tipo y no asumir que todos los campos significan lo mismo.

## 2. Movimientos de venta

Un movimiento de venta representa una salida de unidades del inventario asociada a una operación de venta. Desde el punto de vista de gestión de stock, la venta es importante porque reduce el stock disponible y permite construir la demanda histórica del producto.

En un análisis operativo, las ventas se utilizan principalmente para medir consumo o salida. Permiten calcular ventas medias, rotación, cobertura y posibles necesidades de reposición. Sin embargo, una venta operativa no debe confundirse con un informe comercial completo. La venta como movimiento de stock se centra en unidades que salen del inventario; un informe comercial puede incluir importes, descuentos, impuestos, categorías o datos de facturación que no siempre son necesarios para reconstruir stock.

Ejemplo sencillo: si un producto tenía 20 unidades y se registran 3 unidades vendidas, el stock posterior esperado sería 17 unidades, siempre que no haya otros movimientos simultáneos o correcciones intermedias.

La interpretación conceptual sería:

```text
Stock posterior esperado = stock anterior - unidades vendidas
```

Los movimientos de venta ayudan a calcular la demanda histórica, pero deben revisarse con cuidado. Puede haber anulaciones, devoluciones, errores de registro o ventas corregidas. También puede haber diferencias entre el momento comercial de la venta y el momento en que el stock se actualiza en el sistema.

La advertencia principal es que no toda salida de stock debe interpretarse como venta real para demanda futura. Una anulación, una devolución corregida, una regularización negativa o una retirada no representan necesariamente demanda ordinaria. FarmaStock AI debe distinguir entre venta operativa válida y otros movimientos de salida cuando el objetivo sea calcular demanda o reposición.

## 3. Movimientos de compra o entrada

Un movimiento de compra o entrada representa la incorporación de unidades al inventario. Puede proceder de una recepción de pedido, una entrada manual, una reposición registrada o una corrección positiva del stock. Desde el punto de vista logístico, una entrada aumenta el stock disponible y puede cerrar una situación de baja cobertura o riesgo de rotura.

Es importante diferenciar entre pedido y recepción. Un pedido es una solicitud de unidades. Una recepción es la entrada efectiva de unidades al inventario. Para reconstruir stock, lo relevante es la recepción real, no la intención inicial de compra. Si se piden 20 unidades pero entran 12, el inventario solo aumenta en 12 unidades.

La interpretación conceptual de una entrada simple es:

```text
Stock posterior esperado = stock anterior + unidades recibidas
```

Ejemplo sencillo: si un producto tenía 5 unidades y se reciben 10 unidades, el stock posterior esperado sería 15 unidades, siempre que no haya ventas, devoluciones o ajustes registrados entre medias.

Los movimientos de entrada también son útiles para estimar plazos de reposición si se conoce la relación entre pedido y recepción. Sin embargo, en muchos análisis básicos solo se dispone del movimiento de entrada y no del pedido original. En ese caso, puede saberse que el stock aumentó, pero no calcular con precisión el tiempo de reposición.

La advertencia principal es que no toda entrada debe interpretarse como compra ordinaria. Un ajuste positivo, una devolución de unidades, una regularización tras recuento o una modificación manual pueden aumentar el stock sin representar una compra real. FarmaStock AI debe explicar esta diferencia y evitar inferir compras si el tipo de movimiento no lo confirma.

## 4. Recuentos de inventario

Un recuento de inventario es una verificación del stock físico disponible. Su función es comparar lo que el sistema indica con lo que realmente se encuentra en la farmacia o en el almacén. Puede ser un recuento total, cuando se revisa una gran parte del inventario, o parcial, cuando se revisan productos concretos.

El recuento no siempre representa una entrada o una salida real. Puede simplemente confirmar que el stock teórico coincide con el físico, o puede provocar una corrección si se detecta diferencia. Por eso, desde el punto de vista analítico, un recuento debe interpretarse como un evento de validación o regularización.

Ejemplo sencillo: si el sistema indica 18 unidades, pero al hacer el recuento físico se encuentran 16, el stock debe corregirse a 16. La diferencia es un delta de -2 unidades. Esa salida no significa necesariamente una venta; puede ser un descuadre, error de registro, merma, devolución no registrada u otra incidencia operativa.

La regla conceptual es:

```text
Delta de recuento = stock contado - stock teórico anterior
```

Si el delta es positivo, el sistema tenía menos unidades registradas de las que había físicamente. Si el delta es negativo, el sistema tenía más unidades registradas de las que había físicamente.

Los recuentos son especialmente útiles en productos con descuadres frecuentes, alta rotación, muchas manipulaciones o diferencias entre stock físico y stock teórico. También pueden ayudar a mejorar la calidad de los datos antes de calcular coberturas, puntos de pedido o riesgos de rotura.

La advertencia principal es que el delta de un recuento no debe mezclarse con demanda ordinaria. Si un recuento reduce el stock, no significa que esas unidades se hayan vendido. Para calcular demanda histórica, conviene separar ventas reales de regularizaciones de inventario.

## 5. Ajustes de stock

Un ajuste de stock es una corrección del inventario registrada para alinear el stock del sistema con una situación considerada correcta. Puede ser positivo, si aumenta el stock, o negativo, si lo reduce. Los ajustes pueden deberse a recuentos, errores de registro, deterioros, caducidades, unidades localizadas posteriormente o regularizaciones internas.

Desde el punto de vista logístico, un ajuste modifica el stock, pero no siempre representa una compra o una venta. Esta distinción es fundamental. Un ajuste positivo puede parecer una entrada, pero no necesariamente implica que se haya comprado producto. Un ajuste negativo puede parecer una salida, pero no necesariamente implica demanda.

Ejemplo sencillo: si el sistema muestra 8 unidades y se detecta que físicamente hay 10, puede registrarse un ajuste positivo de +2. El stock aumenta, pero no porque se haya recibido una compra, sino porque se ha corregido un descuadre.

La regla conceptual es:

```text
Ajuste positivo = aumento del stock por regularización
Ajuste negativo = reducción del stock por regularización
```

Los ajustes deben analizarse porque pueden indicar problemas de calidad del dato. Si un producto presenta muchos ajustes, puede haber errores recurrentes en ventas, entradas, ubicación, recuentos o manipulación del inventario. Estos productos pueden requerir revisión manual prioritaria.

La advertencia principal es que los ajustes no deben usarse sin control para reconstruir demanda. Un ajuste negativo no equivale a venta, y un ajuste positivo no equivale a compra. FarmaStock AI debe tratar los ajustes como regularizaciones, no como movimientos comerciales ordinarios, salvo que el contexto indique claramente otra cosa.

## 6. Modificaciones manuales

Una modificación manual es un cambio introducido directamente sobre el stock de un producto. Puede utilizarse para corregir el inventario, registrar una regularización o fijar un nuevo valor de stock. Es uno de los tipos de movimiento que más cuidado requiere al interpretarlo, porque el campo de unidades puede no representar una entrada o salida real.

En algunos sistemas, una modificación manual puede mostrar el nuevo stock final fijado, no el número de unidades que han entrado o salido. Por eso, para interpretarla correctamente hay que comparar el stock anterior con el stock posterior. La clave es calcular el delta.

La regla conceptual es:

```text
Delta de modificación manual = stock posterior - stock anterior
```

Si el delta es positivo, la modificación ha aumentado el stock. Si el delta es negativo, la modificación ha reducido el stock. Si el delta es cero, la modificación no ha cambiado realmente la cantidad, aunque pueda haber corregido otro dato o confirmado una cifra.

Ejemplo sencillo: si antes había 5 unidades y tras una modificación manual el stock posterior es 12, el delta es +7. La interpretación logística es una entrada neta o corrección positiva de 7 unidades. No debe asumirse que se compraron 12 unidades. El valor 12 representa el stock final, no necesariamente la cantidad añadida.

Otro ejemplo: si antes había 20 unidades y después de una modificación manual el stock queda en 14, el delta es -6. La interpretación logística es una reducción neta de 6 unidades. No debe tratarse como una venta ordinaria salvo que el tipo de movimiento lo confirme.

Las modificaciones manuales son útiles para corregir errores, pero si aparecen con mucha frecuencia pueden reducir la fiabilidad del histórico. También pueden dificultar la reconstrucción de compras, ventas o demanda si no se separan correctamente de los movimientos operativos ordinarios.

La advertencia principal es que FarmaStock AI no debe interpretar una modificación manual como compra, venta o demanda sin más información. Si no se conoce el stock anterior o el stock posterior, no se puede calcular el delta con seguridad. En ese caso, el agente debe indicar qué dato falta.

## 7. Devoluciones y anulaciones

Las devoluciones y anulaciones son movimientos que revierten o corrigen operaciones previas. Una devolución puede aumentar o reducir stock según su tipo. Una anulación puede corregir una venta, una entrada u otro movimiento anterior. Su interpretación depende del sentido del movimiento y del evento que corrigen.

Una devolución de unidades al inventario puede aumentar el stock disponible. Una devolución hacia fuera puede reducirlo. Una anulación de venta puede revertir una salida que no debería contar como demanda real. Por eso, estos movimientos deben identificarse y separarse cuando el objetivo sea calcular demanda histórica, rotación o cobertura.

Ejemplo sencillo: si se registró una venta de 2 unidades y posteriormente se anula, no debería interpretarse como una demanda neta de 2 unidades si la operación quedó revertida. Para calcular la demanda real, habría que considerar el efecto neto.

La regla conceptual puede expresarse así:

```text
Efecto neto = movimiento original + movimiento de corrección
```

Si una venta de -2 se anula con una corrección de +2, el efecto neto sobre el stock puede ser 0, aunque ambos movimientos aparezcan en el histórico.

Las devoluciones y anulaciones son importantes para la limpieza de datos. Si no se tratan correctamente, pueden inflar o reducir artificialmente la demanda. También pueden alterar la interpretación de coberturas, rotaciones y riesgos de rotura.

La advertencia principal es que no toda devolución debe tratarse igual. Hay que conocer si devuelve unidades al inventario, si sale del inventario, si corrige una operación previa o si representa una regularización. FarmaStock AI debe mantener una interpretación prudente si el tipo de devolución o anulación no está claramente definido.

## 8. Stock resultante tras cada movimiento

El stock resultante es la cantidad de unidades que queda después de registrar un movimiento. Es una de las columnas más importantes para reconstruir la evolución de inventario, porque permite observar cómo cambia el stock a lo largo del tiempo.

Para analizar correctamente una secuencia de movimientos, es necesario ordenarlos cronológicamente. Si los movimientos no están ordenados por fecha y hora, la reconstrucción puede ser incorrecta. El stock posterior de un movimiento puede actuar como stock anterior del siguiente movimiento, siempre que no falten registros intermedios.

La lógica conceptual es:

```text
Stock anterior del movimiento actual = stock posterior del movimiento anterior
```

Y para cada movimiento:

```text
Delta = stock posterior - stock anterior
```

Ejemplo sencillo: un producto tiene estos cambios: empieza con 10 unidades, se venden 2 y queda en 8; después entran 5 y queda en 13; después se hace un ajuste negativo y queda en 12. La secuencia permite entender no solo el stock final, sino cómo se llegó a él.

El stock resultante ayuda a detectar inconsistencias. Si una venta de 3 unidades no reduce el stock, puede haber otro movimiento simultáneo, una corrección, una reserva, un error de registro o una particularidad del sistema. Si una entrada no aumenta el stock, también conviene revisar el contexto.

La advertencia principal es que el stock resultante solo es fiable si los movimientos están completos y bien ordenados. Si faltan movimientos, si hay registros duplicados o si la fecha no representa el orden real de actualización, el análisis puede ser incorrecto. FarmaStock AI debe pedir más información si la secuencia no es suficiente.

## 9. Diferencia entre informes comerciales y movimientos operativos

Los informes comerciales y los movimientos operativos no responden a la misma pregunta. Un informe comercial suele centrarse en ventas, importes, descuentos, categorías, facturación, periodos o análisis económico. Un movimiento operativo se centra en la variación del inventario: entradas, salidas, ajustes y stock resultante.

Para analizar stock, los movimientos operativos suelen ser más útiles porque permiten reconstruir qué pasó con las unidades disponibles. Para analizar facturación, margen o comportamiento comercial, los informes comerciales pueden aportar más contexto. Ambos tipos de información pueden ser valiosos, pero no deben mezclarse sin limpieza.

Ejemplo sencillo: un informe comercial puede indicar que se vendieron productos por cierto importe durante un periodo. Sin embargo, para saber si el stock de una referencia concreta bajó, subió o fue corregido, se necesita el histórico de movimientos de inventario.

La diferencia conceptual puede resumirse así:

```text
Informe comercial = análisis económico o de ventas agregadas
Movimiento operativo = evento que modifica o confirma el stock
```

Un problema frecuente es usar ventas comerciales agregadas como si fueran movimientos de inventario completos. Esto puede llevar a errores si hay devoluciones, anulaciones, correcciones, descuentos, cambios de presentación o diferencias de registro. También puede ocurrir lo contrario: usar movimientos operativos para hacer análisis comercial sin tener importes, categorías o información económica suficiente.

La advertencia principal es que FarmaStock AI debe identificar el objetivo de la pregunta. Si la pregunta trata sobre demanda, cobertura o reconstrucción de stock, deben priorizarse movimientos operativos. Si trata sobre facturación o análisis económico, harían falta datos comerciales adicionales. Este documento se centra en el análisis logístico del inventario.

## 10. Reglas de negocio para FarmaStock AI

Las reglas de negocio son criterios explícitos que ayudan al agente a interpretar movimientos de stock de forma consistente. En FarmaStock AI, estas reglas se orientan al análisis logístico y formativo del inventario, no a decisiones clínicas ni comerciales cerradas.

Reglas principales:

```text
1. Una venta ordinaria se interpreta como salida de stock.
2. Una compra o recepción confirmada se interpreta como entrada de stock.
3. Un recuento se interpreta como verificación o regularización del stock.
4. Un ajuste se interpreta como corrección, no como venta ni compra automática.
5. Una modificación manual debe interpretarse mediante delta.
6. Una devolución o anulación debe analizarse por su efecto neto.
7. El stock resultante debe usarse para reconstruir la evolución temporal.
8. Si falta stock anterior o posterior, no debe calcularse delta con seguridad.
9. Si falta el tipo de movimiento, la interpretación debe ser prudente.
10. No deben inventarse cantidades, compras, ventas ni causas no documentadas.
```

Estas reglas permiten que el agente mantenga coherencia al responder. Por ejemplo, si se pregunta por una modificación manual, el agente debe explicar que necesita stock anterior y stock posterior para calcular el delta. Si se pregunta por una venta, puede explicar que normalmente reduce stock y alimenta demanda histórica. Si se pregunta por un ajuste, debe advertir que no equivale necesariamente a demanda.

Ejemplo sencillo: si un registro muestra una modificación manual con stock anterior de 7 y stock posterior de 10, FarmaStock AI debe interpretar un delta de +3, no una compra de 10 unidades.

La advertencia principal es que las reglas de negocio dependen de la estructura del sistema de datos. Si un sistema de gestión utiliza nombres distintos o campos con significados diferentes, las reglas deben adaptarse. Por eso, ante dudas, el agente debe pedir aclaración sobre columnas, tipo de movimiento y significado de los campos.

## 11. Errores frecuentes al interpretar movimientos

Uno de los errores más frecuentes es confundir unidades del movimiento con stock final. En algunos registros, el número mostrado puede representar unidades movidas; en otros, puede representar el stock resultante. Si no se distingue, se pueden inflar entradas o salidas.

Otro error habitual es interpretar una modificación manual positiva como una compra. Si el stock pasa de 5 a 12, la variación real es +7, no necesariamente una compra de 12 unidades. Del mismo modo, si el stock pasa de 20 a 14, la variación es -6, pero no debe interpretarse automáticamente como venta.

También es frecuente confundir pedido con recepción. Un pedido de 30 unidades no aumenta el stock si todavía no se ha recibido. Para reconstruir inventario, debe registrarse la entrada efectiva.

Otros errores comunes son no ordenar movimientos por fecha, ignorar anulaciones, mezclar informes comerciales con movimientos operativos, tratar ajustes negativos como ventas reales, duplicar registros, no separar productos con presentaciones diferentes o calcular demanda con datos afectados por recuentos y regularizaciones.

Ejemplo sencillo: si se suman ventas, anulaciones y ajustes negativos como si todos fueran demanda, la demanda histórica quedará distorsionada. Esto puede provocar puntos de pedido demasiado altos o conclusiones equivocadas sobre la rotación.

La advertencia principal es que un histórico de movimientos necesita limpieza antes de alimentar cálculos. FarmaStock AI puede explicar reglas y detectar posibles errores conceptuales, pero no debe asumir que un dataset está limpio si no se han validado tipos de movimiento, orden temporal, duplicados y significado de columnas.

## 12. Límites del agente al interpretar movimientos

FarmaStock AI puede ayudar a explicar e interpretar movimientos de stock desde una perspectiva logística, pero tiene límites claros. No debe inventar datos, causas ni cantidades. Si no dispone de stock anterior, stock posterior, tipo de movimiento o fecha, debe indicar que la interpretación es incompleta.

El agente tampoco debe reconstruir un inventario completo a partir de un movimiento aislado. Para reconstruir la evolución de stock se necesita una secuencia ordenada de movimientos. Un único registro puede dar pistas, pero no permite conocer todo el contexto.

FarmaStock AI no debe interpretar movimientos como consejo clínico ni hacer recomendaciones relacionadas con tratamientos. Tampoco debe usar datos reales sensibles ni información identificable de personas, proveedores, operaciones comerciales reales o una farmacia concreta. Los ejemplos deben ser genéricos o sintéticos. Si se menciona un sistema de gestión, debe hacerse de forma genérica, como ejemplo de software que registra movimientos de inventario.

Ejemplo sencillo: si se pregunta “este movimiento tiene unidades 15, ¿es una compra?”, el agente no puede responder con seguridad si no conoce el tipo de movimiento y si esas unidades representan cantidad movida o stock final. La respuesta correcta sería explicar qué datos faltan y cómo se interpretaría cada caso.

La advertencia principal es que la interpretación de movimientos depende mucho del significado de las columnas. Dos sistemas pueden usar nombres parecidos para campos distintos. Por eso, el agente debe ser prudente y explicar supuestos cuando no tenga certeza.

## 13. Preguntas que puede responder este documento

Este documento permite responder preguntas sobre movimientos de stock, ventas, entradas, recuentos, ajustes, modificaciones manuales, devoluciones, anulaciones, stock resultante, delta e interpretación logística de inventario. Está diseñado para que un sistema RAG pueda recuperar definiciones, reglas conceptuales, ejemplos y límites de uso relacionados con la reconstrucción y revisión de stock en farmacia comunitaria.

Preguntas que puede responder:

- ¿Qué es un movimiento de stock?
- ¿Qué diferencia hay entre unidades del movimiento, stock anterior, stock posterior y delta?
- ¿Cómo se calcula el delta de un movimiento?
- ¿Qué representa una venta en el análisis de stock?
- ¿Qué diferencia hay entre una venta operativa y un informe comercial?
- ¿Qué representa una compra o entrada en el inventario?
- ¿Por qué no es lo mismo pedido que recepción?
- ¿Qué es un recuento de inventario?
- ¿Cómo se interpreta un ajuste positivo?
- ¿Cómo se interpreta un ajuste negativo?
- ¿Qué significa una modificación manual positiva?
- ¿Por qué una modificación manual no debe interpretarse automáticamente como compra?
- Si el stock pasa de 5 a 12, ¿cuál es el delta?
- Si el stock pasa de 20 a 14, ¿qué variación se interpreta?
- ¿Cómo afectan las devoluciones y anulaciones a la demanda histórica?
- ¿Por qué es importante el stock resultante tras cada movimiento?
- ¿Cómo se reconstruye la evolución de stock de un producto?
- ¿Qué errores son frecuentes al interpretar movimientos?
- ¿Qué datos faltan para interpretar correctamente una modificación manual?
- ¿Qué límites tiene FarmaStock AI al analizar movimientos de stock?