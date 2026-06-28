# -*- coding: utf-8 -*-
"""Generador del 'Pack 100 Respuestas para WhatsApp' — Academia Venta Digital.
Fuente única de datos -> genera HTML (para PDF), Markdown editable y CSV.
"""
import html, csv, io

# ---------------------------------------------------------------------------
# DATOS: 100 mensajes en 9 categorías.
# Cada mensaje: (titulo, mensaje, corta, cuando)
# Variables entre [corchetes] para que el usuario las reemplace.
# ---------------------------------------------------------------------------

CATEGORIAS = [
("Mensajes de bienvenida",
 "Las primeras palabras marcan el tono. Salud con calidez, agradece el contacto e invita a contar qué necesita.",
[
("Bienvenida general",
 "¡Hola! 👋 Gracias por escribir a [Tu Negocio]. Soy [tu nombre] y con gusto te ayudo. Cuéntame, ¿qué estás buscando hoy?",
 "¡Hola! 👋 Gracias por escribir. Cuéntame, ¿en qué te ayudo?",
 "Apenas un cliente nuevo escribe por primera vez."),
("Bienvenida desde un anuncio",
 "¡Hola! 🙌 Veo que llegaste por nuestra publicación de [producto/oferta]. ¡Buena elección! ¿Te cuento los detalles?",
 "¡Hola! 🙌 ¿Llegaste por el anuncio de [producto]? Te cuento los detalles 👇",
 "Cuando el contacto viene de una publicidad o promoción puntual."),
("Bienvenida desde redes sociales",
 "¡Hola! 😊 Qué bueno verte por aquí desde [Instagram/Facebook]. Gracias por escribir. ¿Qué te gustaría saber?",
 "¡Hola! 😊 Gracias por escribirnos desde [red]. ¿Qué te gustaría saber?",
 "Cuando el cliente llega desde un perfil o historia en redes."),
("Bienvenida fuera de horario",
 "¡Hola! 🙌 Gracias por escribir. En este momento estoy fuera de horario, pero apenas vuelva (a las [hora]) te respondo. Déjame tu consulta y la dejo lista 😊",
 "¡Hola! Gracias por escribir 🙌 Te respondo apenas vuelva a las [hora]. Cuéntame qué necesitas.",
 "Como respuesta automática cuando no puedes atender al momento."),
("Bienvenida que califica al cliente",
 "¡Hola! 👋 Gracias por tu mensaje. Para recomendarte lo mejor, ¿es para ti o para regalo? Así te oriento mejor 😊",
 "¡Hola! 👋 ¿Es para ti o para regalo? Así te recomiendo mejor.",
 "Cuando quieres entender la necesidad antes de ofrecer algo."),
("Bienvenida breve y cálida",
 "¡Holaa! 😊 Qué gusto que escribas. Cuéntame en qué te puedo ayudar y vemos todo al toque.",
 "¡Holaa! 😊 Cuéntame en qué te ayudo.",
 "Para negocios de tono muy cercano e informal."),
("Bienvenida con beneficio destacado",
 "¡Hola! 🙌 Gracias por escribir a [Tu Negocio], donde [beneficio principal: ej. encuentras X con envío a todo el país]. ¿Qué estás buscando?",
 "¡Hola! 🙌 En [Tu Negocio] encuentras [beneficio]. ¿Qué buscas?",
 "Cuando quieres dejar clara tu propuesta de valor desde el inicio."),
("Bienvenida a un referido",
 "¡Hola! 😊 Qué bueno que [nombre de quien refiere] te recomendara. Bienvenido/a. Cuéntame qué necesitas y te ayudo con todo gusto.",
 "¡Hola! 😊 Bienvenido/a de parte de [referente]. ¿En qué te ayudo?",
 "Cuando alguien llega recomendado por otro cliente."),
("Bienvenida con catálogo",
 "¡Hola! 👋 Gracias por escribir. Te dejo nuestro catálogo aquí 👉 [link/imagen]. Cualquier cosa que te guste, me dices y te paso los detalles 😊",
 "¡Hola! 👋 Aquí va el catálogo 👉 [link]. ¿Algo te llamó la atención?",
 "Cuando el cliente pide ver opciones o productos disponibles."),
("Bienvenida con respuesta rápida",
 "¡Hola! 🙌 Gracias por contactarnos. Ya recibí tu mensaje y en un momento te respondo personalmente. Mientras, cuéntame qué necesitas 😊",
 "¡Hola! 🙌 Recibí tu mensaje, en un momento te respondo. Cuéntame qué necesitas.",
 "Como auto-respuesta para que el cliente sepa que lo viste."),
("Bienvenida agradeciendo el interés",
 "¡Hola! 😊 Gracias por interesarte en [producto/servicio]. Es de mis favoritos para recomendar. ¿Quieres que te cuente cómo funciona?",
 "¡Hola! 😊 Gracias por tu interés en [producto]. ¿Te cuento cómo funciona?",
 "Cuando el cliente menciona un producto específico al escribir."),
("Bienvenida personalizada por nombre",
 "¡Hola [nombre]! 👋 Qué gusto saludarte. Gracias por escribir a [Tu Negocio]. Cuéntame, ¿en qué te puedo ayudar hoy?",
 "¡Hola [nombre]! 👋 ¿En qué te ayudo hoy?",
 "Cuando ya conoces el nombre del cliente (por su perfil o contacto)."),
("Bienvenida con promoción vigente",
 "¡Hola! 🙌 Llegaste en buen momento: esta semana tenemos [promoción]. Cuéntame qué buscas y vemos cómo aprovecharla 😊",
 "¡Hola! 🙌 Esta semana hay [promoción]. ¿Qué estás buscando?",
 "Cuando tienes una oferta activa que quieres comunicar de entrada."),
("Bienvenida que dirige a la información",
 "¡Hola! 😊 Gracias por escribir. Para ayudarte rápido: ¿quieres ver precios, conocer el producto o coordinar una compra? Dime y vamos al grano 🙌",
 "¡Hola! 😊 ¿Quieres ver precios, conocer el producto o comprar? Dime y vamos 🙌",
 "Cuando recibes muchos mensajes y quieres ordenar la conversación."),
("Bienvenida a un cliente que vuelve",
 "¡Hola de nuevo! 😊 Qué bueno tenerte por acá otra vez. Gracias por la confianza. Cuéntame, ¿en qué te ayudo esta vez?",
 "¡Hola de nuevo! 😊 Qué bueno tenerte de vuelta. ¿En qué te ayudo?",
 "Cuando reconoces a alguien que ya te había comprado o consultado."),
]),

("Respuestas a consultas iniciales",
 "Responde claro y completo, y termina siempre con una pregunta o un paso siguiente para mantener viva la conversación.",
[
("Responder \"¿qué venden?\"",
 "¡Hola! 😊 En [Tu Negocio] nos especializamos en [productos/servicios]. Cuéntame qué necesitas y te muestro las mejores opciones para ti 🙌",
 "¡Hola! 😊 Vendemos [productos]. ¿Qué estás buscando?",
 "Cuando el cliente pregunta de forma general qué ofreces."),
("Confirmar disponibilidad / stock",
 "¡Hola! 🙌 Sí, tengo disponible el [producto] que buscas. ¿Lo quieres en [color/talla/variante] o te muestro las opciones?",
 "¡Sí, está disponible! 🙌 ¿En qué [color/talla] lo quieres?",
 "Cuando preguntan si tienes un producto en stock."),
("Responder \"¿hacen envíos?\"",
 "¡Hola! 😊 Sí, hacemos envíos a [zonas]. El costo es [valor o 'gratis sobre $X'] y llega en [tiempo]. ¿A qué ciudad sería?",
 "¡Sí, enviamos a [zonas]! 😊 ¿A qué ciudad sería?",
 "Cuando consultan por envíos o despacho."),
("Responder \"¿dónde están ubicados?\"",
 "¡Hola! 🙌 Estamos en [dirección/zona] y también vendemos online con envíos. ¿Prefieres pasar a vernos o coordinamos un envío?",
 "¡Hola! 🙌 Estamos en [zona] y también enviamos. ¿Qué te acomoda más?",
 "Cuando preguntan por tu ubicación o local físico."),
("Dar detalles del producto",
 "¡Claro! 😊 El [producto] incluye [característica 1], [característica 2] y [beneficio]. Es ideal si buscas [necesidad]. ¿Te paso fotos o precio?",
 "¡Claro! El [producto] tiene [beneficios]. ¿Te paso fotos o precio?",
 "Cuando piden más información sobre un producto puntual."),
("Explicar cómo funciona",
 "¡Buena pregunta! 🙌 Funciona así: [paso 1], luego [paso 2] y listo. Es muy simple. ¿Quieres que te lo explique con un ejemplo?",
 "¡Te explico! 🙌 [Paso 1] y luego [paso 2]. ¿Te lo muestro con un ejemplo?",
 "Cuando el cliente no entiende bien el producto o servicio."),
("Pedir contexto para asesorar",
 "¡Con gusto te ayudo! 😊 Para recomendarte lo ideal, cuéntame: ¿para qué lo necesitas y tienes alguna preferencia? Así afinamos la opción perfecta.",
 "¡Con gusto! 😊 ¿Para qué lo necesitas? Así te recomiendo lo ideal.",
 "Cuando necesitas más información para hacer una buena recomendación."),
("Responder cuando falta información",
 "¡Hola! 🙌 Para darte el dato exacto, ¿me cuentas [detalle que falta: ciudad / modelo / cantidad]? Así te respondo al toque 😊",
 "¡Hola! 🙌 ¿Me dices [detalle que falta]? Así te respondo exacto.",
 "Cuando la consulta es incompleta y necesitas un dato para responder."),
("Responder por color / talla / modelo",
 "¡Hola! 😊 Sí, lo tengo en [opciones disponibles]. El [opción] es el más pedido. ¿Cuál te gustaría?",
 "¡Sí! Lo tengo en [opciones]. ¿Cuál prefieres?",
 "Cuando preguntan por una variante específica."),
("Responder sobre originalidad / garantía",
 "¡Hola! 🙌 Sí, es 100% [original/nuevo] e incluye [garantía/respaldo]. Quiero que compres con total confianza. ¿Te cuento más?",
 "¡Sí, es [original] con [garantía]! 🙌 Compra con confianza.",
 "Cuando el cliente quiere asegurarse de la calidad o respaldo."),
("Responder horario de atención",
 "¡Hola! 😊 Atendemos de [días] de [hora] a [hora]. Aun así, déjame tu consulta cuando quieras y te respondo apenas pueda 🙌",
 "¡Hola! 😊 Atendemos [días y horario]. Déjame tu consulta cuando quieras.",
 "Cuando preguntan a qué hora atiendes o abres."),
("Responder formas de pago",
 "¡Hola! 🙌 Puedes pagar con [transferencia / efectivo / tarjeta / link de pago] y también ofrecemos [cuotas si aplica]. ¿Cuál te acomoda más?",
 "¡Hola! 🙌 Aceptamos [medios de pago]. ¿Cuál te acomoda?",
 "Cuando preguntan cómo pueden pagar."),
("Responder a quien \"solo está mirando\"",
 "¡Genial, mira con calma! 😊 Cualquier duda que tengas, aquí estoy. Y si quieres, te paso lo más pedido por si te sirve de referencia 🙌",
 "¡Mira con calma! 😊 Cualquier duda, aquí estoy.",
 "Cuando el cliente dice que solo está viendo, sin compromiso."),
("Responder una consulta técnica",
 "¡Buena pregunta! 🙌 Sobre [aspecto técnico]: [respuesta clara y simple]. Si necesitas el detalle completo te lo paso. ¿Te sirve así?",
 "¡Buena pregunta! 🙌 [Respuesta clara]. ¿Te sirve o quieres el detalle?",
 "Cuando hacen una consulta específica o técnica del producto."),
("Recomendar según la necesidad",
 "Por lo que me cuentas, te recomendaría [producto], porque [razón ligada a su necesidad] 😊 Es la opción que más se ajusta a ti. ¿Te muestro?",
 "Para lo que buscas, te recomiendo [producto] porque [razón] 😊 ¿Te muestro?",
 "Cuando ya sabes qué necesita y quieres guiarlo a la mejor opción."),
]),

("Mensajes para explicar precios",
 "Da el precio con seguridad y acompáñalo siempre de valor o de un paso siguiente. El precio nunca debe quedar 'solo'.",
[
("Precio con beneficio",
 "¡Hola! 😊 El [producto] te queda en $[precio] e incluye [beneficio]. ¿Te lo aparto o tienes alguna duda antes?",
 "El [producto] queda en $[precio] con [beneficio] 😊 ¿Te lo aparto?",
 "Respuesta estándar cuando preguntan el precio de un producto."),
("Precio con opción de cuotas",
 "¡Hola! 🙌 El valor es $[precio], y si prefieres lo puedes dividir en [N] partes de $[monto]. ¿Cuál opción te acomoda más?",
 "Son $[precio], o en [N] cuotas de $[monto] 🙌 ¿Cuál prefieres?",
 "Cuando ofreces pago en cuotas y quieres facilitar la decisión."),
("Precio con valor agregado",
 "El [producto] está en $[precio] 😊 Y lo bueno es que incluye [extra: envío / garantía / asesoría], así que aprovechas más. ¿Te gustaría?",
 "Son $[precio] e incluye [extra] 😊 ¿Te gustaría?",
 "Cuando quieres resaltar todo lo que el cliente recibe por ese precio."),
("Precio de varias opciones / packs",
 "¡Hola! 🙌 Te dejo las opciones:\n• [Opción 1]: $[precio]\n• [Opción 2]: $[precio]\n• Pack [3]: $[precio] (el más conveniente)\n¿Cuál te llama más la atención?",
 "Opciones: [1] $[precio] · [2] $[precio] · Pack $[precio] 🙌 ¿Cuál prefieres?",
 "Cuando tienes varios productos o packs para mostrar."),
("Responder \"¿cuánto cuesta?\" directo",
 "¡Hola! 😊 El [producto] te queda en $[precio]. ¿Te cuento qué incluye o lo dejamos coordinado?",
 "Te queda en $[precio] 😊 ¿Te cuento qué incluye?",
 "Cuando preguntan el precio de forma directa y sin rodeos."),
("Precio con oferta vigente",
 "¡Buena noticia! 🙌 El [producto] normalmente está $[precio], pero esta semana lo tienes en $[precio oferta]. ¿Lo aprovechamos?",
 "Esta semana el [producto] está en $[precio oferta] (antes $[precio]) 🙌 ¿Lo aprovechas?",
 "Cuando hay un descuento por tiempo limitado y honesto."),
("Precio con envío incluido",
 "¡Hola! 😊 Son $[precio] con el envío ya incluido a [zona], así no tienes costos extra. ¿Te lo dejo agendado?",
 "Son $[precio] con envío incluido 😊 ¿Te lo agendo?",
 "Cuando el envío gratis es un argumento de valor."),
("Justificar el precio por calidad",
 "Te entiendo 🙌 El valor es $[precio] porque [razón: material / durabilidad / atención personalizada]. Es una compra que te dura y vale la pena. ¿Te muestro por qué?",
 "Son $[precio] por [razón de calidad]. Vale la pena 🙌 ¿Te muestro?",
 "Cuando el cliente percibe el precio como alto y quieres mostrar el valor."),
("Precio comparando opciones",
 "Para que elijas tranquilo/a 😊: la opción [básica] está en $[precio] y la [completa] en $[precio], que incluye [extra]. La mayoría prefiere la [completa]. ¿Cuál te acomoda?",
 "[Básica] $[precio] o [completa] $[precio] con [extra] 😊 ¿Cuál te acomoda?",
 "Cuando quieres ayudar al cliente a comparar y decidir."),
("Precio con descuento por cantidad",
 "¡Hola! 🙌 La unidad está en $[precio], pero si llevas [N] te queda en $[precio] cada una. ¿Quieres aprovechar el precio por cantidad?",
 "1 unidad $[precio]; desde [N] queda en $[precio] c/u 🙌 ¿Aprovechas?",
 "Cuando ofreces mejor precio por volumen."),
("Calificar antes de dar el precio",
 "¡Con gusto te paso el precio! 😊 Para darte el valor exacto, cuéntame [cantidad / modelo / zona]. Así te cotizo bien y sin sorpresas 🙌",
 "¡Con gusto! 😊 ¿Me dices [cantidad/modelo]? Y te paso el precio exacto.",
 "Cuando el precio depende de detalles que aún no conoces."),
("Precio con garantía",
 "El [producto] está en $[precio] e incluye [garantía], así compras con respaldo y total tranquilidad 😊 ¿Te lo preparo?",
 "Son $[precio] con [garantía] incluida 😊 ¿Te lo preparo?",
 "Cuando la garantía respalda el precio y da confianza."),
("Precio de un servicio / por sesión",
 "¡Hola! 🙌 El [servicio] tiene un valor de $[precio] por [sesión/mes/proyecto] e incluye [qué incluye]. ¿Te gustaría agendar o resolver alguna duda?",
 "El [servicio] está en $[precio] por [unidad] e incluye [qué incluye] 🙌 ¿Agendamos?",
 "Cuando vendes servicios y no productos físicos."),
("Precio con link de pago / financiamiento",
 "¡Hola! 😊 Son $[precio] y puedes pagar fácil con [link de pago / financiamiento en N cuotas]. Te lo dejo listo para cuando quieras. ¿Avanzamos?",
 "Son $[precio], con pago fácil por [link/cuotas] 😊 ¿Avanzamos?",
 "Cuando ofreces medios de pago digitales o financiamiento."),
("Precio + invitación a decidir",
 "El [producto] te queda en $[precio] 😊 Si te parece bien, lo dejamos coordinado y te lo aseguro. ¿Lo confirmamos?",
 "Son $[precio] 😊 ¿Lo confirmamos y te lo aseguro?",
 "Cuando el cliente ya está interesado y quieres avanzar al cierre."),
]),

("Mensajes para hacer seguimiento",
 "Seguir no es perseguir. Cada mensaje debe aportar algo nuevo: una novedad, una facilidad o una ayuda. Nunca un seco '¿sigues interesado?'.",
[
("Seguimiento el mismo día",
 "¡Hola [nombre]! 😊 Te dejo resumido lo que conversamos: [producto] en $[precio] con [beneficio]. Quedo atento/a para dejarlo coordinado cuando quieras 🙌",
 "¡Hola [nombre]! 😊 Resumo: [producto] en $[precio]. Quedo atento/a 🙌",
 "El mismo día de la consulta, para dejar todo claro y abierto."),
("Seguimiento al día siguiente",
 "¡Hola [nombre]! 😊 ¿Pudiste pensar lo del [producto]? Sigue disponible y feliz de resolver cualquier duda que te haya quedado 🙌",
 "¡Hola [nombre]! 😊 ¿Pudiste verlo? Sigue disponible, cualquier duda aquí estoy.",
 "1 o 2 días después, cuando no hubo respuesta tras la primera charla."),
("Seguimiento con apartado",
 "¡Hola [nombre]! 🙌 Te aparté una unidad del [producto] por si todavía la querías. Te la guardo hasta [día]. ¿La dejamos lista?",
 "¡Hola [nombre]! 🙌 Te aparté el [producto] hasta [día]. ¿Lo dejamos listo?",
 "Cuando quieres dar un motivo amable para que el cliente decida."),
("Seguimiento con novedad de stock",
 "¡Hola [nombre]! 😊 Me llegó justo el [producto/variante] que estabas buscando. Te dejo foto por si todavía te interesa 👇",
 "¡Hola [nombre]! 😊 Llegó el [producto] que buscabas. ¿Te muestro?",
 "Cuando reapareció o llegó algo que el cliente pidió antes."),
("Seguimiento con oferta",
 "¡Hola [nombre]! 🙌 Me acordé de ti porque esta semana tengo [oferta] en [producto]. Quería avisarte por si quieres aprovecharlo 😊",
 "¡Hola [nombre]! 🙌 Esta semana hay [oferta] en [producto]. ¿La aprovechamos?",
 "Cuando tienes una promoción que puede destrabar la decisión."),
("Seguimiento tras enviar el precio",
 "¡Hola [nombre]! 😊 ¿Te hizo sentido el valor que te pasé? Si quieres lo vemos con calma o ajustamos algo. Estoy para ayudarte 🙌",
 "¡Hola [nombre]! 😊 ¿Te hizo sentido el precio? Lo vemos con calma.",
 "Cuando enviaste un precio y el cliente quedó en silencio."),
("Seguimiento amable \"¿pudiste ver?\"",
 "¡Hola [nombre]! 😊 Solo paso a saludar y saber si pudiste revisar lo que te envié. Sin apuro, cuando puedas me cuentas 🙌",
 "¡Hola [nombre]! 😊 ¿Pudiste revisar lo que te envié? Sin apuro.",
 "Para retomar con suavidad sin presionar."),
("Seguimiento con info extra",
 "¡Hola [nombre]! 🙌 Te comparto [foto/video/dato extra] del [producto] que creo te puede ayudar a decidir. Cualquier duda, aquí estoy 😊",
 "¡Hola [nombre]! 🙌 Te dejo [info extra] del [producto] por si te ayuda a decidir.",
 "Cuando puedes aportar contenido útil que sume valor."),
("Seguimiento recordando el beneficio",
 "¡Hola [nombre]! 😊 Recordaba que buscabas [necesidad]. El [producto] justo resuelve eso porque [beneficio]. ¿Lo retomamos?",
 "¡Hola [nombre]! 😊 El [producto] resuelve lo que buscabas: [beneficio]. ¿Lo retomamos?",
 "Cuando quieres reconectar la oferta con el problema del cliente."),
("Seguimiento por fin de promoción",
 "¡Hola [nombre]! 🙌 Te aviso que la promo de [producto] termina [día]. No quería que la perdieras por no avisarte. ¿La aprovechamos?",
 "¡Hola [nombre]! 🙌 La promo termina [día]. ¿La aprovechamos antes?",
 "Cuando una oferta real está por terminar (sin inventar urgencia)."),
("Seguimiento preguntando la duda",
 "¡Hola [nombre]! 😊 ¿Hubo algo que te generó duda? Cuéntame con confianza y lo aclaramos. Prefiero que decidas tranquilo/a 🙌",
 "¡Hola [nombre]! 😊 ¿Quedó alguna duda? Cuéntame y la aclaramos.",
 "Cuando sospechas que una duda sin resolver frenó al cliente."),
("Seguimiento ofreciendo ayuda",
 "¡Hola [nombre]! 🙌 Quedo a tu disposición por si necesitas que te ayude a elegir o coordinar algo. Sin compromiso, cuando gustes 😊",
 "¡Hola [nombre]! 🙌 Aquí estoy si necesitas ayuda para decidir.",
 "Para mantener la puerta abierta de forma servicial."),
("Seguimiento con testimonio / reseña",
 "¡Hola [nombre]! 😊 Te comparto lo que opinó [otro cliente] sobre el [producto] 👇 por si te sirve para decidir con más confianza 🙌",
 "¡Hola [nombre]! 😊 Mira lo que opinó otro cliente del [producto] 👇",
 "Cuando una reseña real puede dar el empujón de confianza."),
("Seguimiento por última unidad",
 "¡Hola [nombre]! 🙌 Me queda la última unidad del [producto] que viste. Si todavía la quieres, te la aparto hoy para que no la pierdas 😊",
 "¡Hola [nombre]! 🙌 Queda la última unidad. ¿Te la aparto hoy?",
 "Cuando el stock es real y bajo (nunca lo inventes)."),
("Seguimiento de cierre de ciclo",
 "¡Hola [nombre]! 😊 No quiero llenarte de mensajes. Si más adelante necesitas el [producto], aquí estaré con gusto. ¡Que tengas una linda semana! 🙌",
 "¡Hola [nombre]! 😊 Si más adelante lo necesitas, aquí estoy. ¡Linda semana!",
 "Como último mensaje amable tras varios intentos sin respuesta."),
]),

("Clientes que dejaron de responder",
 "El silencio casi nunca es un 'no': suele ser un 'me distraje'. Retoma con calidez y un motivo nuevo, sin reproches ni presión.",
[
("Recordatorio suave",
 "¡Hola [nombre]! 😊 Pasaba a retomar nuestra conversación sobre el [producto]. Sin apuro, cuando puedas me cuentas cómo seguimos 🙌",
 "¡Hola [nombre]! 😊 Retomo lo del [producto]. ¿Cómo seguimos?",
 "Primer intento tras unos días de silencio."),
("Con valor: sigue disponible",
 "¡Hola [nombre]! 🙌 Solo para contarte que el [producto] sigue disponible por si todavía lo quieres. Te lo puedo dejar apartado 😊",
 "¡Hola [nombre]! 🙌 El [producto] sigue disponible. ¿Te lo aparto?",
 "Cuando quieres reabrir con un motivo concreto."),
("Pregunta abierta",
 "¡Hola [nombre]! 😊 ¿Cómo vas con la decisión del [producto]? Cuéntame si quieres avanzar o si prefieres que lo dejemos para más adelante 🙌",
 "¡Hola [nombre]! 😊 ¿Cómo vas con el [producto]? Avanzamos o lo dejamos para después.",
 "Para invitar a responder dando opciones cómodas."),
("Ofreciendo resolver una duda",
 "¡Hola [nombre]! 🙌 Quizás quedó alguna duda dando vueltas. Si me cuentas qué te frena, lo resolvemos juntos. Sin compromiso 😊",
 "¡Hola [nombre]! 🙌 ¿Quedó alguna duda? La resolvemos juntos, sin compromiso.",
 "Cuando crees que una duda sin aclarar detuvo al cliente."),
("Tono cercano y ligero",
 "¡Hola [nombre]! 😊 No quería dejarte en visto sin querer 😅 Aquí sigo por si quieres retomar lo del [producto]. ¿Cómo estás?",
 "¡Hola [nombre]! 😊 Aquí sigo por si quieres retomar lo del [producto] 🙌",
 "Con clientes de trato cercano, para romper el hielo con simpatía."),
("Con una novedad",
 "¡Hola [nombre]! 🙌 Tengo una novedad sobre el [producto]: [nuevo color / mejor precio / nuevo stock]. Me acordé de ti y quise avisarte 😊",
 "¡Hola [nombre]! 🙌 Novedad del [producto]: [novedad]. Me acordé de ti 😊",
 "Cuando hay algo nuevo que justifica volver a escribir."),
("Reabrir con una oferta",
 "¡Hola [nombre]! 😊 Quería avisarte que tengo [oferta] en el [producto] que viste. Quizás es el momento ideal para aprovecharlo 🙌",
 "¡Hola [nombre]! 😊 Hay [oferta] en el [producto] que viste. ¿La aprovechas?",
 "Cuando una promoción puede reactivar el interés."),
("\"¿Mal momento?\"",
 "¡Hola [nombre]! 😊 ¿Te pillé en mal momento la otra vez? Sin problema. Cuando tengas un ratito retomamos lo del [producto] con calma 🙌",
 "¡Hola [nombre]! 😊 ¿Fue mal momento? Retomamos cuando puedas, sin apuro.",
 "Para quitar presión y mostrar empatía con el silencio."),
("Dar espacio (penúltimo intento)",
 "¡Hola [nombre]! 😊 No quiero insistir de más. Si por ahora no es el momento, lo entiendo perfecto. Solo dime y lo dejamos para cuando estés listo/a 🙌",
 "¡Hola [nombre]! 😊 Si no es el momento, lo entiendo. Tú me dices cuándo.",
 "Cuando ya hubo varios intentos y quieres mostrar respeto."),
("Cierre respetuoso del ciclo",
 "¡Hola [nombre]! 🙌 Será este mi último mensaje para no abrumarte. Fue un gusto. Si en el futuro necesitas el [producto], aquí estaré con gusto 😊",
 "¡Hola [nombre]! 🙌 No te escribo más para no abrumar. Si me necesitas, aquí estoy 😊",
 "Último mensaje del ciclo, dejando una buena impresión."),
]),

("Respuestas a objeciones comunes",
 "Una objeción es una duda, no un rechazo. La fórmula: validar lo que siente, responder con calma y proponer el paso siguiente.",
[
("\"Está muy caro\"",
 "Te entiendo 🙌 Lo bueno es que el [producto] [beneficio: te dura / te ahorra / incluye X], así que rinde más de lo que parece. Y si ayuda, lo dividimos en [N] pagos. ¿Te sirve así?",
 "Te entiendo 🙌 Rinde más de lo que parece, y lo puedo dividir en [N] pagos. ¿Te sirve?",
 "Cuando el cliente siente que el precio es alto."),
("\"Lo tengo que pensar\"",
 "¡Claro, tómate tu tiempo! 😊 Solo para ayudarte: ¿hay algo puntual que te genere duda? Así te lo aclaro y decides con total tranquilidad 🙌",
 "¡Claro, tómate tu tiempo! 😊 ¿Hay alguna duda puntual que te aclare?",
 "Cuando el cliente pide tiempo para decidir."),
("\"Lo vi más barato en otro lado\"",
 "Puede ser 🙌 Lo que incluyo yo es [garantía / atención directa / envío seguro] y respondo siempre que me necesites. Esa tranquilidad también cuenta. ¿Lo prefieres con ese respaldo?",
 "Puede ser 🙌 Conmigo tienes [respaldo/garantía/atención]. ¿Lo prefieres así?",
 "Cuando comparan tu precio con el de la competencia."),
("\"Ahora no tengo plata\"",
 "¡Sin problema, te entiendo! 😊 ¿Quieres que te lo aparte para [fecha] o te aviso cuando tenga una promo? Así no lo pierdes cuando estés listo/a 🙌",
 "¡Te entiendo! 😊 ¿Te lo aparto para [fecha] o te aviso cuando haya promo?",
 "Cuando el tema es presupuesto o momento económico."),
("\"No estoy seguro si me servirá\"",
 "¡Buena duda! 🙌 Cuéntame para qué lo necesitas y te digo con honestidad si es lo ideal para ti. Prefiero que quedes contento/a antes que venderte algo que no te sirva 😊",
 "¡Buena duda! 🙌 Cuéntame para qué lo quieres y te digo con honestidad si te sirve.",
 "Cuando el cliente no está seguro de que el producto le sirva."),
("\"Tengo que consultarlo\"",
 "¡Perfecto, me parece bien! 😊 Para que lo conversen con la info clara, te dejo un resumen: [producto], [precio], [beneficio]. Cualquier duda que surja, aquí estoy 🙌",
 "¡Me parece bien! 😊 Te dejo el resumen para que lo conversen: [producto, precio, beneficio].",
 "Cuando debe consultarlo con su pareja, socio o familia."),
("\"Me da desconfianza comprar online\"",
 "¡Te entiendo perfecto! 🙌 Para tu tranquilidad: [forma de pago seguro / contra entrega / reseñas / garantía]. Quiero que compres seguro/a. ¿Te muestro?",
 "¡Te entiendo! 🙌 Para tu tranquilidad tienes [pago seguro/garantía/reseñas]. ¿Te muestro?",
 "Cuando el cliente teme comprar por internet."),
("\"¿Y si no me gusta?\"",
 "¡Muy válido! 😊 Tenemos [cambio / garantía / política de devolución], así que compras tranquilo/a. La idea es que quedes feliz con tu [producto] 🙌",
 "¡Muy válido! 😊 Tienes [cambio/garantía], compras tranquilo/a.",
 "Cuando teme arrepentirse de la compra."),
("\"No es buen momento\"",
 "¡Lo entiendo! 😊 No hay apuro. ¿Quieres que te escriba más adelante o prefieres que te avise si sale alguna promo del [producto]? Tú me dices 🙌",
 "¡Lo entiendo! 😊 ¿Te escribo más adelante o te aviso si hay promo?",
 "Cuando el cliente dice que no es el momento adecuado."),
("\"Déjame ver y te aviso\"",
 "¡Perfecto! 😊 Quedo atento/a. Para no perder el contacto, ¿te parece si te escribo el [día] por si decidiste? Sin compromiso, solo para acompañarte 🙌",
 "¡Perfecto! 😊 ¿Te escribo el [día] para saber cómo vas? Sin compromiso.",
 "Cuando el cliente queda en avisarte (y quieres asegurar el seguimiento)."),
]),

("Mensajes de cierre de venta",
 "Cerrar es facilitar el 'sí'. Sé claro, da el paso siguiente exacto y quita toda la fricción posible.",
[
("Cierre directo",
 "¡Perfecto! 🙌 Entonces te confirmo el [producto] en $[precio]. Te paso los datos para coordinar el pago, ¿te parece?",
 "¡Perfecto! 🙌 Te confirmo el [producto] en $[precio]. ¿Coordinamos el pago?",
 "Cuando el cliente ya está decidido (etapa caliente)."),
("Cierre con opciones",
 "¡Genial! 😊 ¿Lo prefieres con envío a domicilio o pasas a retirarlo? Así te lo voy dejando listo 🙌",
 "¡Genial! 😊 ¿Con envío o lo retiras? Así te lo dejo listo.",
 "Para facilitar la decisión ofreciendo elegir entre A o B."),
("Cierre con urgencia honesta",
 "¡Buena elección! 🙌 Me queda la última unidad / la promo termina hoy. Si quieres te la aseguro ahora para que no la pierdas 😊",
 "¡Buena elección! 🙌 Queda poco / la promo termina hoy. ¿Te la aseguro?",
 "Cuando hay una razón real de tiempo o stock (nunca inventada)."),
("Cierre tras resolver la duda",
 "¡Listo, espero haber aclarado tu duda! 😊 Si te parece bien, lo dejamos confirmado y coordinamos el pago. ¿Avanzamos?",
 "¡Espero haber aclarado tu duda! 😊 ¿Lo dejamos confirmado?",
 "Justo después de responder una objeción o consulta final."),
("Cierre con beneficio extra",
 "¡Perfecto! 🙌 Y si lo confirmamos hoy, te incluyo [beneficio extra: envío gratis / pequeño regalo / descuento]. ¿Lo dejamos listo?",
 "¡Perfecto! 🙌 Si lo confirmas hoy te incluyo [extra]. ¿Lo dejamos listo?",
 "Cuando un pequeño incentivo puede inclinar la decisión."),
("Cierre asumiendo la venta",
 "¡Excelente elección! 😊 Te voy preparando el [producto]. ¿A nombre de quién lo dejo y a qué dirección lo enviamos?",
 "¡Excelente! 😊 Te lo voy preparando. ¿A nombre de quién y a qué dirección?",
 "Cuando el cliente mostró señales claras de querer comprar."),
("Cierre con apartado",
 "¡Genial! 🙌 Te lo aparto enseguida para asegurarte el stock. Con [seña / confirmación] te lo dejo reservado. ¿Te parece?",
 "¡Genial! 🙌 Te lo aparto para asegurar el stock. ¿Lo reservamos?",
 "Cuando el cliente quiere pero necesita un poco más de tiempo."),
("Cierre con resumen",
 "Entonces quedamos así 😊: [producto], $[precio], [forma de entrega]. ¿Lo confirmamos y avanzamos con el pago?",
 "Quedamos: [producto] a $[precio] con [entrega] 😊 ¿Lo confirmamos?",
 "Para ordenar y cerrar cuando ya conversaron varios detalles."),
("Cierre con facilidad de pago",
 "¡Perfecto! 🙌 Para que sea cómodo, puedes pagar con [link / transferencia / cuotas]. Te dejo todo listo, solo dime cuál te acomoda 😊",
 "¡Perfecto! 🙌 Págalo fácil con [link/transferencia/cuotas]. ¿Cuál te acomoda?",
 "Cuando facilitar el pago es lo que falta para cerrar."),
("Cierre amable final",
 "Me encantaría ayudarte con tu [producto] 😊 Si te parece bien, lo dejamos coordinado y te aseguras el tuyo. ¿Lo confirmamos? 🙌",
 "Me encantaría ayudarte 😊 ¿Lo confirmamos y te aseguro el tuyo?",
 "Cierre suave para clientes que valoran un trato cálido."),
]),

("Mensajes para pedir datos de compra",
 "Una vez que el cliente dijo 'sí', haz el proceso simple y ordenado. Pide solo lo necesario y confirma cada paso.",
[
("Pedir datos de envío",
 "¡Genial! 😊 Para coordinar tu envío, ¿me ayudas con estos datos?\n• Nombre completo:\n• Dirección y comuna/ciudad:\n• Teléfono de contacto:\nApenas los tenga, te confirmo todo 🙌",
 "¡Genial! 😊 Para el envío: nombre, dirección y teléfono. ¡Y te confirmo!",
 "Cuando el cliente confirmó la compra con despacho."),
("Pedir datos para boleta / factura",
 "¡Perfecto! 🙌 ¿Necesitas boleta o factura? Si es factura, pásame [razón social / RUT / giro] y la dejo lista junto a tu pedido 😊",
 "¡Perfecto! 🙌 ¿Boleta o factura? Si es factura, pásame los datos.",
 "Cuando necesitas datos para emitir el documento de pago."),
("Compartir datos de pago",
 "¡Listo! 😊 Te dejo los datos para el pago 👇\n[Banco / Nombre / Cuenta / Tipo / Correo]\nApenas hagas la transferencia, mándame el comprobante y te confirmo enseguida 🙌",
 "¡Listo! 😊 Datos de pago 👇 [datos]. Mándame el comprobante y confirmo.",
 "Cuando el cliente acordó pagar por transferencia."),
("Confirmar pedido y pedir comprobante",
 "¡Perfecto, pedido confirmado! 🙌 En cuanto me envíes el comprobante de pago, preparo tu [producto] y te aviso cuando vaya en camino 😊",
 "¡Pedido confirmado! 🙌 Envíame el comprobante y preparo tu [producto].",
 "Para cerrar el círculo una vez acordado el pago."),
("Pedir datos para coordinar un servicio",
 "¡Excelente! 😊 Para agendar tu [servicio], ¿me confirmas estos datos?\n• Nombre:\n• Día y hora que prefieres:\n• [Dato relevante del servicio]:\nY te dejo todo reservado 🙌",
 "¡Excelente! 😊 Para agendar: nombre, día/hora preferido y [dato]. ¡Y lo reservo!",
 "Cuando vendes servicios y necesitas coordinar una cita."),
]),

("Mensajes para reactivar clientes antiguos",
 "Tus clientes pasados ya confían en ti: son tu mejor activo. Reconecta con calidez, recordando que los valoras (no solo para venderles).",
[
("Saludo + novedad",
 "¡Hola [nombre]! 😊 ¿Cómo has estado? Pasaba a saludarte y a contarte que tenemos [novedad / nuevo producto] que creo te puede gustar. ¿Te muestro? 🙌",
 "¡Hola [nombre]! 😊 ¿Cómo has estado? Tenemos [novedad] que te puede gustar. ¿Te muestro?",
 "Para reconectar con un cliente que hace tiempo no te compra."),
("Oferta exclusiva para clientes",
 "¡Hola [nombre]! 🙌 Como ya eres cliente, quería darte acceso primero a [oferta exclusiva] antes que al resto. Es mi forma de agradecerte la confianza 😊",
 "¡Hola [nombre]! 🙌 Por ser cliente, tienes primero esta [oferta]. ¡Gracias por la confianza!",
 "Cuando quieres premiar la fidelidad con un beneficio especial."),
("Producto nuevo relacionado",
 "¡Hola [nombre]! 😊 Me acordé de ti porque llegó [producto nuevo] que combina perfecto con el [producto que compró]. ¿Te gustaría verlo? 🙌",
 "¡Hola [nombre]! 😊 Llegó [producto nuevo] ideal para complementar tu [compra]. ¿Te muestro?",
 "Cuando tienes algo que complementa una compra anterior."),
("\"Te extrañamos\" + beneficio",
 "¡Hola [nombre]! 😊 Hace tiempo que no nos vemos y queríamos saludarte. Si quieres volver a probar [producto/servicio], te dejo [beneficio] de bienvenida 🙌",
 "¡Hola [nombre]! 😊 ¡Te extrañábamos! Te dejo [beneficio] para volver a vernos.",
 "Para reactivar con un gesto cálido y un pequeño incentivo."),
("Recordatorio de reposición / recompra",
 "¡Hola [nombre]! 😊 Calculo que ya se te debe estar acabando tu [producto consumible]. ¿Quieres que te prepare otro para que no te quedes sin? 🙌",
 "¡Hola [nombre]! 😊 ¿Ya se te acaba tu [producto]? ¿Te preparo otro?",
 "Ideal para productos que se consumen o agotan con el tiempo."),
]),
]

