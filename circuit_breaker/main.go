package main 

import (
	"circuitb/newcircuit"
	"time"
	"fmt"
)

func main() {
	// Create a new circuit breaker with failure threshold of 3,
	// success threshold of 2, and retry timeout of 5 seconds.
	cb := newcircuit.NewCircuitBreaker(3, 2, 5*time.Second)

	// Simulate a few service calls
	for i := 0; i < 10; i++ {
		success := cb.Call(newcircuit.IsServiceHealthy)
		if success {
			fmt.Println("Service call succeeded.")
		} else {
			fmt.Println("Service call failed.")
		}
		time.Sleep(1 * time.Second)
	}
}
