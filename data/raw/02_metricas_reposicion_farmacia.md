---
title: "Métricas de reposición y criterios de revisión en farmacia comunitaria"
document_id: "02_metricas_reposicion_farmacia"
version: "1.0"
domain: "Optimización de stock en farmacia comunitaria"
use_in_rag: true
contains_real_data: false
---

# Métricas de reposición y criterios de revisión en farmacia comunitaria

## 1. Introducción a las métricas de reposición

Las métricas de reposición son indicadores que ayudan a interpretar el estado del inventario y a decidir qué productos deben revisarse con mayor prioridad. En una farmacia comunitaria, estas métricas permiten analizar si el stock disponible es suficiente, si existe riesgo de rotura, si hay exceso de unidades o si los niveles configurados necesitan una revisión.

Una métrica no es una decisión automática. Una cifra aislada, como “quedan 5 unidades”, no permite saber si la situación es adecuada o preocupante. Para interpretar correctamente ese dato hay que relacionarlo con la demanda histórica, la venta media, la cobertura, el plazo de reposición, el stock de seguridad, la caducidad, la regularidad de la demanda y la importancia logística del producto.

Las métricas de reposición sirven para pasar de una revisión intuitiva a una revisión más estructurada. No eliminan la necesidad de criterio profesional, pero ayudan a priorizar. Por ejemplo, si hay cientos o miles de referencias, no todas pueden revisarse con la misma intensidad. Tiene sentido prestar más atención a productos con alta rotación y baja cobertura, productos con riesgo de caducidad, productos con descuadres frecuentes o productos con demanda irregular.

Ejemplo sencillo: dos productos pueden tener 6 unidades disponibles. En el primero se vende una unidad al mes, por lo que el stock puede ser suficiente durante bastante tiempo. En el segundo se venden 3 unidades al día, por lo que esas 6 unidades pueden agotarse en poco tiempo. El dato de stock es el mismo, pero la interpretación es completamente diferente.

El límite principal de las métricas es que dependen de la calidad de los datos. Si las ventas no están bien registradas, si el stock teórico no coincide con el físico o si se desconoce el plazo de reposición, las conclusiones pueden ser incompletas. FarmaStock AI debe usar las métricas como apoyo analítico, no como una herramienta para ordenar compras automáticas.

## 2. Demanda histórica

La demanda histórica es el comportamiento de salida de un producto durante un periodo pasado. Normalmente se analiza a partir de unidades vendidas o movimientos de salida registrados en el sistema. Es una de las bases más importantes para estimar si el stock actual será suficiente en el futuro.

En farmacia comunitaria, la demanda histórica puede analizarse con distintos horizontes temporales. Un periodo corto, como los últimos 7 o 30 días, permite detectar cambios recientes. Un periodo intermedio, como 90 días, ofrece una visión más estable. Un periodo largo, como 12 meses, permite observar estacionalidad, campañas o cambios de comportamiento a lo largo del año.

La demanda histórica no debe interpretarse de forma mecánica. Hay productos con demanda estable, productos con demanda estacional, productos de venta intermitente y productos que sufren picos puntuales. También puede haber productos nuevos sin histórico suficiente. En esos casos, la media histórica puede ser poco representativa y debe complementarse con revisión manual.

Ejemplo sencillo: un producto relacionado con una campaña estacional puede vender muy poco durante varios meses y concentrar muchas ventas en una época concreta. Si se calcula su demanda solo a partir de un periodo fuera de campaña, puede parecer que no necesita stock. Si se calcula únicamente durante la campaña, puede parecer que necesita demasiado stock el resto del año.

La advertencia principal es que la demanda histórica describe lo que ocurrió, no garantiza lo que ocurrirá. Sirve para orientar, pero no debe sustituir la revisión del contexto. Si hubo promociones, cambios de ubicación, incidencias de suministro, sustituciones de producto o errores de registro, la demanda histórica puede estar distorsionada.

## 3. Venta media diaria, semanal y mensual

La venta media es una forma sencilla de resumir la demanda de un producto durante un periodo. Puede calcularse por día, por semana o por mes. Su utilidad depende del tipo de producto y del nivel de detalle que se necesite para la revisión.

La venta media diaria suele ser útil para productos de alta rotación o productos que se revisan con frecuencia. Permite estimar cuántas unidades salen cada día y facilita el cálculo de cobertura en días. La venta media semanal puede ser más adecuada para productos con salida moderada, donde una visión diaria puede ser demasiado variable. La venta media mensual puede servir para productos de baja rotación, productos estacionales o revisiones más generales.

Las fórmulas conceptuales pueden expresarse así:

```text
Venta media diaria = unidades vendidas en el periodo / número de días del periodo
```