# ---------------------------------------------------------------------------
# TEXTOS COMPLEMENTARIOS
# ---------------------------------------------------------------------------

INTRO = """Vender por WhatsApp es, muchas veces, una carrera contra el tiempo. El cliente pregunta, y cada minuto que tardas en responder —o cada vez que te quedas en blanco sin saber qué decir— es una venta que se enfría.

Este pack nace para resolver justamente eso. Aquí tienes <b>100 mensajes listos para copiar, pegar y editar</b>, pensados para las situaciones reales que vives todos los días: dar la bienvenida, responder consultas, explicar precios, hacer seguimiento, retomar a quien dejó de responder, manejar objeciones y cerrar ventas con claridad.

No son frases mágicas ni promesas de resultados. Son una <b>base profesional</b> para que respondas más rápido, con mejor tono y sin improvisar. Tú les pones tu producto, tu precio y tu personalidad; el pack te ahorra el trabajo de empezar desde cero cada vez.

El objetivo es simple: ayudarte a <b>ordenar y mejorar tu comunicación comercial</b> para que ninguna conversación se pierda por falta de una buena respuesta."""

INSTRUCCIONES = [
 ("Reemplaza los [corchetes]", "Cada mensaje tiene variables como [producto], [precio] o [nombre]. Cámbialas por los datos reales de tu negocio antes de enviar."),
 ("Guárdalos como respuestas rápidas", "En WhatsApp Business, ve a Ajustes → Herramientas para la empresa → Respuestas rápidas. Crea un atajo (ej. /precio) para cada mensaje y úsalos en segundos."),
 ("Adapta el tono a tu estilo", "Estos mensajes son cercanos y profesionales. Si tu marca es más formal o más divertida, ajusta una palabra aquí y allá para que suene a ti."),
 ("Personaliza siempre una línea", "La plantilla te da velocidad; una línea personalizada le da calidez. Menciona el nombre o algo que dijo el cliente para que no suene genérico."),
 ("Usa la variante corta cuando haga falta", "Para chats rápidos o clientes apurados, la versión corta va directo al grano sin perder amabilidad."),
 ("Sigue la recomendación de cuándo enviarlo", "Cada mensaje indica el mejor momento para usarlo. Enviar el mensaje correcto en el momento correcto es la mitad del resultado."),
 ("No copies y pegues sin leer", "Revisa siempre antes de enviar: que el precio, el nombre y el producto sean los correctos. Un mensaje mal pegado se nota."),
]

