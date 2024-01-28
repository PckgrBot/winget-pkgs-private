package handler

import (
	"encoding/json"
	"net/http"
)

func Information(w http.ResponseWriter, r *http.Request) {
	// only allow GET requests
	if r.Method != http.MethodGet {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]map[string]interface{}{
		"Data": {
			"SourceIdentifier":        "winget-pkgs-private",
			"ServerSupportedVersions": []string{"1.6.0"},
			"UnsupportedPackageMatchFields": []string{
				"Market",
			},
			"UnsupportedQueryParameters": []string{
				"Channel", "Market",
			},
		},
	})
}
