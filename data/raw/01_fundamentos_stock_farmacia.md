---
title: "Fundamentos de gestión de stock en farmacia comunitaria"
document_id: "01_fundamentos_stock_farmacia"
version: "1.0"
domain: "Optimización de stock en farmacia comunitaria"
use_in_rag: true
contains_real_data: false
---

# Fundamentos de gestión de stock en farmacia comunitaria

## 1. Introducción a la gestión de stock en farmacia comunitaria

La gestión de stock en farmacia comunitaria consiste en controlar, revisar y ajustar las existencias de productos disponibles para que la farmacia pueda responder a la demanda habitual sin acumular un exceso innecesario de inventario. El objetivo no es tener muchas unidades de todos los productos, sino disponer de una cantidad razonable, equilibrada y adaptada al comportamiento de cada referencia.

En una farmacia comunitaria conviven productos con comportamientos muy distintos. Algunos tienen una salida frecuente y previsible, otros se venden de forma ocasional, otros dependen de campañas estacionales y otros pueden permanecer mucho tiempo sin movimiento. Por eso, una gestión correcta del stock debe tener en cuenta la rotación, la cobertura, el stock mínimo, el punto de pedido, el riesgo de rotura, el riesgo de sobrestock y la posible caducidad de los productos.

La gestión de stock tiene una dimensión operativa y económica. Desde el punto de vista operativo, ayuda a reducir situaciones en las que un producto no está disponible cuando se necesita. Desde el punto de vista económico, ayuda a evitar que demasiados recursos queden inmovilizados en productos con baja salida o con riesgo de caducar. También mejora la organización interna, porque permite priorizar qué productos revisar con más frecuencia y contribuye a mantener una buena calidad del servicio.

Ejemplo sencillo: una farmacia puede tener un almacén lleno y, aun así, presentar problemas de stock. Esto ocurre si tiene demasiadas unidades de productos con baja demanda y pocas unidades de productos con alta rotación. En ese caso, el problema no es solo la cantidad total de stock, sino su distribución.

Este documento tiene un enfoque exclusivamente logístico y formativo. No trata sobre indicación farmacéutica, consejo clínico, selección de tratamientos ni recomendación de medicamentos. El análisis de stock debe entenderse como una herramienta de apoyo a la gestión del inventario, no como una herramienta para tomar decisiones clínicas ni sustituir el criterio profesional.

## 2. Tipos de stock

El término stock puede tener varios significados según el contexto. Para analizar correctamente el inventario, es importante diferenciar entre stock físico, stock teórico, stock disponible, stock reservado, stock inmovilizado y stock próximo a caducar.

El stock físico es el número de unidades que realmente se encuentran en la farmacia o en el almacén en un momento determinado. Es el stock que se puede contar manualmente. El stock teórico es el que aparece registrado en el sistema informático. En condiciones ideales, el stock físico y el stock teórico deberían coincidir, pero en la práctica pueden aparecer diferencias por errores de registro, movimientos mal introducidos, recuentos pendientes, devoluciones, anulaciones o ajustes manuales.

El stock disponible es el stock que puede utilizarse realmente para cubrir la demanda. Puede diferir del stock físico si existen unidades reservadas, bloqueadas, deterioradas, próximas a caducar o pendientes de revisión. El stock reservado o comprometido hace referencia a unidades que existen, pero que no deberían considerarse libres para una nueva salida. El stock inmovilizado es aquel que permanece en inventario durante mucho tiempo sin salida suficiente. El stock caducado o próximo a caducar debe analizarse de forma separada porque puede no ser útil para cubrir demanda futura.

Ejemplo sencillo: si el sistema indica que hay 12 unidades de un producto, pero al revisar el cajón solo aparecen 9, existe un descuadre entre stock teórico y stock físico. Si además 2 unidades están apartadas por revisión de caducidad, el stock disponible real podría ser menor que el stock físico.

El límite principal de este concepto es que el dato de stock solo es útil si se entiende su origen y calidad. Un sistema puede mostrar una cifra exacta, pero esa cifra puede no reflejar la realidad si no se han registrado correctamente ventas, compras, recuentos o modificaciones manuales. Por eso, ante productos críticos o con descuadres frecuentes, puede ser necesario revisar físicamente el inventario antes de tomar decisiones.

## 3. Rotación de stock

La rotación de stock describe la velocidad con la que un producto sale del inventario durante un periodo determinado. Un producto de alta rotación es aquel que se vende o se mueve con frecuencia. Un producto de baja rotación es aquel que se vende poco o permanece durante mucho tiempo en el inventario.

