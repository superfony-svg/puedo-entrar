"""Contenido de las guías (web/guias/<slug>/). Lo usa build_paginas.py.

Cada guía: slug, titulo (h1), title (pestaña y Google), desc (meta description),
revisado (fecha ISO), cuerpo (HTML con secciones) y faq (preguntas para Google).
Mantener el tono: frases cortas, claro, y avisar cuando algo depende del ayuntamiento.
"""

RECURRIR = {
    "slug": "recurrir-multa-zbe",
    "titulo": "Cómo recurrir una multa de la zona de bajas emisiones",
    "title": "Recurrir una multa de la ZBE: plazos, motivos y pasos (2026)",
    "desc": "Cómo recurrir una multa por entrar en una zona de bajas emisiones: plazos, pronto pago, motivos que funcionan, pasos y el caso de Málaga, donde se devuelven las multas.",
    "revisado": "2026-11-24",
    "cuerpo": """
<section class="card"><h2>¿Cómo sé si tengo una multa?</h2>
<ul>
<li><strong>Por correo certificado</strong> a la dirección que tiene la DGT de tu coche. Si cambiaste de casa, actualízala en la DGT.</li>
<li><strong>En la Dirección Electrónica Vial (DEV)</strong>, el buzón de multas de la DGT. Si te diste de alta, las multas llegan solo ahí y cuentan como recibidas aunque no las abras. Se mira en la sede de la DGT o en la app miDGT.</li>
<li><strong>En el TESTRA</strong> (Tablón Edictal de Sanciones de Tráfico), que es donde se publican las multas que no se han podido entregar. Puedes buscar tu DNI o matrícula en la sede de la DGT.</li>
</ul>
<p><strong>Cuidado con las estafas:</strong> los ayuntamientos no dejan códigos QR en el parabrisas para pagar multas de la zona de bajas emisiones ni las cobran por SMS o WhatsApp con un enlace. Si te llega algo así, no pagues: entra tú en la sede electrónica del ayuntamiento.</p></section>

<section class="card"><h2>Lo primero: ¿pagar o recurrir?</h2>
<p>Tienes dos caminos y no puedes hacer los dos:</p>
<ul>
<li><strong>Pagar con descuento.</strong> Si pagas en los <strong>20 días naturales</strong> siguientes a la notificación, en la mayoría de ciudades la multa baja a la mitad (de 200 € a 100 €). Pagando así renuncias a presentar alegaciones.</li>
<li><strong>Recurrir.</strong> Si crees que la multa es injusta, presenta alegaciones en esos mismos 20 días naturales. Si te las rechazan, pagarás la multa entera, sin descuento.</li>
</ul>
<p class="muted">Recurre solo si tienes un motivo claro (los de abajo). Si no, el descuento suele salir mejor.</p></section>

<section class="card"><h2>Motivos que suelen funcionar</h2>
<ul>
<li><strong>Tu coche sí podía entrar.</strong> Comprueba tu etiqueta con tu matrícula en <a href="../../">nuestro buscador</a>. Si tu etiqueta estaba permitida, aporta la captura y la ficha técnica.</li>
<li><strong>Tenías una excepción o permiso:</strong> vehículo histórico, tarjeta de movilidad reducida, residente, parking dentro de la zona, invitación de un vecino… Aporta el justificante.</li>
<li><strong>Error en los datos:</strong> matrícula mal leída por la cámara, marca o modelo que no coincide, calle o fecha equivocadas.</li>
<li><strong>Señalización:</strong> no había señal de entrada a la zona o no se veía.</li>
<li><strong>Notificación fuera de plazo.</strong> Las infracciones graves de tráfico prescriben a los 6 meses.</li>
<li><strong>La norma fue anulada</strong> por un tribunal, como en Málaga (ver abajo).</li>
</ul></section>

<section class="card"><h2>Paso a paso</h2>
<ol>
<li><strong>Lee bien la notificación:</strong> fecha, hora, lugar, matrícula y la norma que dice que incumpliste.</li>
<li><strong>Reúne pruebas:</strong> tu etiqueta, fotos de la zona, el permiso o la tarjeta que tuvieras.</li>
<li><strong>Presenta alegaciones</strong> en 20 días naturales, en la sede electrónica del ayuntamiento (con certificado digital o Cl@ve) o en un registro presencial. Indica el número de expediente.</li>
<li><strong>Si no respondes ni pagas</strong>, la denuncia se convierte en sanción firme pasados unos 30 días naturales.</li>
<li><strong>Si te rechazan las alegaciones</strong>, puedes poner un <strong>recurso de reposición</strong> en el plazo de 1 mes. Si en 1 mes no contestan, se entiende rechazado.</li>
<li><strong>Último paso: el juzgado</strong> (contencioso-administrativo). Puede costar más que la multa, así que solo merece la pena en casos claros.</li>
</ol>
<p class="muted">Los plazos son los generales de tráfico. Cada ayuntamiento puede tener detalles propios: míralos en su notificación. Esta guía es información general, no asesoramiento jurídico para tu caso.</p></section>

<section class="card"><h2>Caso Málaga: devuelven las multas</h2>
<p>El Tribunal Superior de Justicia de Andalucía anuló la regulación de la ZBE de Málaga (sentencia de 6 de mayo de 2026) por discriminatoria: los coches empadronados en Málaga estaban exentos y los de fuera no. El Ayuntamiento <strong>no pone multas desde el 14 de octubre de 2026</strong>.</p>
<ul>
<li><strong>Si tu multa está en trámite:</strong> no la pagues. Está suspendida y se anulará.</li>
<li><strong>Si ya la pagaste:</strong> se devolverá de oficio. Para cobrar, da una cuenta bancaria a tu nombre en la sede electrónica (trámite «Devolución de ingresos» de Gestión Tributaria), en una OMAC o con cita previa.</li>
<li><strong>Si te llega una notificación o un cobro</strong> pese a la suspensión, pide la anulación y no dejes pasar el plazo.</li>
</ul>
<p class="muted">Fuente: <a href="https://www.elespanol.com/malaga/20261019/malaga-devolvera-dinero-multas-zbe-tramite-hacer/1003744426101_0.html">El Español, 19/10/2026</a>. Confirma tu caso en Gestrisam (Ayuntamiento de Málaga).</p></section>
""",
    "faq": [
        ("¿Cuánto tiempo tengo para recurrir una multa de la ZBE?", "20 días naturales desde que recibes la notificación para presentar alegaciones. Si te las rechazan, 1 mes para el recurso de reposición."),
        ("¿Si recurro pierdo el descuento del 50 %?", "Sí. El descuento solo se aplica si pagas en los 20 días naturales; si presentas alegaciones y te las rechazan, pagarás la multa entera."),
        ("¿Qué motivos sirven para recurrir una multa de la ZBE?", "Que tu etiqueta sí estuviera permitida, tener una excepción o permiso, un error en la matrícula o los datos, falta de señalización, notificación fuera de plazo o que un tribunal haya anulado la norma."),
        ("¿Cómo sé si tengo una multa de una zona de bajas emisiones?", "Llega por correo certificado o, si tienes la Dirección Electrónica Vial (DEV) de la DGT, solo ahí. Las que no se pueden entregar se publican en el TESTRA, que puedes consultar en la sede de la DGT."),
        ("¿Me pueden cobrar la multa con un QR en el parabrisas o un SMS?", "No. Es una estafa conocida. Paga solo en la sede electrónica del ayuntamiento o con los datos de la notificación oficial."),
        ("¿Devuelven las multas de la ZBE de Málaga?", "Sí. Tras anular el TSJA la regulación, el Ayuntamiento dejó de multar el 14 de octubre de 2026, suspendió las multas en trámite y devolverá de oficio las pagadas."),
    ],
}

