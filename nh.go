package main

import (
	"fmt"
	"net/http"

	nhapi "github.com/bitbandi/go-nicehash-api"
)

func main() {

	url := ""
	key := "98cbf48d-513b-c9c6-1d6f-9aeb3d95afda"
	id := "1343547"

	httpClient := &http.Client{}

	nh := nhapi.NewNicehashClient(httpClient, url, id, key, "")

	balance, err := nh.GetBalance()
	if err == nil {
		fmt.Printf("%v\n", balance)
	}

}
