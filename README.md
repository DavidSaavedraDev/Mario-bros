<div align="center">

  <img src="https://media.giphy.com/media/3oKIPsx2VAYAgEHC12/giphy.gif" width="220" alt="Mario Bros en acción">

  # 🍄 SUPER MARIO BROS. · PIXEL ADVENTURE

  ### Un homenaje retro creado desde cero con Python y Pygame

  <img src="https://img.shields.io/badge/PYTHON-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PYGAME-2.x-45B649?style=for-the-badge&logo=python&logoColor=white" alt="Pygame">
  <img src="https://img.shields.io/badge/PIXEL%20ART-CODE%20GENERATED-F2C94C?style=for-the-badge&logo=gamepad&logoColor=111827" alt="Pixel Art">
  <img src="https://img.shields.io/badge/STATUS-PLAYABLE-00C853?style=for-the-badge&logo=rocket&logoColor=white" alt="Estado">
  <img src="https://img.shields.io/github/license/DavidSaavedraDev/Mario-bros?style=for-the-badge&logo=github&label=LICENSE" alt="Licencia">

  <br>
  <br>

  **Plataformas · monedas · Goombas · tuberías · saltos · nostalgia de 8 bits**

</div>

---

## 🕹️ Sobre el proyecto

**Mario Bros. · Pixel Adventure** es un prototipo jugable desarrollado en Python/Pygame
con una regla especial: **todos los sprites y elementos visuales se dibujan directamente
con `pygame.Surface` y primitivas de dibujo**. No depende de imágenes externas para crear
su estética pixel art.

El proyecto combina una base sencilla y extensible con una presentación inspirada en los
clásicos juegos de plataformas de 8 bits.

## ✨ Características

| Sistema | Detalles |
|---|---|
| 🎨 **Pixel Art por código** | Mario, Goombas, monedas, bloques, tuberías, nubes y colinas generados con superficies y rectángulos pixelados. |
| 🧢 **Jugador animado** | Gorra roja, overol azul, animación al caminar y sprite especial durante el salto. |
| 👾 **Enemigos** | Goombas con animación de pasos, movimiento lateral y derrota al saltar sobre ellos. |
| 🪙 **Monedas** | Animación giratoria, recolección y puntuación. |
| 🧱 **Nivel retro** | Bloques de ladrillo, bloques sorpresa, tuberías verdes y plataformas elevadas. |
| 🌤️ **Fondo clásico** | Cielo azul, nubes con ojos, colinas con textura y suelo de ladrillos. |
| ⚙️ **Física** | Gravedad, salto, movimiento horizontal, colisiones y límites de escenario. |
| ❤️ **Progresión** | Vidas, puntuación, invulnerabilidad temporal y pantalla de Game Over. |
| 🔁 **Reinicio** | Pulsa `R` para comenzar una nueva partida después del Game Over. |

## 🎮 Controles

| Acción | Teclado |
|---|---|
| Mover a la izquierda | `←` / `A` |
| Mover a la derecha | `→` / `D` |
| Saltar | `ESPACIO` / `↑` / `W` |
| Reiniciar tras perder | `R` |
| Salir | `ESC` |

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/DavidSaavedraDev/Mario-bros.git
cd Mario-bros
```

### 2. Crear un entorno virtual (recomendado)

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Pygame

```bash
python -m pip install pygame
```

### 4. Iniciar el juego

```bash
python main.py
```

> 💡 Se recomienda Python 3.10 o superior y una terminal con soporte para ejecutar
> aplicaciones gráficas.

## 🧰 Tecnologías usadas

| Tecnología | Uso |
|---|---|
| 🐍 **Python** | Lógica principal, clases, físicas y gestión del juego. |
| 🎮 **Pygame** | Ventana, eventos, reloj, sprites, superficies y renderizado. |
| 🧩 **Pygame Draw** | Construcción de personajes, escenarios y detalles pixelados. |
| 📦 **Python Standard Library** | `random` y `sys` para utilidades del prototipo. |
| 🛠️ **GitHub** | Control de versiones y presentación del proyecto. |

## 📁 Estructura

```text
Mario-bros/
├── main.py       # Juego completo y assets generados por código
└── README.md     # Documentación del proyecto
```

## 🌟 Ideas para futuras versiones

- [ ] Música y efectos de sonido retro.
- [ ] Más niveles y generación procedural.
- [ ] Power-ups adicionales.
- [ ] Pantalla de inicio y selección de nivel.
- [ ] Tabla de mejores puntuaciones.

---

<div align="center">

  ## 🧑‍💻 Hecho con ❤️, Python y muchos píxeles

  **David Saavedra** · [@DavidSaavedraDev](https://github.com/DavidSaavedraDev)

  ⭐ Si te gusta el proyecto, ¡dale una estrella en GitHub!

</div>