ETIQUETAS = {
    "slug": "etiquetas-dgt",
    "titulo": "Etiquetas de la DGT: qué significa cada una",
    "title": "Etiquetas ambientales de la DGT: 0, ECO, C, B y sin etiqueta explicadas",
    "desc": "Qué coches tienen etiqueta Cero, ECO, C, B o ninguna, por qué año y combustible, dónde comprar la pegatina y cómo saber la tuya con tu matrícula.",
    "revisado": "2026-11-24",
    "cuerpo": """
<section class="card"><h2>La forma más fácil de saber la tuya</h2>
<p>Escribe tu matrícula en <a href="../../">nuestro buscador</a>: te damos la etiqueta oficial de la DGT, actualizada cada día, y en qué ciudades puedes entrar.</p></section>

<section class="card"><h2>Cada etiqueta, de mejor a peor</h2>
<dl>
<dt>Cero emisiones (azul)</dt><dd>Eléctricos puros, eléctricos de autonomía extendida, híbridos enchufables con más de 40 km de autonomía eléctrica y coches de hidrógeno. Entran en todas las zonas.</dd>
<dt>ECO (azul y verde)</dt><dd>Híbridos no enchufables, híbridos enchufables con menos de 40 km eléctricos y coches de gas (GLP, GNC o GNL). Entran en casi todas las zonas.</dd>
<dt>C (verde)</dt><dd>Gasolina matriculados desde enero de 2006 y diésel desde septiembre de 2015 (en la práctica, muchos de 2014 con norma Euro 6).</dd>
<dt>B (amarilla)</dt><dd>Gasolina matriculados desde enero de 2001 y diésel desde enero de 2006.</dd>
<dt>Sin etiqueta</dt><dd>Gasolina anteriores a 2001 y diésel anteriores a 2006. Son los que más zonas tienen prohibidas.</dd>
</dl>
<p class="muted">Las fechas son orientativas: lo que cuenta es la norma Euro de tu ficha técnica. Para motos, furgonetas y camiones las fechas cambian. Por eso es mejor mirar tu matrícula.</p></section>

<section class="card"><h2>La pegatina</h2>
<ul>
<li>Se compra en Correos, en talleres y en gestorías. Cuesta unos 5 €.</li>
<li>Las cámaras leen la matrícula, no la pegatina, pero algunas ordenanzas obligan a llevarla en el parabrisas. Ponerla evita problemas.</li>
<li>Va en la esquina inferior derecha del parabrisas delantero.</li>
</ul></section>

<section class="card"><h2>¿Se puede cambiar de etiqueta?</h2>
<p>Solo si cambia el coche de verdad: por ejemplo, al pasarlo a gas (GLP) en un taller homologado y legalizarlo en la ITV puede pasar a ECO. Un filtro o una reprogramación no cambian la etiqueta.</p></section>
""",
    "faq": [
        ("¿Cómo sé qué etiqueta tiene mi coche?", "Escribe tu matrícula en el buscador de ¿Puedo entrar?: muestra la etiqueta oficial de la DGT, actualizada cada día."),
        ("¿Qué coches tienen etiqueta C?", "Los de gasolina matriculados desde enero de 2006 y los diésel desde septiembre de 2015, aproximadamente (norma Euro 4 o superior en gasolina y Euro 6 en diésel)."),
        ("¿Qué coches tienen etiqueta B?", "Los de gasolina matriculados desde enero de 2001 y los diésel desde enero de 2006, aproximadamente."),
        ("¿Es obligatorio llevar la pegatina?", "Las cámaras leen la matrícula, pero algunas ordenanzas municipales obligan a llevarla visible. Cuesta unos 5 € en Correos, talleres y gestorías."),
    ],
}

