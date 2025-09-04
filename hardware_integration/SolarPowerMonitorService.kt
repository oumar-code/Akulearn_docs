// Service to connect SolarPowerMonitorImpl to Akulearn app
import com.akulearn.core.SolarStatus
import kotlinx.coroutines.*

class SolarPowerMonitorService(private val monitor: SolarPowerMonitor) {
    private var currentStatus: SolarStatus? = null
    private var listeners = mutableListOf<(SolarStatus) -> Unit>()

    fun startMonitoring(intervalMillis: Long = 60000L) {
        GlobalScope.launch {
            while (true) {
                val status = monitor.getStatus()
                currentStatus = status
                listeners.forEach { it(status) }
                delay(intervalMillis)
            }
        }
    }

    fun addListener(listener: (SolarStatus) -> Unit) {
        listeners.add(listener)
        currentStatus?.let { listener(it) }
    }

    fun getCurrentStatus(): SolarStatus? = currentStatus
}
