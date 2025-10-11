package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
)

var (
	cache      = make(map[string]string)
	cacheMutex = sync.RWMutex{}
)

// Caching endpoint (LRU logic simplified)
func cacheHandler(w http.ResponseWriter, r *http.Request) {
	cacheMutex.Lock()
	cache["session"] = "data"
	cacheMutex.Unlock()
	w.Write([]byte("Cached session data"))
}

// Routing endpoint
func routeHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Routing packet..."))
}

// Fast reroute failover endpoint
func failoverHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Rerouting to next edge node"))
}

// Metrics endpoint
func metricsHandler(w http.ResponseWriter, r *http.Request) {
	resp := map[string]string{"dc_np_ratio": "0.1/0.9"}
	json.NewEncoder(w).Encode(resp)
}

func main() {
	fmt.Println("Mesh Agent starting...")
	http.HandleFunc("/cache", cacheHandler)
	http.HandleFunc("/route", routeHandler)
	http.HandleFunc("/failover", failoverHandler)
	http.HandleFunc("/metrics/edge", metricsHandler)
	http.ListenAndServe(":8081", nil)
}