HISTORICOS = {
    "slug": "vehiculos-historicos",
    "titulo": "Vehículos históricos y zonas de bajas emisiones",
    "title": "¿Pueden entrar los coches históricos en la ZBE? Norma por ciudad",
    "desc": "Los coches y motos históricos no siempre están exentos de las zonas de bajas emisiones. Qué dice cada ciudad, qué hay que registrar y cómo comprobarlo.",
    "revisado": "2026-11-24",
    "cuerpo": """
<section class="card"><h2>Resumen</h2>
<p>Un vehículo histórico suele salir <strong>sin etiqueta</strong> en la DGT, porque es antiguo. Si puede entrar o no en una ZBE <strong>lo decide cada ayuntamiento</strong> en su ordenanza, y las normas cambian mucho:</p>
<ul>
<li>En algunas ciudades están exentos sin más.</li>
<li>En otras hay que registrar la matrícula antes de entrar.</li>
<li>En otras solo pueden entrar unos días al año con permiso. Por ejemplo, en <a href="../../zbe/barcelona/">Barcelona</a> no están exentos: pueden pedir un permiso de hasta 24 días al año y deben estar inscritos en el registro metropolitano (AMB).</li>
</ul></section>

<section class="card"><h2>Qué hacer antes de ir</h2>
<ol>
<li>Escribe tu matrícula en <a href="../../">el buscador</a> y marca la casilla «Es un vehículo histórico».</li>
<li>Toca la ciudad a la que vas: si ya hemos revisado su norma, te la mostramos.</li>
<li>Si no la hemos revisado aún, entra en la web del ayuntamiento y busca «vehículos históricos» en la ordenanza de la zona de bajas emisiones.</li>
<li>Si hay que registrarse, hazlo <strong>antes</strong> de entrar: las cámaras multan al momento.</li>
<li>Lleva en el coche la documentación de vehículo histórico (la tarjeta ITV con la catalogación).</li>
</ol></section>

<section class="card"><h2>¿Qué cuenta como vehículo histórico?</h2>
<p>El que está catalogado como histórico según el Reglamento de Vehículos Históricos (normalmente con más de 30 años y en estado original), con su inspección en la ITV. Un coche viejo sin catalogar <strong>no</strong> es histórico, aunque tenga muchos años.</p></section>
""",
    "faq": [
        ("¿Los coches históricos pueden entrar en las zonas de bajas emisiones?", "Depende de cada ayuntamiento. En algunas ciudades están exentos, en otras hay que registrarse y en otras, como Barcelona, solo pueden entrar unos días al año con permiso."),
        ("¿Qué etiqueta tiene un coche histórico?", "Normalmente ninguna, porque por su año no cumple las normas de emisiones. Por eso necesita una excepción de la ciudad para entrar."),
    ],
}