CHECKLIST = [
 "Respondí a todos los clientes nuevos del día.",
 "Atendí primero a los clientes más interesados (los \"calientes\").",
 "A cada conversación le dejé un paso siguiente claro.",
 "Hice al menos 3 seguimientos con valor (no un seco \"¿sigues ahí?\").",
 "Retomé al menos 1 cliente que había dejado de responder.",
 "Reemplacé bien los [corchetes] antes de enviar cada mensaje.",
 "Personalicé al menos una línea en los mensajes importantes.",
 "Pedí el cierre a quien ya estaba listo para comprar.",
 "Anoté con quién quedé pendiente para mañana.",
 "Revisé que ningún cliente interesado quedara sin respuesta.",
]

PROMPTS_IA = [
 "Actúa como experto en ventas por WhatsApp. Adapta este mensaje a mi negocio de [rubro], manteniendo un tono cercano y profesional, sin sonar agresivo: [pega el mensaje].",
 "Reescribe este mensaje de WhatsApp para que suene más [cercano / formal / divertido], sin perder claridad ni el llamado a la acción: [pega el mensaje].",
 "Tengo un negocio de [rubro] y vendo [producto/servicio]. Personaliza este mensaje reemplazando las variables con datos realistas de mi negocio: [pega el mensaje].",
 "Acórtame este mensaje de WhatsApp para que vaya directo al grano, pero siga siendo amable y con un emoji como máximo: [pega el mensaje].",
 "Un cliente me dijo: \"[objeción]\". Dame 3 respuestas para WhatsApp que validen lo que siente, respondan con calma y propongan un paso siguiente, sin presionar.",
 "Crea 5 variantes de este mensaje de seguimiento para no repetir siempre lo mismo con mis clientes, manteniendo un tono respetuoso y con valor: [pega el mensaje].",
 "Adapta este pack de mensajes a mi rubro de [rubro]. Cambia los ejemplos de productos por los míos: [lista tus productos]. Mantén el tono cercano y vendedor.",
 "Revisa este mensaje y dime si suena desesperado o demasiado insistente. Si es así, reescríbelo para que suene seguro, calmado y profesional: [pega el mensaje].",
 "Escríbeme un mensaje de bienvenida para WhatsApp Business de mi negocio de [rubro], que destaque mi beneficio principal: [beneficio], en tono cercano y con máximo un emoji.",
 "Tradúceme y adapta culturalmente este mensaje de WhatsApp para clientes de [país/región], cuidando que las expresiones suenen naturales y locales: [pega el mensaje].",
]

