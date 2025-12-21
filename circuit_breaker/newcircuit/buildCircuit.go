package newcircuit

import (
	"fmt"
	"time"
)

func IsServiceHealthy() bool {
	return time.Now().Unix()%2 == 0
}

func (cb *CircuitBreaker) Call(serviceCall func() bool) bool {
	cb.mu.Lock()
	defer cb.mu.Unlock()

	switch cb.state {
	case Open:
		if time.Since(cb.lastFailureTime) < cb.retryTimeout {
			fmt.Println("Circuit Breaker is Open: Request Rejected")
			return false
		}

		cb.state = HalfOpen
		fallthrough
	case HalfOpen: 
		if serviceCall() {
			cb.successCount++

			if cb.successCount >= cb.successThreshold {
			cb.state = Closed
			cb.successCount = 0
			cb.failureCount = 0
			fmt.Println("Circuit Breaker is CLOSED: Service Is Available")

			}
		return true
		} else {
			cb.failureCount++

			if cb.failureCount >= cb.failureThreshold {
				cb.state = Open 
				cb.lastFailureTime = time.Now()
				fmt.Println("Circuit Breaker is Open: Service is failing")
			}
			return false 
		}
	case Closed:
	if serviceCall() {
		cb.successCount++
		return true 
	} else {
		cb.failureCount++
		if cb.failureCount >= cb.failureThreshold {
			cb.state = Open 
			cb.lastFailureTime = time.Now()
			fmt.Println("Circuit Breaker is Open: Service is failed to many times.")

		}
		return false
	}
		
	}
	return false 
}