```text
Venta media semanal = unidades vendidas en el periodo / número de semanas del periodo
```

```text
Venta media mensual = unidades vendidas en el periodo / número de meses del periodo
```

Ejemplo sencillo: si un producto ha vendido 60 unidades en 30 días, su venta media diaria aproximada es de 2 unidades al día. Si otro producto ha vendido 8 unidades en 8 semanas, su venta media semanal aproximada es de 1 unidad por semana.

La limitación principal de la media es que puede ocultar irregularidad. Un producto puede vender 30 unidades en un mes, pero concentrar todas las ventas en dos días. En ese caso, la media diaria parece estable, pero el comportamiento real no lo es. Por eso, la venta media debe interpretarse junto con la regularidad de la demanda, la clasificación XYZ, la estacionalidad y la existencia de picos anómalos.

## 4. Cobertura en días

La cobertura en días indica cuántos días podría mantenerse la demanda con el stock disponible actual. Es una métrica especialmente útil porque permite convertir el stock en tiempo estimado de disponibilidad. No solo responde a la pregunta “¿cuántas unidades quedan?”, sino también a “¿cuánto tiempo podrían durar esas unidades según la demanda media?”.

La fórmula conceptual es:

```text
Cobertura en días = stock disponible / venta media diaria
```

Si la venta media diaria es muy baja o igual a cero, la cobertura debe interpretarse con precaución. En productos de baja rotación, la fórmula puede generar coberturas muy altas que no siempre tienen significado operativo claro. En esos casos, puede ser más útil revisar ventas mensuales, fecha de última venta, caducidad y stock inmovilizado.

Ejemplo sencillo: si un producto tiene 24 unidades disponibles y una venta media diaria de 3 unidades, su cobertura aproximada es de 8 días. Si el plazo de reposición habitual es de 2 días, la situación puede ser razonable. Si el plazo de reposición es de 10 días, puede existir riesgo de rotura antes de recibir nuevas unidades.

La cobertura también permite detectar posibles excesos. Si un producto tiene una cobertura de 300 días y no hay una razón logística que lo justifique, puede ser candidato a revisión por sobrestock. Sin embargo, una cobertura alta no siempre es negativa. Puede estar justificada por campañas, compras planificadas, vida útil larga o dificultad de reposición.

El límite principal es que la cobertura depende de la venta media utilizada. Si el periodo de cálculo no es representativo, la cobertura tampoco lo será. FarmaStock AI debe explicar la cobertura como una estimación, no como una certeza.

## 5. Lead time o plazo de reposición

El lead time o plazo de reposición es el tiempo que transcurre entre la detección de la necesidad de reponer y la disponibilidad real del producto en el inventario. Puede incluir el tiempo de preparación del pedido, envío, recepción, registro y colocación del producto.

En farmacia comunitaria, el plazo de reposición es clave para interpretar el riesgo de rotura. Un producto con cobertura de 4 días puede estar en una situación cómoda si se repone en 24 horas. Ese mismo producto puede estar en riesgo si tarda una semana en llegar. Por tanto, no basta con saber cuánto stock queda: también hay que saber cuánto tiempo tarda en recuperarse el nivel de inventario.

El lead time puede ser estable o variable. Algunos productos pueden reponerse de forma rápida y frecuente. Otros pueden depender de disponibilidad irregular, pedidos especiales, campañas o incidencias de suministro. Si el plazo de reposición es variable, puede ser necesario aumentar el stock de seguridad o revisar el punto de pedido.

Ejemplo sencillo: dos productos venden una media de 2 unidades al día y tienen 10 unidades disponibles. Ambos tienen una cobertura aproximada de 5 días. Si el primer producto se repone en 1 día y el segundo en 7 días, el segundo tiene una situación de riesgo mucho mayor.

El límite principal es que muchas veces el lead time no está registrado de forma explícita o puede variar según el momento. Si el agente no conoce el plazo de reposición, no debe calcular un punto de pedido cerrado. Debe indicar que falta ese dato y explicar cómo afectaría al análisis.

## 6. Punto de pedido aplicado

El punto de pedido es el nivel de stock a partir del cual conviene lanzar o revisar una reposición. Su finalidad es evitar que el producto se agote durante el tiempo que tarda en llegar la reposición. A diferencia del stock mínimo, que puede funcionar como umbral general, el punto de pedido se basa en la demanda durante el plazo de reposición y en un posible stock de seguridad.

La fórmula conceptual es:

```text
Punto de pedido orientativo = demanda media durante el plazo de reposición + stock de seguridad
```

La demanda media durante el plazo de reposición puede calcularse de forma aproximada así:

```text
Demanda durante el plazo de reposición = venta media diaria × lead time en días
```

