package com.example.pigplotter

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.location.LocationManager
import android.media.AudioAttributes
import android.media.SoundPool
import android.os.Bundle
import android.webkit.GeolocationPermissions
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val ioExecutor = Executors.newSingleThreadExecutor()
    private var soundPool: SoundPool? = null
    private var dartSoundId: Int = 0

    companion object {
        private const val PREFS_NAME = "pigplotter_prefs"
        private const val KEY_SERVER_URL = "server_url"
        private const val DEFAULT_SERVER_URL = "https://pigplotter.duckdns.org"
        private const val REQ_LOCATION_PERMISSION = 1001
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

        val audioAttributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_ASSISTANCE_SONIFICATION)
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            .build()
        soundPool = SoundPool.Builder()
            .setMaxStreams(5)
            .setAudioAttributes(audioAttributes)
            .build()
        dartSoundId = soundPool?.load(this, R.raw.dart_throw, 1) ?: 0

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
            cacheMode = WebSettings.LOAD_DEFAULT
            userAgentString = "$userAgentString PigPlotter-Android/1.0"
            setGeolocationEnabled(true)
        }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })

        webView.webViewClient = WebViewClient()
        webView.webChromeClient = object : WebChromeClient() {
            override fun onGeolocationPermissionsShowPrompt(
                origin: String?,
                callback: GeolocationPermissions.Callback?
            ) {
                callback?.invoke(origin, true, false)
            }
        }

        webView.addJavascriptInterface(AndroidBridge(), "AndroidBridge")

        val htmlContent = assets.open("map.html").bufferedReader().use { it.readText() }
        webView.loadDataWithBaseURL(
            DEFAULT_SERVER_URL,
            htmlContent,
            "text/html",
            "UTF-8",
            null
        )
    }

    inner class AndroidBridge {

        @JavascriptInterface
        fun playPlotSound() {
            runOnUiThread {
                if (dartSoundId != 0) {
                    soundPool?.play(dartSoundId, 1.0f, 1.0f, 1, 0, 1.0f)
                }
            }
        }

        @JavascriptInterface
        fun getServerUrl(): String {
            val prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            return prefs.getString(KEY_SERVER_URL, DEFAULT_SERVER_URL) ?: DEFAULT_SERVER_URL
        }

        @JavascriptInterface
        fun setServerUrl(url: String) {
            val cleaned = url.trim().ifEmpty { DEFAULT_SERVER_URL }
            getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
                .edit()
                .putString(KEY_SERVER_URL, cleaned)
                .apply()
        }

        @JavascriptInterface
        fun postToPipe(pipeUrl: String, jsonPayload: String) {
            ioExecutor.execute {
                var conn: HttpURLConnection? = null
                try {
                    val targetUrl = URL(pipeUrl)
                    conn = (targetUrl.openConnection() as HttpURLConnection).apply {
                        requestMethod = "POST"
                        connectTimeout = 8000
                        readTimeout = 8000
                        doOutput = true
                        setRequestProperty("Content-Type", "application/json; charset=utf-8")
                        setRequestProperty("User-Agent", "PigPlotter-Android/1.0")
                    }
                    OutputStreamWriter(conn.outputStream, Charsets.UTF_8).use { writer ->
                        writer.write(jsonPayload)
                        writer.flush()
                    }
                    val code = conn.responseCode
                    runOnUiThread {
                        Toast.makeText(
                            this@MainActivity,
                            "Dispatched to /pipe (HTTP $code)",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                } catch (e: Exception) {
                    runOnUiThread {
                        Toast.makeText(
                            this@MainActivity,
                            "POST /pipe error: ${e.message}",
                            Toast.LENGTH_LONG
                        ).show()
                    }
                } finally {
                    conn?.disconnect()
                }
            }
        }

        @JavascriptInterface
        fun requestDeviceLocation() {
            runOnUiThread {
                if (ContextCompat.checkSelfPermission(
                        this@MainActivity,
                        Manifest.permission.ACCESS_FINE_LOCATION
                    ) != PackageManager.PERMISSION_GRANTED
                ) {
                    ActivityCompat.requestPermissions(
                        this@MainActivity,
                        arrayOf(
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION
                        ),
                        REQ_LOCATION_PERMISSION
                    )
                } else {
                    dispatchLastKnownLocation()
                }
            }
        }
    }

    @SuppressLint("MissingPermission")
    private fun dispatchLastKnownLocation() {
        try {
            val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
            val location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
                ?: locationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER)
            if (location != null) {
                webView.evaluateJavascript(
                    "window.onDeviceLocation && window.onDeviceLocation(${location.latitude}, ${location.longitude});",
                    null
                )
            } else {
                Toast.makeText(this, "No cached GPS fix available yet", Toast.LENGTH_SHORT).show()
            }
        } catch (e: Exception) {
            Toast.makeText(this, "Location error: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQ_LOCATION_PERMISSION &&
            grantResults.isNotEmpty() &&
            grantResults[0] == PackageManager.PERMISSION_GRANTED
        ) {
            dispatchLastKnownLocation()
        }
    }

    override fun onDestroy() {
        soundPool?.release()
        soundPool = null
        ioExecutor.shutdownNow()
        super.onDestroy()
    }
}