HOTMART_CORTA = "100 mensajes listos para copiar, pegar y editar en WhatsApp Business: bienvenida, consultas, precios, seguimiento, objeciones y cierre. Responde rápido, con buen tono y sin quedarte en blanco. Incluye variantes cortas, recomendaciones de uso y prompts de IA para adaptarlos a tu negocio."

HOTMART_LARGA_INTRO = """<b>¿Cuántas veces te has quedado sin saber qué responder a un cliente por WhatsApp?</b>

Si vendes por WhatsApp, conoces esa sensación: un cliente pregunta el precio, dice "lo pienso" o simplemente deja de responder, y tú no sabes qué escribir para no sonar insistente ni perder la venta. Cada duda al teclear es tiempo perdido y, muchas veces, una oportunidad que se enfría.

<b>Pack 100 Respuestas para WhatsApp</b> es tu biblioteca de mensajes listos para usar. 100 respuestas profesionales, cercanas y editables que cubren las situaciones reales de tu día a día comercial, para que nunca más te quedes en blanco."""

HOTMART_LARGA_INCLUYE = [
 "15 mensajes de bienvenida para cada tipo de contacto.",
 "15 respuestas para consultas iniciales (precio, stock, envíos y más).",
 "15 formas de explicar precios con seguridad y valor.",
 "15 mensajes de seguimiento que aportan valor sin presionar.",
 "10 mensajes para retomar a clientes que dejaron de responder.",
 "10 respuestas a las objeciones más comunes (\"está caro\", \"lo pienso\"...).",
 "10 mensajes de cierre claros y directos.",
 "5 mensajes para pedir datos de compra de forma ordenada.",
 "5 mensajes para reactivar clientes antiguos.",
 "Cada mensaje con una variante corta y la recomendación de cuándo enviarlo.",
 "Instrucciones de uso, checklist de seguimiento y 10 prompts de IA para adaptarlo todo a tu negocio.",
]

