# Monitor de Noticias de Derecho Medioambiental — Chile

Actualización automática diaria de las 69 fuentes más relevantes para derecho medioambiental en Chile, con filtrado inteligente por IA.

---

## ¿Cómo funciona?

Cada mañana a las **8:00 AM** (hora de Chile), un programa automático:
1. Visita las 69 fuentes configuradas y extrae las noticias de las últimas 24 horas
2. Usa inteligencia artificial para quedarse solo con las noticias relevantes al derecho medioambiental
3. Guarda los resultados en una tabla que tú puedes ver en la web

Tú no tienes que hacer nada. Entras a tu web cada mañana y están las noticias listas.

---

## Requisitos previos

No necesitas saber programar. Solo necesitas:
- Una cuenta de email (Gmail o cualquier otra)
- Un computador con acceso a internet
- Unos 30 minutos para la configuración inicial (solo se hace una vez)

---

## Paso 1: Crear una cuenta en GitHub

GitHub es el servicio donde vive el código y donde se ejecuta la automatización. Es gratuito.

1. Ve a **https://github.com** y haz clic en **"Sign up"**
2. Ingresa tu email, crea una contraseña y elige un nombre de usuario
3. Verifica tu email cuando te llegue el correo de confirmación
4. Inicia sesión en tu nueva cuenta

---

## Paso 2: Subir este proyecto a GitHub

1. Inicia sesión en GitHub
2. Haz clic en el botón verde **"New"** (en la esquina superior izquierda)
3. En **"Repository name"** escribe: `monitor-medioambiental`
4. Deja la opción **"Public"** seleccionada
5. Haz clic en **"Create repository"**

Ahora debes subir los archivos. La forma más fácil es usando la interfaz web de GitHub:

6. En la página de tu repositorio vacío, haz clic en **"uploading an existing file"**
7. Arrastra y suelta todos los archivos y carpetas de este proyecto
   - `index.html`
   - La carpeta `data/` (con sus dos archivos JSON)
   - La carpeta `scraper/` (con sus tres archivos)
   - La carpeta `.github/` (con su subcarpeta y el archivo .yml)
8. Al final haz clic en **"Commit changes"**

> **Nota:** Si la carpeta `.github` no aparece porque está oculta, en Windows activa "Mostrar archivos ocultos" en el Explorador de archivos.

---

## Paso 3: Obtener la clave de Gemini (IA gratuita)

Gemini es la inteligencia artificial de Google que filtra las noticias relevantes. Tiene un plan gratuito más que suficiente.

1. Ve a **https://aistudio.google.com**
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Get API key"** (en el menú izquierdo)
4. Haz clic en **"Create API key"**
5. Selecciona **"Create API key in new project"**
6. Se generará una clave que comienza con `AIza...`
7. **Cópiala y guárdala en un lugar seguro** (no la compartas con nadie)

---

## Paso 4: Configurar la clave en GitHub

Para que el programa automático pueda usar Gemini, hay que guardar la clave de forma segura en GitHub.

1. Ve a tu repositorio `monitor-medioambiental` en GitHub
2. Haz clic en **"Settings"** (pestaña en la parte superior)
3. En el menú izquierdo, busca **"Secrets and variables"** y haz clic en **"Actions"**
4. Haz clic en el botón **"New repository secret"**
5. En **"Name"** escribe exactamente: `GEMINI_API_KEY`
6. En **"Secret"** pega la clave que copiaste en el paso anterior
7. Haz clic en **"Add secret"**

Listo. La clave está guardada de forma segura y el programa la usará automáticamente.

---

## Paso 5: Conectar a Vercel (para tener tu propia web)

Vercel es el servicio que muestra tu web en internet. Es gratuito para proyectos pequeños.

1. Ve a **https://vercel.com** y haz clic en **"Sign Up"**
2. Elige **"Continue with GitHub"** para conectar tu cuenta de GitHub
3. Autoriza a Vercel a acceder a tus repositorios
4. Una vez dentro, haz clic en **"Add New Project"**
5. Busca tu repositorio `monitor-medioambiental` y haz clic en **"Import"**
6. En la pantalla de configuración, **no cambies nada**, solo haz clic en **"Deploy"**
7. Espera 1-2 minutos mientras Vercel construye tu web
8. Cuando aparezca el mensaje **"Congratulations!"**, haz clic en **"Visit"**

Ya tienes tu web en una dirección como `monitor-medioambiental.vercel.app`

---

## Paso 6: Ejecutar el scraper por primera vez

La web está lista pero todavía no tiene noticias porque el programa automático no ha corrido aún (corre solo en las mañanas). Para ver las primeras noticias hoy mismo:

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña **"Actions"**
3. En el menú izquierdo verás **"Actualizar Noticias Medioambientales"**, haz clic ahí
4. Haz clic en el botón **"Run workflow"** (en la parte derecha)
5. En el menú que aparece, haz clic en el botón verde **"Run workflow"**
6. Espera entre 5 y 10 minutos mientras el programa corre