En farmacia comunitaria, la rotación permite diferenciar productos de uso frecuente frente a productos de salida ocasional. Esta métrica es útil para priorizar revisiones, ajustar mínimos y detectar productos que pueden estar inmovilizando recursos. Sin embargo, la rotación no debe interpretarse de forma aislada. Un producto puede tener alta rotación, pero bajo margen; o baja rotación, pero ser importante por otros criterios logísticos o de servicio. También puede haber productos con rotación estacional, cuya salida cambia mucho según la época del año.

La rotación suele analizarse a partir de las unidades vendidas o movidas durante un periodo concreto: por ejemplo, los últimos 30 días, los últimos 90 días o el último año. Cuanto más corto sea el periodo, más sensible será el dato a cambios recientes. Cuanto más largo sea el periodo, más estable será la visión general, pero puede ocultar cambios recientes de demanda.

Ejemplo sencillo: si un producto vende 100 unidades al mes y otro vende 3 unidades al mes, el primero tiene una rotación claramente superior. Sin embargo, antes de decidir una reposición habría que revisar también el stock actual, la cobertura, el plazo de reposición, la regularidad de la demanda y el riesgo de caducidad.

El límite de la rotación es que no explica por sí sola cuánto stock conviene tener. La rotación indica velocidad de salida, pero no determina automáticamente la cantidad óptima de inventario. Para tomar decisiones más completas debe combinarse con cobertura, punto de pedido, demanda histórica, clasificación ABC/XYZ y revisión humana.

## 4. Cobertura de stock

La cobertura de stock indica durante cuánto tiempo podría mantenerse la demanda con el stock actual disponible. Normalmente se expresa en días, semanas o meses. Es una métrica muy útil porque conecta dos datos: cuántas unidades hay y cuántas unidades se consumen o venden de media en un periodo determinado.

De forma conceptual, si la demanda se mide por día, la cobertura aproximada puede expresarse así:

```text
Cobertura aproximada = stock disponible / demanda media por día
```

Por ejemplo, si se mide la demanda diaria, la cobertura se expresa en días. Si se mide la demanda semanal, la cobertura puede expresarse en semanas. La cobertura permite detectar situaciones de riesgo: una cobertura muy baja puede indicar posible rotura, mientras que una cobertura excesivamente alta puede indicar sobrestock.

En farmacia comunitaria, la cobertura debe interpretarse siempre junto al plazo de reposición. No es lo mismo tener 5 días de cobertura si el producto llega en 24 horas que si tarda 10 días en reponerse. También debe tenerse en cuenta si la demanda es estable o irregular. Una cobertura aparentemente suficiente puede no serlo si la demanda aumenta bruscamente o si existen retrasos de suministro.

Ejemplo sencillo: si un producto tiene 20 unidades disponibles y se venden de media 2 unidades al día, la cobertura aproximada es de 10 días. Si el plazo habitual de reposición es de 2 días, puede ser una situación cómoda. Si el plazo de reposición es de 12 días, podría existir riesgo de rotura antes de recibir nuevas unidades.

El principal límite de la cobertura es que depende de la demanda media utilizada. Si la demanda media está mal calculada, si el periodo elegido no es representativo o si hay estacionalidad, la cobertura puede inducir a error. Por eso, cuando se analizan productos con demanda irregular, campañas o cambios recientes de comportamiento, la cobertura debe revisarse con cautela.

## 5. Stock mínimo, stock máximo y stock de seguridad

El stock mínimo es el nivel mínimo de inventario que se considera necesario para cubrir la demanda habitual sin entrar en una situación de riesgo. No debe confundirse con el stock de seguridad, aunque ambos conceptos están relacionados. El stock mínimo suele representar un umbral operativo: si el stock baja demasiado, conviene revisar la reposición.

El stock máximo es el nivel superior que se considera razonable para evitar exceso de inventario. Sirve para reducir el riesgo de sobrestock, caducidad y acumulación innecesaria de unidades. El stock máximo no tiene por qué ser igual para todos los productos. Debe depender de la rotación, la demanda, el espacio disponible, el coste, la caducidad y el plazo de reposición.