ORDER_BUMP = """<b>✅ Sí, agrega el Pack 100 Respuestas para WhatsApp a mi compra</b>

Ya tienes el sistema con <i>WhatsApp Ventas Pro</i>. Ahora llévate las palabras exactas para aplicarlo. Suma <b>100 mensajes listos para copiar y pegar</b> —bienvenida, precios, seguimiento, objeciones y cierre— para que nunca te quedes en blanco frente a un cliente. Editables, con variantes cortas y recomendaciones de cuándo usarlos. <b>Solo por hoy, agrégalo a tu pedido a un precio especial.</b>"""

CANVA_IDEAS = [
 ("Idea 1 — \"Burbujas de chat\"", "Plantilla tipo conversación: fondo claro con burbujas de chat verdes y blancas mostrando ejemplos de mensajes. Encabezado azul con el título. Transmite al instante que es un pack de mensajes para WhatsApp. <b>(La más representativa del producto.)</b>"),
 ("Idea 2 — \"Tarjetas numeradas\"", "Cada mensaje en una tarjeta limpia con número, título, mensaje y etiqueta de categoría con color. Estilo catálogo ordenado, fácil de hojear. Ideal para la versión editable que el usuario imprime o consulta en el celular."),
 ("Idea 3 — \"Índice por categorías\"", "Portada con un índice visual de las 9 categorías, cada una con su ícono y color. Páginas interiores con fondo neutro y acentos verdes. Estilo guía profesional, moderno y muy navegable."),
]

