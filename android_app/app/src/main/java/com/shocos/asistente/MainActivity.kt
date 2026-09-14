package com.shocos.asistente
import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.Toast
class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            setContentView(R.layout.activity_main)
            val btn = findViewById<Button>(R.id.btnPermiso)
            btn.setOnClickListener {
                try { startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)) } catch (e: Exception) {}
                try {
                    if (!Settings.canDrawOverlays(this)) {
                        startActivity(Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:$packageName")))
                    }
                } catch (e: Exception) {}
                Toast.makeText(this, "Activa Asistente Trujillo + Overlay", Toast.LENGTH_LONG).show()
            }
        } catch (e: Exception) {
            // Si falla el layout, al menos no crashea
            Toast.makeText(this, "Asistente instalado. Activa en Ajustes > Accesibilidad", Toast.LENGTH_LONG).show()
            try { startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)) } catch (_: Exception) {}
            finish()
        }
    }
}