El stock de seguridad es un colchón adicional destinado a cubrir incertidumbre. Puede ser útil cuando la demanda no es completamente estable, cuando el proveedor puede retrasarse, cuando el producto tiene importancia operativa o cuando se quiere reducir el riesgo de rotura. Un producto de demanda estable y reposición rápida puede necesitar poco stock de seguridad. Un producto con demanda irregular o reposición lenta puede necesitar un margen mayor.

Ejemplo sencillo: un producto con venta estable de 1 unidad diaria y reposición en 24-48 horas puede funcionar con un mínimo bajo. En cambio, un producto que se vende de forma irregular y tarda una semana en llegar puede necesitar un nivel de seguridad más alto para evitar quedarse sin existencias entre pedidos.

El límite de estos valores es que no deberían configurarse una vez y olvidarse. El stock mínimo, máximo y de seguridad deben revisarse periódicamente. Cambios en la demanda, estacionalidad, caducidad, campañas, incidencias de suministro o cambios en los hábitos de compra pueden hacer que los valores anteriores dejen de ser adecuados.

## 6. Punto de pedido

El punto de pedido es el nivel de stock a partir del cual conviene lanzar o revisar una reposición. Su función es anticiparse a la rotura, teniendo en cuenta que entre el momento en que se detecta la necesidad de comprar y el momento en que el producto llega puede pasar un tiempo.

De forma conceptual, el punto de pedido depende de tres elementos principales: la demanda media, el plazo de reposición y el stock de seguridad. Si un producto se vende mucho durante el tiempo que tarda en llegar, el punto de pedido deberá ser más alto. Si el producto llega muy rápido y su demanda es estable, el punto de pedido puede ser más bajo.

La fórmula conceptual puede expresarse así:

```text
Punto de pedido orientativo = demanda media durante el plazo de reposición + stock de seguridad
```

En farmacia comunitaria, el punto de pedido ayuda a evitar decisiones reactivas. En lugar de esperar a que el stock llegue a cero, permite actuar antes. Sin embargo, debe adaptarse al comportamiento de cada producto. No todos los productos necesitan el mismo punto de pedido, ni todos deben reponerse con la misma frecuencia.

Ejemplo sencillo: si un producto vende de media 3 unidades al día y tarda 4 días en llegar, durante el plazo de reposición podrían venderse unas 12 unidades. Si además se quiere mantener un pequeño margen de seguridad, el punto de pedido debería estar por encima de esas 12 unidades. Este ejemplo es conceptual y no debe interpretarse como una regla universal.

El límite principal es que el punto de pedido no puede calcularse bien si faltan datos. Si no se conoce la demanda media, el plazo de reposición, el stock actual o la variabilidad de la demanda, el agente no debe inventar una cifra. En ese caso, debe explicar qué información falta y ofrecer una orientación general.

## 7. Roturas de stock

Una rotura de stock se produce cuando un producto no está disponible para cubrir una demanda que aparece. Puede ser una rotura real, cuando el stock físico es cero, o una situación de riesgo de rotura, cuando la cobertura es tan baja que probablemente no alcanzará hasta la siguiente reposición.

Las roturas pueden tener varias causas. Algunas se deben a una demanda superior a la prevista. Otras aparecen porque el punto de pedido está mal definido, porque el stock mínimo es demasiado bajo, porque el plazo de reposición es mayor de lo habitual, porque no se registraron bien los movimientos o porque hubo un descuadre entre stock teórico y stock físico. También pueden existir problemas externos de suministro que no dependen directamente de la farmacia.

En el análisis de inventario, no interesa únicamente detectar roturas cuando ya han ocurrido. Lo más útil es identificar señales tempranas. Una cobertura inferior al plazo de reposición, un producto de alta rotación con pocas unidades disponibles o una demanda reciente en aumento pueden indicar que conviene revisar el producto.

Ejemplo sencillo: si un producto tiene 4 unidades disponibles, vende de media 2 unidades al día y tarda 5 días en reponerse, la cobertura aproximada es de 2 días. Como el plazo de reposición es superior a la cobertura, existe riesgo de rotura antes de recibir nuevas unidades.

El límite del análisis es que una posible rotura no implica automáticamente una compra concreta. Para proponer una reposición razonable habría que conocer más datos: demanda histórica, stock actual fiable, plazo de entrega, stock de seguridad, caducidad, clasificación del producto y posibles incidencias de suministro. El agente debe limitarse a explicar el riesgo y los criterios de revisión.

## 8. Sobrestock

El sobrestock se produce cuando la cantidad disponible de un producto es superior a la que resulta razonable según su demanda, rotación, caducidad, espacio ocupado y plazo de reposición. No significa simplemente “tener muchas unidades”, sino tener más unidades de las necesarias para el comportamiento esperado del producto.