PORTADA = """<b>Concepto:</b> burbuja de chat verde estilo WhatsApp como protagonista, sobre fondo azul degradado (confianza + digital).

<b>Composición sugerida:</b>
• Arriba: \"ACADEMIA VENTA DIGITAL\" en mayúsculas espaciadas.
• Centro: título grande <b>\"Pack 100 Respuestas para WhatsApp\"</b> en blanco, dentro o junto a una burbuja de chat verde.
• Debajo: subtítulo \"Mensajes listos para responder, hacer seguimiento y cerrar ventas sin quedarte en blanco\".
• Detalle: un número \"100\" grande y destacado, y 3 píldoras con categorías (Bienvenida · Precios · Cierre).
• Pie: etiqueta \"Complemento de WhatsApp Ventas Pro\"."""

CONTRAPORTADA = """<b>Deja de quedarte en blanco frente a un cliente.</b>

Dentro de este pack tienes 100 mensajes profesionales y editables para cada momento de tu venta por WhatsApp: dar la bienvenida, responder consultas, explicar precios, hacer seguimiento, manejar objeciones, cerrar y reactivar clientes.

Cada mensaje viene listo para copiar y pegar, con una variante más corta y la recomendación de cuándo enviarlo. Solo reemplazas los datos de tu negocio y lo guardas como respuesta rápida en WhatsApp Business.

No prometemos ventas garantizadas ni fórmulas mágicas. Te damos una base sólida para <b>responder mejor, más rápido y con un tono que genera confianza</b>. El resto lo pones tú.

<i>Academia Venta Digital · Aprende a vender con orden, no con suerte.</i>"""

# Avisos legales (mismos que el ebook principal, para coherencia de marca)
AVISOS = [
 ("Sobre las marcas",
  "Este producto es independiente y no está afiliado, patrocinado ni aprobado por WhatsApp, Meta Platforms, Inc. ni empresas relacionadas. <b>WhatsApp</b>, <b>Facebook</b> e <b>Instagram</b> son marcas de sus respectivos propietarios. Las menciones a estas plataformas son solo con fines informativos y educativos."),
 ("Sobre los resultados",
  "Este material es de carácter educativo y comercial. <b>No promete ventas garantizadas ni resultados.</b> Los mensajes son una base para ordenar y mejorar tu comunicación; los resultados dependen de cada persona, de su producto, de su mercado y de su constancia."),
 ("Sobre las herramientas de IA",
  "Las funciones de inteligencia artificial mencionadas dependen de la herramienta que utilices (como ChatGPT u otras) y de sus condiciones de uso, disponibilidad y precios, que pueden cambiar. Academia Venta Digital no es responsable de dichas herramientas de terceros."),
]
AVISO_MARCAS_HOTMART = "Aviso de marcas (para incluir también en la página de Hotmart): Este producto es independiente y no está afiliado, patrocinado ni aprobado por WhatsApp, Meta Platforms, Inc. ni empresas relacionadas. WhatsApp, Facebook e Instagram son marcas de sus respectivos propietarios."

# ---------------------------------------------------------------------------
# VERIFICACIÓN DE CONTEO
# ---------------------------------------------------------------------------
total = sum(len(c[2]) for c in CATEGORIAS)
assert total == 100, f"Se esperaban 100 mensajes, hay {total}"