EXTRANJEROS = {
    "slug": "coches-extranjeros-y-visitantes",
    "titulo": "Coches extranjeros y visitantes en las zonas de bajas emisiones",
    "title": "ZBE con coche extranjero o de alquiler: qué hay que hacer en España",
    "desc": "Si vienes con un coche de otro país o de alquiler, o visitas una ciudad española: cuándo hay que registrarse antes de entrar en una zona de bajas emisiones.",
    "revisado": "2026-11-24",
    "cuerpo": """
<section class="card"><h2>Si vienes de otra ciudad de España</h2>
<p>No tienes que hacer nada especial: si tu etiqueta puede entrar, entras igual que un vecino. Compruébalo con tu matrícula en <a href="../../">el buscador</a>.</p>
<p>Si tu etiqueta no puede entrar, mira en la página de la ciudad si hay permisos para visitantes, por ejemplo para ir a un parking público dentro de la zona, a un hotel o al hospital. Suelen pedir registrar la matrícula antes.</p></section>

<section class="card"><h2>Si tu coche tiene matrícula extranjera</h2>
<ul>
<li>Tu coche <strong>no tiene etiqueta de la DGT</strong>, así que nuestro buscador no lo encontrará.</li>
<li>Las pegatinas de otros países (Crit'Air francesa, Umweltplakette alemana…) <strong>no valen</strong> en España.</li>
<li>Muchas ciudades piden <strong>registrar el coche antes de entrar</strong>, indicando su norma Euro. Por ejemplo, en <a href="../../zbe/barcelona/">Barcelona</a> hay que darlo de alta en el registro de la AMB.</li>
<li>Busca en la web del ayuntamiento «vehículos extranjeros zona de bajas emisiones». Si no encuentras nada, usa un parking fuera de la zona y transporte público.</li>
</ul>
<p>Para saber qué etiqueta le correspondería, mira la norma Euro de tu documentación y compárala con <a href="../etiquetas-dgt/">la tabla de etiquetas</a>.</p></section>

<section class="card"><h2>Coches de alquiler</h2>
<p>Los de empresas españolas tienen matrícula española y etiqueta como cualquier otro: escribe la matrícula en el buscador. Casi todos son recientes (C, ECO o Cero) y pueden entrar. La multa llega a la empresa, que te la cobrará con un recargo.</p></section>
""",
    "faq": [
        ("¿Puede entrar un coche extranjero en una zona de bajas emisiones de España?", "Sí, si cumple la norma, pero no tiene etiqueta de la DGT y muchas ciudades piden registrarlo antes de entrar. Las pegatinas de otros países no sirven en España."),
        ("¿Tengo que registrarme si visito una ciudad con ZBE?", "Con coche español y una etiqueta permitida, no. Si tu etiqueta no está permitida, algunas ciudades dan permisos (por ejemplo, para ir a un parking público) pero hay que registrar la matrícula antes."),
    ],
}