Ejemplo sencillo: si un producto vende de media 2 unidades al día y el plazo de reposición es de 5 días, la demanda esperada durante ese plazo sería de 10 unidades. Si se añade un stock de seguridad de 4 unidades, el punto de pedido orientativo sería de 14 unidades.

En farmacia comunitaria, el punto de pedido aplicado debe ajustarse según el tipo de producto. Productos de alta rotación, demanda estable y reposición rápida pueden tener puntos de pedido más ajustados. Productos con demanda irregular, reposición lenta o mayor impacto operativo pueden necesitar un margen de seguridad superior.

La advertencia principal es que el punto de pedido no debe aplicarse como fórmula rígida. Si la demanda media está distorsionada, si el producto es estacional, si hay problemas de suministro o si el stock registrado no es fiable, el cálculo puede ser insuficiente. FarmaStock AI puede explicar el criterio y la fórmula, pero no debe inventar cantidades ni tomar decisiones automáticas de compra.

## 7. Detección de riesgo de rotura

El riesgo de rotura aparece cuando existe una probabilidad relevante de que el producto no esté disponible antes de la siguiente reposición. No es necesario que el stock sea cero para hablar de riesgo. Puede haber riesgo aunque todavía queden unidades, si la cobertura es inferior al plazo de reposición o si la demanda reciente está aumentando.

Las señales más habituales de riesgo de rotura son: stock disponible bajo, cobertura inferior al lead time, aumento reciente de ventas, producto de alta rotación, demanda más variable de lo habitual, retrasos de reposición, descuadres frecuentes o mínimos mal configurados.

Un criterio conceptual sencillo es:

```text
Riesgo de rotura probable = cobertura en días < lead time en días
```

Este criterio no debe utilizarse de forma aislada, pero sirve como alerta inicial. Si la cobertura es menor que el tiempo necesario para reponer, el producto podría agotarse antes de recibir nuevas unidades.

Ejemplo sencillo: un producto tiene 6 unidades disponibles, una venta media diaria de 2 unidades y un lead time de 5 días. Su cobertura aproximada es de 3 días. Como 3 días de cobertura son menos que 5 días de reposición, existe riesgo de rotura si no se revisa la reposición.

La limitación principal es que el riesgo de rotura no equivale automáticamente a una cantidad concreta de compra. Para estimar una reposición sería necesario conocer demanda histórica, stock actual fiable, lead time, stock de seguridad, posible estacionalidad, caducidad y clasificación del producto. Si falta información, el agente debe señalar el riesgo y pedir los datos necesarios.

El riesgo debe interpretarse con más prioridad cuando el producto tiene alta importancia operativa, alta rotación o difícil reposición.

## 8. Detección de sobrestock

El sobrestock aparece cuando hay más unidades disponibles de las razonables según la demanda, la rotación, la caducidad, el espacio ocupado y el plazo de reposición. A diferencia de la rotura, el sobrestock no siempre se percibe como un problema inmediato, pero puede afectar a la eficiencia del inventario.

Las señales habituales de sobrestock son: cobertura muy alta, baja rotación, muchas unidades sin salida reciente, productos con fecha de caducidad próxima, compras excesivas, acumulación tras campañas, mínimos demasiado altos o falta de revisión periódica. También puede haber sobrestock si se mantienen muchas unidades por inercia, aunque la demanda haya disminuido.

Un criterio conceptual sencillo es:

```text
Posible sobrestock = cobertura muy superior al periodo razonable de revisión
```

El periodo razonable de revisión depende del tipo de producto. No puede fijarse un único valor válido para todos. Un producto de alta rotación puede necesitar más unidades que uno de baja rotación. Un producto de demanda estacional puede tener cobertura alta antes de una campaña. Un producto con reposición difícil puede justificar mayor inventario.

Ejemplo sencillo: si un producto tiene 80 unidades disponibles y vende 2 unidades al mes, la cobertura aproximada es muy elevada. Si no existe una campaña prevista, una justificación logística o una vida útil suficientemente larga, puede ser candidato a revisión por sobrestock.

La advertencia principal es que una cobertura alta no debe clasificarse automáticamente como error. Puede estar justificada en algunos casos. FarmaStock AI debe proponer revisión, no dictar una conclusión cerrada. Conviene revisar demanda, caducidad, motivo de acumulación, comportamiento histórico y política de stock.

## 9. Priorización de revisión manual

La priorización de revisión manual consiste en decidir qué productos deben revisarse antes cuando no es posible analizar todo el inventario con la misma profundidad. En una farmacia comunitaria, esta priorización es importante porque el número de referencias puede ser elevado y los productos no tienen el mismo impacto operativo ni el mismo comportamiento de demanda.