CSS = """
:root{--azul:#0B3D6B;--azul2:#1573C6;--verde:#25D366;--verde-osc:#0E7A4A;
--grafito:#26303B;--gris:#5C6B7A;--gris-claro:#EAF0F5;--gris-borde:#D7E0E8;--amarillo:#FFC53D;}
*{box-sizing:border-box;}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif;color:var(--grafito);margin:0;font-size:10.5pt;line-height:1.55;}
.page{page-break-after:always;padding:22mm 20mm;position:relative;min-height:100vh;}
.page:last-child{page-break-after:auto;}
h1{color:#fff;margin:0;}
h2{color:var(--azul);font-size:17pt;border-bottom:3px solid var(--verde);padding-bottom:.2em;margin:0 0 .5em;}
h3{color:var(--azul2);font-size:12.5pt;margin:1.1em 0 .3em;}
p{margin:.45em 0;}ul,ol{margin:.4em 0 .8em;padding-left:1.2em;}li{margin:.28em 0;}
strong,b{color:var(--azul);}
.kicker{text-transform:uppercase;letter-spacing:.16em;font-size:8.5pt;color:var(--verde-osc);font-weight:700;margin-bottom:.3em;}
.divider{height:3px;width:54px;background:var(--verde);border-radius:3px;margin:7px 0 14px;}
.cover{background:linear-gradient(150deg,var(--azul),var(--azul2) 58%,var(--verde-osc) 130%);color:#fff;
display:flex;flex-direction:column;justify-content:space-between;padding:28mm 22mm;min-height:100vh;page-break-after:always;}
.cover .brand{letter-spacing:.22em;text-transform:uppercase;font-weight:700;font-size:11pt;}
.cover .brand span{color:var(--amarillo);}
.cover .wa{display:inline-block;background:var(--verde);color:#04331f;font-weight:800;padding:5px 15px;border-radius:30px;font-size:11pt;}
.cover h1{font-size:38pt;line-height:1.05;margin:.15em 0;}
.cover .big100{font-size:90pt;font-weight:800;line-height:.9;color:var(--amarillo);margin:0;}
.cover .sub{font-size:13.5pt;font-weight:300;opacity:.96;max-width:88%;}
.cover .pill{display:inline-flex;gap:7px;flex-wrap:wrap;margin-top:6px;}
.cover .pill span{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);padding:4px 12px;border-radius:20px;font-size:9pt;}
.cover .tagc{font-size:9pt;background:var(--amarillo);color:#3a2a00;font-weight:800;padding:4px 11px;border-radius:6px;display:inline-block;}
.cover .foot{font-size:9.5pt;opacity:.85;border-top:1px solid rgba(255,255,255,.3);padding-top:12px;}
.runhead{position:absolute;top:10mm;left:20mm;right:20mm;display:flex;justify-content:space-between;
font-size:7.5pt;color:var(--gris);text-transform:uppercase;letter-spacing:.1em;border-bottom:1px solid var(--gris-borde);padding-bottom:4px;}
.runhead b{color:var(--verde-osc);}
.cathead{background:linear-gradient(120deg,var(--azul),var(--azul2));color:#fff;border-radius:14px;padding:18px 22px;margin:0 0 16px;}
.cathead .n{font-size:9pt;letter-spacing:.14em;text-transform:uppercase;opacity:.85;color:#cfe6ff;}
.cathead h2{color:#fff;border:none;margin:.1em 0 .3em;font-size:18pt;}
.cathead p{margin:0;font-size:10pt;opacity:.95;color:#eaf3ff;}
.cathead .count{display:inline-block;background:var(--verde);color:#04331f;font-weight:800;padding:2px 12px;border-radius:20px;font-size:9pt;margin-top:8px;}
.msg{background:#fff;border:1px solid var(--gris-borde);border-radius:12px;padding:13px 16px;margin:11px 0;page-break-inside:avoid;}
.msg .top{display:flex;align-items:center;gap:9px;margin-bottom:7px;}
.msg .num{display:inline-flex;align-items:center;justify-content:center;min-width:26px;height:26px;background:var(--azul);
color:#fff;border-radius:7px;font-weight:800;font-size:10pt;flex:none;}
.msg .titulo{font-weight:800;color:var(--azul);font-size:11pt;}
.bubble{background:#D9FDD3;border:1px solid #b8eeae;border-radius:4px 12px 12px 12px;padding:9px 13px;margin:5px 0;
font-size:10pt;color:var(--grafito);line-height:1.45;white-space:pre-line;}
.bubble.short{background:#EAF3FC;border-color:#cfe3f7;}
.lbl{display:block;font-size:7.5pt;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--verde-osc);margin:8px 0 2px;}
.lbl.s{color:var(--azul2);}
.when{margin-top:8px;font-size:9pt;color:var(--gris);background:var(--gris-claro);border-radius:8px;padding:6px 11px;}
.when b{color:var(--verde-osc);}
.box{background:var(--gris-claro);border-radius:12px;padding:15px 19px;margin:13px 0;}
.card{background:#fff;border:1px solid var(--gris-borde);border-left:5px solid var(--verde);border-radius:0 10px 10px 0;padding:12px 17px;margin:10px 0;}
.card h3{margin-top:0;}
.copybox{background:#fff;border:1.5px dashed var(--verde);border-radius:10px;padding:12px 16px;margin:9px 0;font-size:10pt;line-height:1.5;}
.check{list-style:none;padding-left:0;}
.check li{padding-left:28px;position:relative;margin:.42em 0;}
.check li:before{content:"\\2713";position:absolute;left:0;top:-1px;width:19px;height:19px;background:var(--verde);
color:#fff;border-radius:5px;text-align:center;font-weight:800;font-size:10pt;line-height:19px;}
.lead{font-size:12pt;color:var(--gris);line-height:1.5;}
ol.steps{counter-reset:s;list-style:none;padding-left:0;}
ol.steps li{position:relative;padding-left:38px;margin:.7em 0;}
ol.steps li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:-2px;width:26px;height:26px;
background:var(--verde);color:#fff;border-radius:50%;text-align:center;line-height:26px;font-weight:800;font-size:11pt;}
ol.steps b{display:block;}
table{width:100%;border-collapse:collapse;margin:11px 0;font-size:9.5pt;}
th{background:var(--azul);color:#fff;text-align:left;padding:8px 10px;}
td{border:1px solid var(--gris-borde);padding:8px 10px;vertical-align:top;}
.toc-item{display:flex;justify-content:space-between;border-bottom:1px dotted var(--gris-borde);padding:6px 0;font-size:10.5pt;}
.toc-item .c{color:var(--azul2);font-weight:700;}
.best{background:#EAFBF1;border:1px solid var(--verde);border-radius:10px;padding:6px 14px;margin:8px 0;}
"""

def esc(t):
    return html.escape(t).replace("\n", "<br>")

def bullets(items):
    return "".join(f"<li>{esc(i)}</li>" for i in items)

