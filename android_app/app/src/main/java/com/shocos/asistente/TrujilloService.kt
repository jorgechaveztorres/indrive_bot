package com.shocos.asistente
import android.accessibilityservice.AccessibilityService
import android.graphics.PixelFormat
import android.graphics.drawable.GradientDrawable
import android.view.View
import android.view.WindowManager
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import android.animation.ObjectAnimator
import android.os.Handler
import android.os.Looper

class TrujilloService : AccessibilityService() {

    private var windowManager: WindowManager? = null
    private var overlayView: View? = null

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event?.packageName != "com.indriver") return
        
        val root = rootInActiveWindow ?: return
        // ESTUDIO: Busca cards de solicitud en inDrive
        val cards = root.findAccessibilityNodeInfosByViewId("com.indriver:id/request_card")
        if (cards.isEmpty()) {
            // Fallback: busca por texto "S/"
            buscarPorTexto(root)
            return
        }
        for (card in cards) {
            if (evaluarCard(card)) {
                // CUMPLE TODO -> Abre siguiente pantalla
                card.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                // Parpadeo verde en la card que cumplió
                Handler(Looper.getMainLooper()).postDelayed({
                    mostrarParpadeoVerde(card)
                }, 500)
                break // solo una a la vez
            }
        }
    }

    private fun evaluarCard(card: AccessibilityNodeInfo): Boolean {
        // ESTUDIO: Aquí iría tu lógica de rentabilidad_calculator.py portada a Kotlin
        // Simulado: extrae tarifa, km, zona del texto de la card
        val texto = card.text?.toString() ?: card.contentDescription?.toString() ?: ""
        // Ejemplo: "Florencia 1.2 km S/14"
        // Tu regla punta a punta: recojo <=2km, S/0.18/km, zona no penalizada
        if (texto.contains("El Porvenir") || texto.contains("La Esperanza") || texto.contains("Florencia de Mora")) return false
        if (texto.contains("S/")) {
            // Extrae números y evalúa - aquí simplificado
            return true // si pasa tus reglas
        }
        return false
    }

    private fun buscarPorTexto(root: AccessibilityNodeInfo) {
        // Método alternativo para Termux
    }

    private fun mostrarParpadeoVerde(card: AccessibilityNodeInfo) {
        if (overlayView != null) return
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager
        val bounds = android.graphics.Rect()
        card.getBoundsInScreen(bounds)

        overlayView = View(this).apply {
            background = GradientDrawable().apply {
                setStroke(8, 0xFF00FF00.toInt()) // Borde verde 8dp
                setColor(0x3300FF00) // Fondo verde transparente
            }
        }
        val params = WindowManager.LayoutParams(
            bounds.width(), bounds.height(),
            bounds.left, bounds.top,
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE,
            PixelFormat.TRANSLUCENT
        )
        windowManager?.addView(overlayView, params)

        // Parpadeo 400ms infinito
        ObjectAnimator.ofFloat(overlayView, "alpha", 0f, 1f).apply {
            duration = 400
            repeatMode = ObjectAnimator.REVERSE
            repeatCount = ObjectAnimator.INFINITE
            start()
        }

        // Auto-quita en 8 segundos para dejarte aceptar manual
        Handler(Looper.getMainLooper()).postDelayed({ quitarOverlay() }, 8000)
    }

    private fun quitarOverlay() {
        overlayView?.let { windowManager?.removeView(it) }
        overlayView = null
    }

    override fun onInterrupt() {}
}
