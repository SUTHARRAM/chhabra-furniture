package newcircuit 

import (
	"sync"
	"time"
)

type CircuitBreakerState int 

const (
	Closed CircuitBreakerState = iota
	Open
	HalfOpen
)

type CircuitBreaker struct {
	state CircuitBreakerState
	failureThreshold int 
	successThreshold int 
	failureCount int 
	successCount int
	lastFailureTime time.Time 
	mu sync.Mutex 
	retryTimeout time.Duration 
}

func NewCircuitBreaker(failureThreshold, successThreshold int, retryTimeout time.Duration) *CircuitBreaker {
	return &CircuitBreaker{
		state: Closed, 
		failureThreshold: failureThreshold, 
		successThreshold: successThreshold, 
		failureCount: 0, 
		successCount: 0, 
		retryTimeout: retryTimeout,
	}
}