Breakout es un juego arcade donde el jugador controla una paleta horizontal con el mouse para hacer rebotar una pelota y destruir todos los ladrillos dispuestos en la parte superior de la pantalla. El juego termina cuando se eliminan todos los ladrillos (victoria) o se agotan las 3 vidas (derrota).

Mecánicas implementadas

Paleta controlada por mouse con límites para no salirse de la pantalla
Pelota con física de rebote en paredes laterales, techo y paleta
Ángulo variable según el punto de impacto en la paleta
10 filas × 10 columnas de ladrillos en 5 colores (rojo, naranja, amarillo, verde, cyan)
Sistema de 3 vidas con contador en pantalla
Sistema de puntuación (10 puntos por ladrillo)
Detección anti-pegado al paddle para evitar el bug clásico del juego

Tecnologías usadas
Componente Detalle Lenguaje Python 3.8 + Interfaz gráfica tkinter (incluido con Python)
Aleatoriedad random (dirección inicial de la pelota)
Sin dependencias externas✅

Cómo ejecutarlo
bashpython breakout.py