PLAN_AUTO = {
    "slug": "ayudas-plan-auto",
    "titulo": "Ayudas para cambiar de coche: Plan Auto+ 2026",
    "title": "Plan Auto+ 2026: ayudas para comprar un coche eléctrico y entrar en las ZBE",
    "desc": "Qué se sabe del Plan Auto+ 2026, el sustituto del MOVES: qué coches entran, cuánto dinero, cómo se pide y qué dudas quedan.",
    "revisado": "2026-11-24",
    "cuerpo": """
<section class="card"><h2>Lo que está claro</h2>
<ul>
<li>Es el plan que <strong>sustituye al MOVES</strong>, con <strong>400 millones de euros</strong>.</li>
<li>Lo aprobó el Consejo de Ministros en julio de 2026 y cubre compras desde el <strong>1 de enero de 2026</strong>.</li>
<li>Es para coches con <strong>etiqueta Cero</strong>: eléctricos, híbridos enchufables con más de 40 km eléctricos y de hidrógeno. Con ellos puedes entrar en todas las zonas de bajas emisiones.</li>
<li>Según la prensa, en general es el <strong>concesionario quien adelanta la ayuda</strong> y la descuenta del precio.</li>
</ul></section>

<section class="card"><h2>Cuánto dinero: las cifras no coinciden</h2>
<p>Los medios dan cantidades distintas, y aquí preferimos decírtelo:</p>
<ul>
<li><a href="https://www.motorpasion.com/observatorio-motorpasion/plan-auto-ayudas-coche-electrico">Motorpasión</a>: hasta <strong>4.500 €</strong> más al menos 1.000 € que pone la marca, con más ayuda si el coche y la batería se fabrican en la UE. Precio máximo del coche: 45.000 € antes de impuestos.</li>
<li><a href="https://www.motor16.com/las-ultimas-noticias/ayudas-coches-electrificados-2026-plan-auto/">Motor16</a>: hasta <strong>7.000 €</strong> sumando la ayuda del Estado, la de achatarrar un coche viejo y hasta 2.000 € de tu comunidad autónoma.</li>
</ul>
<p>Tampoco coinciden en si achatarrar tu coche viejo da más dinero. Pregunta en el concesionario la cifra exacta para tu caso, y pide que te la pongan por escrito en el presupuesto.</p></section>

<section class="card"><h2>Consejos antes de comprar</h2>
<ol>
<li>Mira qué ciudades te afectan con tu matrícula actual en <a href="../../">el buscador</a>: quizá tu coche aún puede entrar donde vas.</li>
<li>Si cambias, un híbrido con etiqueta ECO también entra en casi todas las zonas, aunque no tiene esta ayuda.</li>
<li>Pregunta en tu comunidad autónoma si hay ayuda propia: se pide aparte y con sus plazos.</li>
</ol>
<p class="muted">Lo actualizaremos cuando se publique la convocatoria oficial.</p></section>
""",
    "faq": [
        ("¿Qué es el Plan Auto+?", "El plan de ayudas de 2026 que sustituye al MOVES para comprar coches con etiqueta Cero (eléctricos, enchufables con más de 40 km de autonomía e hidrógeno), con 400 millones de euros."),
        ("¿Cuánto dan con el Plan Auto+?", "Las cifras publicadas varían: hasta 4.500 € más al menos 1.000 € de la marca según unas fuentes, y hasta 7.000 € con achatarramiento y ayuda autonómica según otras. Confírmalo en el concesionario."),
    ],
}