# ============================ HTML (para PDF) ============================
def gen_html():
    cat_idx = "".join(
        f'<div class="toc-item"><span><span class="c">{i+1}.</span> {esc(c[0])}</span>'
        f'<span style="color:#5C6B7A;font-weight:700">{len(c[2])} msj</span></div>'
        for i, c in enumerate(CATEGORIAS))

    out = [f"<!DOCTYPE html><html lang='es'><head><meta charset='UTF-8'>"
           f"<title>Pack 100 Respuestas para WhatsApp</title><style>{CSS}</style></head><body>"]

    # Portada
    out.append(f"""<section class="cover">
      <div class="brand">Academia <span>Venta Digital</span></div>
      <div>
        <span class="wa">WhatsApp Business</span>
        <div class="big100">100</div>
        <h1>Respuestas para<br>WhatsApp</h1>
        <p class="sub">Mensajes listos para responder, hacer seguimiento y cerrar ventas sin quedarte en blanco.</p>
      </div>
      <div>
        <div class="pill"><span>Copiar y pegar</span><span>Editables</span><span>Variante corta</span><span>Cuándo enviarlo</span></div>
        <br><span class="tagc">COMPLEMENTO DE WHATSAPP VENTAS PRO</span>
      </div>
      <div class="foot">Academia Venta Digital · Aprende a vender con orden, no con suerte.</div>
    </section>""")

    # Intro + índice
    out.append(f"""<section class="page">
      <div class="runhead"><span>Pack 100 Respuestas</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Antes de empezar</div><h2>Bienvenido a tu pack de respuestas</h2><div class="divider"></div>
      <p>{INTRO}</p>
      <h3>Las 9 categorías del pack</h3>{cat_idx}
      <div class="best"><b>100 mensajes</b> · cada uno con mensaje completo, variante corta y recomendación de cuándo enviarlo.</div>
    </section>""")

    # Instrucciones de uso
    pasos = "".join(f"<li><b>{esc(t)}</b>{esc(d)}</li>" for t, d in INSTRUCCIONES)
    out.append(f"""<section class="page">
      <div class="runhead"><span>Instrucciones de uso</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Cómo usar este pack</div><h2>Instrucciones de uso</h2><div class="divider"></div>
      <p class="lead">Saca el máximo provecho en 7 pasos simples. La idea es que respondas más rápido y mejor, sin sonar como un robot.</p>
      <ol class="steps">{pasos}</ol>
      <div class="box"><b>Recuerda:</b> estos mensajes son una base para ordenar y mejorar tu comunicación. No prometen ventas garantizadas: tu producto, tu trato y tu constancia son los que cierran.</div>
    </section>""")

    # Las 9 categorías con sus mensajes
    for ci, (cnombre, cintro, mensajes) in enumerate(CATEGORIAS):
        cards = []
        for mi, (titulo, mensaje, corta, cuando) in enumerate(mensajes):
            n = sum(len(CATEGORIAS[k][2]) for k in range(ci)) + mi + 1
            cards.append(f"""<div class="msg">
              <div class="top"><span class="num">{n}</span><span class="titulo">{esc(titulo)}</span></div>
              <span class="lbl">Mensaje listo para copiar</span>
              <div class="bubble">{esc(mensaje)}</div>
              <span class="lbl s">Variante más corta</span>
              <div class="bubble short">{esc(corta)}</div>
              <div class="when"><b>Cuándo enviarlo:</b> {esc(cuando)}</div>
            </div>""")
        head = f"""<div class="cathead"><div class="n">Categoría {ci+1}</div>
          <h2>{esc(cnombre)}</h2><p>{esc(cintro)}</p><span class="count">{len(mensajes)} mensajes</span></div>"""
        out.append(f"""<section class="page">
          <div class="runhead"><span>Cat. {ci+1} · {esc(cnombre)}</span><span><b>Academia Venta Digital</b></span></div>
          {head}{''.join(cards)}</section>""")

    # Checklist
    out.append(f"""<section class="page">
      <div class="runhead"><span>Checklist de seguimiento</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Para no perder ninguna venta</div><h2>Checklist de seguimiento diario</h2><div class="divider"></div>
      <p class="lead">Repasa esta lista al final de cada día. Si la cumples, tu comunicación está ordenada.</p>
      <ul class="check">{bullets(CHECKLIST)}</ul>
      <div class="box"><b>Tip:</b> imprime esta página o tenla a mano en tu celular. La constancia en el seguimiento es lo que diferencia a quien vende con orden de quien vende por suerte.</div>
    </section>""")

    # Prompts IA
    prompts = "".join(f'<div class="copybox"><b>Prompt {i+1}.</b> {esc(p)}</div>' for i, p in enumerate(PROMPTS_IA))
    out.append(f"""<section class="page">
      <div class="runhead"><span>Prompts de IA</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Adapta el pack a tu negocio</div><h2>10 prompts de IA para personalizar tus mensajes</h2><div class="divider"></div>
      <p class="lead">Copia estos prompts en ChatGPT u otra IA para adaptar los mensajes a tu rubro. Revisa siempre el resultado antes de usarlo.</p>
      {prompts}
    </section>""")

    # Material de venta: Hotmart corta + larga
    incluye = bullets(HOTMART_LARGA_INCLUYE)
    out.append(f"""<section class="page">
      <div class="runhead"><span>Material de venta</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Sección de marketing</div><h2>Descripciones para Hotmart</h2><div class="divider"></div>
      <h3>Descripción corta</h3><div class="copybox">{esc(HOTMART_CORTA)}</div>
      <h3>Descripción larga</h3><div class="card"><p>{HOTMART_LARGA_INTRO}</p>
      <p><b>¿Qué incluye?</b></p><ul>{incluye}</ul>
      <p><b>¿Para quién es?</b> Para emprendedores, vendedores, negocios locales, revendedores, prestadores de servicios y cualquiera que venda por WhatsApp y quiera responder mejor sin improvisar.</p>
      <p style="color:#5C6B7A;font-size:9pt"><i>Aviso: material educativo. No promete ventas garantizadas ni resultados. Los resultados dependen de cada persona, su producto y su constancia.</i></p></div>
      <div class="box" style="font-size:9pt;color:#5C6B7A;margin-top:12px"><b>{esc(AVISO_MARCAS_HOTMART.split(':')[0])}:</b> {esc(AVISO_MARCAS_HOTMART.split(':',1)[1].strip())}</div>
    </section>""")

    # Order bump + Canva + portada + contraportada
    canva = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in CANVA_IDEAS)
    out.append(f"""<section class="page">
      <div class="runhead"><span>Material de venta</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Order Bump</div><h2>Texto para el checkout (Order Bump)</h2><div class="divider"></div>
      <div class="copybox">{ORDER_BUMP}</div>
      <div class="kicker" style="margin-top:24px">Diseño</div><h2>3 ideas de diseño en Canva</h2><div class="divider"></div>
      {canva}
    </section>""")

    out.append(f"""<section class="page">
      <div class="runhead"><span>Material de venta</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Diseño</div><h2>Portada sugerida</h2><div class="divider"></div>
      <div class="card">{PORTADA}</div>
      <div class="kicker" style="margin-top:24px">Diseño</div><h2>Contraportada</h2><div class="divider"></div>
      <div class="card">{CONTRAPORTADA}</div>
    </section>""")

    # Avisos legales (página final)
    avisos = "".join(
        f'<div class="box" style="border:1px solid var(--gris-borde)"><h3 class="mt0" style="margin-top:0">{esc(t)}</h3>'
        f'<p class="mt0" style="margin:0">{d}</p></div>' for t, d in AVISOS)
    out.append(f"""<section class="page">
      <div class="runhead"><span>Avisos legales</span><span><b>Academia Venta Digital</b></span></div>
      <div class="kicker">Información importante</div><h2>Avisos legales</h2><div class="divider"></div>
      {avisos}
      <p class="center" style="margin-top:22px;color:var(--gris);font-size:9pt">© Academia Venta Digital · Todos los derechos reservados. Prohibida su reventa o distribución sin autorización.</p>
    </section>""")

    out.append("</body></html>")
    return "\n".join(out)

# ============================ MARKDOWN EDITABLE ============================
def gen_md():
    L = ["# Pack 100 Respuestas para WhatsApp",
         "### Academia Venta Digital",
         "_Mensajes listos para responder, hacer seguimiento y cerrar ventas sin quedarte en blanco._",
         "",
         "> **Plantilla editable.** Reemplaza el texto entre [corchetes] con los datos de tu negocio. "
         "Copia cada mensaje y guárdalo como respuesta rápida en WhatsApp Business.",
         "", "---", "", "## Introducción",
         INTRO.replace("<b>", "**").replace("</b>", "**"), "", "---", "",
         "## Instrucciones de uso", ""]
    for i, (t, d) in enumerate(INSTRUCCIONES, 1):
        L.append(f"{i}. **{t}** {d}")
    L += ["", "---", "", "## Los 100 mensajes", ""]
    for ci, (cnombre, cintro, mensajes) in enumerate(CATEGORIAS, 1):
        L += [f"## {ci}. {cnombre} ({len(mensajes)} mensajes)", f"_{cintro}_", ""]
        base = sum(len(CATEGORIAS[k][2]) for k in range(ci - 1))
        for mi, (titulo, mensaje, corta, cuando) in enumerate(mensajes, 1):
            n = base + mi
            L += [f"### {n}. {titulo}",
                  f"**Mensaje:**", f"> {mensaje.replace(chr(10), chr(10)+'> ')}", "",
                  f"**Variante corta:**", f"> {corta}", "",
                  f"**Cuándo enviarlo:** {cuando}", ""]
        L.append("---\n")
    L += ["## Checklist de seguimiento diario", ""]
    L += [f"- [ ] {c}" for c in CHECKLIST]
    L += ["", "---", "", "## 10 prompts de IA para adaptar los mensajes", ""]
    for i, p in enumerate(PROMPTS_IA, 1):
        L.append(f"{i}. {p}")
    L += ["", "---", "", "## Material de venta", "",
          "### Descripción corta (Hotmart)", "", HOTMART_CORTA, "",
          "### Descripción larga (Hotmart)", "",
          HOTMART_LARGA_INTRO.replace("<b>", "**").replace("</b>", "**"), "",
          "**¿Qué incluye?**", ""]
    L += [f"- {x}" for x in HOTMART_LARGA_INCLUYE]
    L += ["", "### Texto Order Bump (checkout)", "",
          ORDER_BUMP.replace("<b>", "**").replace("</b>", "**").replace("<i>", "_").replace("</i>", "_"), "",
          "### 3 ideas de diseño en Canva", ""]
    for t, d in CANVA_IDEAS:
        L.append(f"- **{t}** {d.replace('<b>', '**').replace('</b>', '**')}")
    L += ["", "### Portada sugerida", "",
          PORTADA.replace("<b>", "**").replace("</b>", "**").replace("•", "-"), "",
          "### Contraportada", "",
          CONTRAPORTADA.replace("<b>", "**").replace("</b>", "**").replace("<i>", "_").replace("</i>", "_"), ""]
    L += ["---", "", "## Avisos legales", ""]
    for t, d in AVISOS:
        L += [f"**{t}.** " + d.replace("<b>", "**").replace("</b>", "**"), ""]
    L += ["_© Academia Venta Digital · Todos los derechos reservados. "
          "Prohibida su reventa o distribución sin autorización._", ""]
    return "\n".join(L)

# ============================ CSV (respuestas rápidas) ============================
def gen_csv():
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["N", "Categoria", "Titulo", "Mensaje", "Variante_corta", "Cuando_enviarlo"])
    n = 0
    for cnombre, _, mensajes in CATEGORIAS:
        for titulo, mensaje, corta, cuando in mensajes:
            n += 1
            w.writerow([n, cnombre, titulo, mensaje, corta, cuando])
    return buf.getvalue()

if __name__ == "__main__":
    open("pack-100-respuestas.html", "w", encoding="utf-8").write(gen_html())
    open("pack-100-respuestas-EDITABLE.md", "w", encoding="utf-8").write(gen_md())
    open("pack-100-respuestas.csv", "w", encoding="utf-8").write(gen_csv())
    print(f"OK · {total} mensajes · HTML + MD + CSV generados")