Los productos que suelen requerir revisión prioritaria son aquellos con alta rotación y baja cobertura, productos con cobertura inferior al lead time, productos con muchas unidades y baja salida, productos con caducidad próxima, productos con descuadres frecuentes, productos con modificaciones manuales repetidas y productos con demanda irregular.

Una priorización básica puede organizarse así:

```text
Prioridad alta = alta rotación + baja cobertura + lead time relevante
```

```text
Prioridad por exceso = baja rotación + cobertura muy alta + riesgo de caducidad o inmovilizado
```

La revisión manual no debe centrarse solo en productos con riesgo de rotura. También es importante revisar productos que consumen espacio, inmovilizan recursos o pueden caducar. Una buena gestión de stock busca equilibrio: evitar faltas de producto, pero también evitar acumulaciones innecesarias.

Ejemplo sencillo: en una revisión diaria, puede ser más urgente revisar un producto que vende 5 unidades al día y tiene cobertura de 2 días que un producto que vende 1 unidad al mes y tiene cobertura de 40 días. En una revisión de sobrestock, en cambio, el segundo puede ser más interesante si tiene muchas unidades y baja salida.

El límite principal es que la priorización depende del objetivo de la revisión. No se prioriza igual una revisión para evitar roturas que una revisión para reducir inmovilizado. El agente debe aclarar el criterio usado antes de ordenar o comparar productos.

## 10. Datos necesarios antes de recomendar reposición

Antes de recomendar una reposición, es necesario reunir un conjunto mínimo de datos. Sin esta información, cualquier recomendación cuantitativa puede ser poco fiable. FarmaStock AI debe ser especialmente cuidadoso en este punto: puede explicar qué revisar, pero no debe inventar cantidades ni asumir datos no disponibles.

Los datos más importantes son: stock disponible, stock físico si hay dudas, ventas recientes, demanda histórica, venta media diaria o semanal, lead time, stock de seguridad, punto de pedido actual, stock mínimo configurado, regularidad de la demanda, posible estacionalidad, fecha de caducidad, incidencias de suministro y clasificación ABC/XYZ si está disponible.

También es importante conocer el objetivo de la reposición. No es lo mismo reponer para cubrir demanda inmediata, ajustar un mínimo, preparar una campaña, reducir una rotura recurrente o corregir un descuadre. La recomendación depende del problema que se quiere resolver.

Ejemplo sencillo: si solo se sabe que quedan 3 unidades, no se puede recomendar una compra responsable. Si además se sabe que se venden 2 unidades al día, que el producto tarda 4 días en llegar y que se quiere mantener un stock de seguridad de 2 unidades, ya se puede razonar mejor sobre el punto de pedido y el riesgo de rotura.

Un esquema mínimo de datos podría ser:

```text
Datos mínimos = stock disponible + demanda media + lead time + criterio de seguridad
```

La advertencia principal es que la reposición no debe automatizarse solo con una fórmula. Hay que revisar la calidad del dato, la caducidad, la variabilidad de la demanda, el contexto operativo y posibles incidencias. Si falta información, el agente debe responder indicando qué dato falta y por qué es necesario.

## 11. Preguntas que puede responder este documento

Este documento permite responder preguntas sobre métricas de reposición, criterios de revisión, demanda histórica, cobertura, lead time, punto de pedido, riesgo de rotura y sobrestock. Está diseñado para que un sistema RAG pueda recuperar explicaciones técnicas, fórmulas conceptuales, ejemplos y límites de uso relacionados con la reposición en farmacia comunitaria.

Preguntas que puede responder:

- ¿Qué son las métricas de reposición?
- ¿Por qué no basta con saber cuántas unidades quedan?
- ¿Qué es la demanda histórica?
- ¿Qué periodo conviene revisar para analizar la demanda?
- ¿Cómo se calcula la venta media diaria?
- ¿Cuándo es mejor usar venta media semanal o mensual?
- ¿Cómo se calcula la cobertura en días?
- ¿Qué significa que la cobertura sea menor que el plazo de reposición?
- ¿Qué es el lead time?
- ¿Cómo afecta el lead time al riesgo de rotura?
- ¿Cómo se calcula un punto de pedido orientativo?
- ¿Qué datos necesito para calcular el punto de pedido?
- ¿Cómo puedo detectar un producto con riesgo de rotura?
- ¿Qué señales indican posible sobrestock?
- ¿Por qué una cobertura alta no siempre significa un problema?
- ¿Qué productos debería revisar primero?
- ¿Qué diferencia hay entre priorizar por riesgo de rotura y priorizar por sobrestock?
- ¿Qué datos faltan antes de recomendar una reposición?
- ¿Por qué FarmaStock AI no debe inventar cantidades de compra?
- ¿Por qué las métricas no sustituyen la revisión humana?