FAQ = {
    "slug": "preguntas-frecuentes",
    "titulo": "Preguntas frecuentes sobre las zonas de bajas emisiones",
    "title": "Zonas de bajas emisiones (ZBE): preguntas frecuentes y respuestas claras",
    "desc": "Qué es una ZBE, qué ciudades la tienen, cuánto es la multa, cómo funcionan las cámaras, qué pasa si no tengo etiqueta y más, explicado claro.",
    "revisado": "2026-11-24",
    "cuerpo": "",
    "faq": [
        ("¿Qué es una zona de bajas emisiones (ZBE)?", "Una zona de una ciudad donde solo pueden circular los vehículos que menos contaminan, según su etiqueta de la DGT. Cada ayuntamiento decide qué etiquetas entran, en qué horario y con qué excepciones."),
        ("¿Qué ciudades tienen que tener ZBE?", "La Ley de Cambio Climático obliga a los municipios de más de 50.000 habitantes y a los territorios insulares, y a los de más de 20.000 si tienen mala calidad del aire. Son unos 150 municipios; no todos la aplican aún."),
        ("¿Cuánto es la multa por entrar en una ZBE?", "Normalmente 200 €, o 100 € si pagas en 20 días naturales. La cuantía la fija cada ayuntamiento."),
        ("¿Cómo multan?", "Con cámaras que leen la matrícula a la entrada y dentro de la zona y la comparan con el registro de la DGT. La multa llega por correo o a la dirección electrónica vial (DEV)."),
        ("¿Puedo entrar para ir a la ITV, al taller o al hospital?", "Depende de la ciudad. Muchas dan permisos para talleres, citas médicas o el hospital, pero casi siempre hay que avisar antes o en las 24 a 48 horas siguientes con un justificante. Míralo en la página de cada ciudad o en la web del ayuntamiento."),
        ("¿Puedo parar un momento a recoger o dejar a alguien?", "En general, no: la cámara registra la entrada aunque estés un minuto. Algunas ciudades dan permisos para llevar a los niños al colegio o a personas con movilidad reducida, pero hay que pedirlos."),
        ("¿Puede invitarme un familiar que vive dentro de la zona?", "En algunas ciudades, sí. En Bilbao, por ejemplo, cada vecino de la zona puede invitar hasta 6 coches al mes. En otras no existe esa opción. Míralo en la página de la ciudad."),
        ("¿Tengo que llevar la pegatina puesta?", "Las cámaras leen la matrícula, no la pegatina, pero algunas ordenanzas obligan a llevarla en el parabrisas. Llevarla evita problemas con un agente."),
        ("¿Qué hago si creo que mi coche tiene la etiqueta equivocada?", "La etiqueta sale de la fecha de matriculación, el combustible y la norma Euro de la ficha técnica. Si crees que está mal, pide la corrección a la DGT (sede electrónica o cita previa) con la ficha técnica, que debe indicar la norma Euro."),
        ("¿Qué pasa si mi coche no tiene etiqueta?", "Es el caso más restringido. En muchas ciudades no puede entrar, pero en otras sí o solo en ciertos horarios. Escribe tu matrícula en el buscador y verás ciudad por ciudad."),
        ("¿Cómo sé la etiqueta de mi coche?", "Escribe tu matrícula en ¿Puedo entrar?: mostramos la etiqueta oficial de la DGT, actualizada cada día, gratis y sin registro."),
        ("¿Los vecinos de la zona pueden entrar?", "Casi siempre los empadronados tienen excepciones o plazos más largos, pero cada ciudad pone sus condiciones. Un tribunal anuló la ZBE de Málaga precisamente por eximir a los coches por su domicilio."),
        ("¿Y si voy a un parking dentro de la zona?", "Muchas ciudades permiten entrar para ir a un aparcamiento público, a veces registrando la matrícula. Consúltalo en la web del ayuntamiento antes de ir."),
        ("¿Las motos también tienen que cumplir?", "Sí. Las motos también tienen etiqueta de la DGT y la mayoría de zonas las incluyen, con las mismas reglas que los coches o parecidas."),
        ("¿Qué es un episodio de contaminación?", "Días con mucha contaminación en los que algunas ciudades restringen más el tráfico. En ciudades como Alcalá de Henares la ZBE solo se aplica esos días."),
        ("¿Esta web es oficial?", "No. Es una web informativa que usa los datos abiertos de la DGT y de OpenStreetMap, actualizados cada día. Confirma siempre la norma en la web del ayuntamiento."),
    ],
}

GUIAS = [RECURRIR, ETIQUETAS, HISTORICOS, EXTRANJEROS, PLAN_AUTO, FAQ]
