package com.shocos.asistente
import android.accessibilityservice.AccessibilityService
import android.graphics.PixelFormat
import android.view.Gravity
import android.view.WindowManager
import android.view.accessibility.AccessibilityEvent
import android.widget.TextView
import android.os.Handler
import android.os.Looper
class TrujilloService : AccessibilityService() {
    private var overlayView: TextView? = null
    private val handler = Handler(Looper.getMainLooper())
    private var blinkRunnable: Runnable? = null
    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null) return
        val root = rootInActiveWindow ?: return
        if (!event.packageName.toString().contains("indriver", true)) return
        try {
            val nodes = root.findAccessibilityNodeInfosByText("S/")
            for (node in nodes) {
                val texto = (node.text?.toString() ?: "") + " " + (node.parent?.text?.toString() ?: "")
                if (texto.contains("S/") && !texto.contains("La Esperanza alta", true)) {
                    node.parent?.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_CLICK)
                    mostrarOverlayVerde()
                    break
                }
            }
        } catch (e: Exception) {}
    }
    fun mostrarOverlayVerde() {
        if (overlayView != null) return
        val wm = getSystemService(WINDOW_SERVICE) as WindowManager
        val tv = TextView(this).apply { text = " ✓ RENTABLE"; setBackgroundColor(0xFF00FF00.toInt()); textSize = 18f }
        val params = WindowManager.LayoutParams(-2,-2,WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY, WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE, PixelFormat.TRANSLUCENT).apply { gravity = Gravity.TOP or Gravity.CENTER_HORIZONTAL; y = 100 }
        try { wm.addView(tv, params); overlayView = tv } catch (e: Exception) { return }
        var visible = true
        blinkRunnable = object : Runnable { override fun run() { overlayView?.alpha = if (visible) 1f else 0f; visible = !visible; handler.postDelayed(this, 400) } }
        handler.post(blinkRunnable!!)
        handler.postDelayed({ try { wm.removeView(tv) } catch (_: Exception) {}; overlayView = null; blinkRunnable?.let { handler.removeCallbacks(it) } }, 5000)
    }
    override fun onInterrupt() {}
}