En farmacia comunitaria, el sobrestock puede generar varios problemas. Puede inmovilizar recursos, ocupar espacio, aumentar el riesgo de caducidad y dificultar la gestión del almacén. Además, puede ocultar otros problemas: puede existir mucho inventario acumulado en productos de baja salida mientras faltan productos de alta demanda.

El sobrestock suele detectarse al combinar stock actual y cobertura. Un producto con cobertura muy elevada debe revisarse, especialmente si tiene baja rotación o fecha de caducidad próxima. También puede aparecer sobrestock por compras excesivas, promociones mal ajustadas, errores de previsión, cambios de demanda o falta de revisión de mínimos y máximos.

Ejemplo sencillo: si un producto tiene 60 unidades disponibles y vende una unidad cada dos meses, la cobertura es muy alta. Aunque no haya riesgo inmediato de rotura, puede existir riesgo de inmovilizado y caducidad, especialmente si no hay una razón clara para mantener ese volumen.

El límite es que una cobertura alta no siempre es negativa. Puede haber productos con demanda estacional, compras planificadas para campañas o situaciones concretas donde se justifique un stock superior. Por eso, el agente no debe concluir automáticamente que todo stock alto es incorrecto. Debe indicar que conviene revisar demanda, caducidad, contexto y motivo de acumulación.

## 9. Límites del análisis de stock

El análisis de stock es una herramienta de apoyo, no un sistema autónomo de decisión. Sus resultados dependen de la calidad de los datos disponibles, de la correcta interpretación de los movimientos y del contexto operativo de la farmacia. Por tanto, las métricas deben ayudar a revisar y priorizar, pero no sustituir la supervisión humana.

Existen situaciones en las que el análisis puede ser incompleto. Por ejemplo, si no se conoce el plazo de reposición, no puede calcularse bien el punto de pedido. Si el stock teórico no coincide con el físico, la cobertura puede ser incorrecta. Si el producto tiene demanda estacional, una media simple puede ser engañosa. Si hay problemas de suministro, la reposición puede no depender solo de la demanda.

También hay productos cuyo comportamiento no se explica bien con una única métrica. Un producto puede tener baja rotación, pero ser necesario por criterios logísticos o de disponibilidad. Otro puede tener alta rotación, pero no requerir mucho stock si se repone muy rápido. Otro puede tener demanda irregular y necesitar revisión manual aunque su media de ventas parezca baja.

Ejemplo sencillo: si se pregunta “¿cuánto debería comprar de este producto?” pero solo se aporta el stock actual, el análisis es insuficiente. Para responder con mayor seguridad harían falta ventas recientes, demanda histórica, plazo de reposición, stock de seguridad, caducidad y criterio de priorización.

FarmaStock AI debe respetar estos límites. No debe dar consejo clínico, recomendar tratamientos, identificar personas usuarias, usar datos reales sensibles ni tomar decisiones automáticas de compra. Si el contexto recuperado no contiene información suficiente, debe indicarlo claramente. Su función es explicar conceptos, señalar riesgos, ayudar a interpretar métricas y orientar la revisión del inventario desde una perspectiva logística y formativa.

## 10. Preguntas que puede responder este documento

Este documento permite responder preguntas generales sobre los fundamentos de la gestión de stock en farmacia comunitaria. Está pensado para que un sistema RAG pueda recuperar definiciones, explicaciones aplicadas, ejemplos y límites de uso relacionados con inventario, rotación, cobertura, mínimos, punto de pedido, roturas y sobrestock.

Preguntas que puede responder:

- ¿Qué diferencia hay entre rotación y cobertura de stock?
- ¿Qué es el stock de seguridad?
- ¿Qué diferencia hay entre stock mínimo y punto de pedido?
- ¿Qué significa tener riesgo de rotura?
- ¿Qué es el sobrestock?
- ¿Por qué una cobertura alta no siempre es negativa?
- ¿Qué datos faltan para recomendar una reposición?
- ¿Qué diferencia hay entre stock físico, stock teórico y stock disponible?
- ¿Por qué un producto de alta rotación puede quedarse sin stock?
- ¿Por qué un producto con muchas unidades disponibles puede ser un problema?
- ¿Cuándo debería revisarse el stock mínimo de un producto?
- ¿Por qué el análisis de stock no debe sustituir la revisión humana?