Cuando termine, aparecerá un ✅ verde. Después:
7. Ve a tu web en Vercel y recarga la página
8. Deberías ver las noticias del día en la tabla

---

## Paso 7: Verificar que todo funciona

Para confirmar que todo está bien configurado:

- **La web muestra noticias:** ✅ Todo funciona
- **La web dice "El monitor aún no tiene datos":** Vuelve al Paso 6 y ejecuta el workflow
- **Las noticias dicen "Sin filtro IA":** La clave de Gemini no está bien configurada, revisa el Paso 4
- **El workflow muestra ❌ rojo:** Lee la sección de solución de problemas abajo

Desde ahora, cada mañana a las 8:00 AM el programa corre solo y actualiza las noticias automáticamente.

---

## Solución de problemas frecuentes

### "El workflow falla con error rojo"
1. Ve a GitHub → Actions → haz clic en el workflow fallido
2. Haz clic en el paso con el error (mostrará texto en rojo)
3. Los errores más comunes son:
   - **`GEMINI_API_KEY not found`**: Repite el Paso 4
   - **`ModuleNotFoundError`**: Las dependencias no se instalaron; contacta soporte
   - **`git push failed`**: Ve a Settings → Actions → General → en "Workflow permissions" activa "Read and write permissions"

### "La web no se actualiza aunque el workflow fue exitoso"
Vercel se actualiza automáticamente cuando hay cambios en GitHub, pero puede tardar 1-2 minutos. Si después de 5 minutos sigue igual:
1. Ve a Vercel → tu proyecto → haz clic en **"Redeploy"**

### "Veo muy pocas noticias o ninguna"
Puede ser que hoy no haya habido noticias relevantes (es posible algunos días), o que la IA las haya filtrado. Puedes verificar mirando el log del workflow en GitHub Actions → busca la línea que dice "Total artículos nuevos candidatos".

### "Quiero agregar una fuente nueva"
Abre el archivo `scraper/fuentes.py` en GitHub (haz clic sobre él → ícono de lápiz para editar) y agrega una nueva entrada siguiendo el mismo formato que las existentes. Guarda los cambios con "Commit changes".

### "Quiero cambiar la hora de actualización"
Abre `.github/workflows/actualizar.yml` y cambia la línea `cron: '0 11 * * *'`.
El formato es `minuto hora día mes día_semana` en hora UTC.
Chile es UTC-3, así que hora Chile + 3 = hora UTC.
Ejemplo: 7:00 AM Chile = 10:00 UTC → `cron: '0 10 * * *'`

---

## Estructura del proyecto

```
monitor-medioambiental/
├── index.html              ← La página web que ves en el navegador
├── data/
│   ├── noticias.json       ← Noticias del día (se reemplaza cada mañana)
│   └── historial.json      ← URLs ya vistas (evita repetir noticias)
├── scraper/
│   ├── main.py             ← Programa principal de scraping y clasificación
│   ├── fuentes.py          ← Lista de las 69 fuentes monitoreadas
│   └── requirements.txt    ← Librerías Python necesarias
├── .github/
│   └── workflows/
│       └── actualizar.yml  ← Instrucciones para GitHub Actions
├── ROADMAP.md              ← Visión futura del producto
└── README.md               ← Este archivo
```

---

## Costos

| Servicio | Plan | Costo |
|----------|------|-------|
| GitHub | Free | $0 |
| Vercel | Hobby | $0 |
| Google Gemini | Free tier (1.500 req/día) | $0 |
| **Total** | | **$0/mes** |

El tier gratuito de Gemini es más que suficiente para el volumen diario de este monitor.

---

## Preguntas frecuentes

**¿Puedo usar esto en móvil?**
Sí, la web está diseñada para funcionar bien en celular y computador.

**¿Las noticias son de las últimas 24 horas?**
Sí, el scraper solo toma noticias publicadas en las últimas 24 horas. No aparecerán noticias de días anteriores.

**¿Qué pasa si una fuente está caída o bloquea el scraper?**
El programa registra el error, lo anota en los logs y continúa con las demás fuentes. No falla por un solo sitio caído.

**¿Puedo exportar las noticias a Excel?**
No está incluido en esta versión. Está planificado para una versión futura (ver ROADMAP.md).

**¿La IA puede equivocarse y filtrar noticias relevantes?**
Sí, ocasionalmente puede pasar. La IA tiene una configuración amplia para minimizar los falsos negativos (excluir noticias relevantes), pero no es perfecta.

---

*Para soporte técnico o sugerencias, abre un "Issue" en el repositorio de GitHub.*
